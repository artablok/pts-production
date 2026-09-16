#!/usr/bin/env python3

import os
import base64
import json
import hashlib
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

RPC_URL = os.environ.get(
    "PTS_RPC_URL",
    "http://pts-production-node2:39011/rpc"
)

RPC_USER = os.environ["PTS_RPC_USER"]
RPC_PASS = os.environ["PTS_RPC_PASS"]

RPC_AUTH = base64.b64encode(
    (RPC_USER + ":" + RPC_PASS).encode("utf-8")
).decode("ascii")


def rpc(method, params=None):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params or [],
        "id": 1
    }).encode("utf-8")

    req = urllib.request.Request(
        RPC_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic " + RPC_AUTH
        }
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    if data.get("error"):
        raise RuntimeError(str(data["error"]))

    return data.get("result")


class Handler(BaseHTTPRequestHandler):

    def send_json(self, obj, status=200):
        body = json.dumps(
            obj,
            indent=2
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        path = urlparse(self.path).path

        if path != "/api/tx/broadcast":
            return self.send_json({
                "error": "OPTIONS endpoint not found"
            }, 404)

        self.send_response(204)
        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )
        self.send_header(
            "Access-Control-Max-Age",
            "86400"
        )
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/api/tx/broadcast":
            return self.send_json({
                "error": "POST endpoint not found"
            }, 404)

        content_type = self.headers.get(
            "Content-Type", ""
        ).split(";", 1)[0].strip().lower()

        if content_type != "application/json":
            return self.send_json({
                "error": "Content-Type must be application/json"
            }, 415)

        try:
            content_length = int(
                self.headers.get("Content-Length", "0")
            )
        except ValueError:
            return self.send_json({
                "error": "invalid Content-Length"
            }, 400)

        if content_length <= 0:
            return self.send_json({
                "error": "empty request body"
            }, 400)

        if content_length > 65536:
            return self.send_json({
                "error": "request body too large"
            }, 413)

        try:
            body = self.rfile.read(content_length)
            payload = json.loads(
                body.decode("utf-8")
            )
        except Exception:
            return self.send_json({
                "error": "invalid JSON"
            }, 400)

        if not isinstance(payload, dict):
            return self.send_json({
                "error": "JSON body must be an object"
            }, 400)

        transaction = payload.get("transaction")

        if not isinstance(transaction, dict):
            return self.send_json({
                "error": "transaction must be an object"
            }, 400)

        required = {
            "expiration",
            "delegate_slate_id",
            "operations",
            "signatures"
        }

        if not required.issubset(transaction):
            return self.send_json({
                "error": "invalid signed transaction structure"
            }, 400)

        if not isinstance(transaction["operations"], list):
            return self.send_json({
                "error": "operations must be an array"
            }, 400)

        if not isinstance(transaction["signatures"], list):
            return self.send_json({
                "error": "signatures must be an array"
            }, 400)

        if not transaction["signatures"]:
            return self.send_json({
                "error": "signed transaction has no signatures"
            }, 400)

        try:
            txid = rpc(
                "network_broadcast_transaction",
                [transaction]
            )
        except Exception:
            return self.send_json({
                "error": "transaction rejected"
            }, 400)

        return self.send_json({
            "status": "broadcast",
            "transaction_id": txid
        }, 200)

    def do_GET(self):
        try:
            path = urlparse(self.path).path

            if path == "/api/status":
                info = rpc("get_info")

                return self.send_json({
                    "network": "PTS Production",
                    "symbol": "PTS",
                    "chain_id":
                        "3a658e5846c3258dfbcfd4df712aa31cff81b25b2800e213fbe64c05c134ec60",
                    "head":
                        info.get("blockchain_head_block_num"),
                    "head_timestamp":
                        info.get("blockchain_head_block_timestamp"),
                    "block_interval": 10,
                    "delegate_count": 101,
                    "delegate_participation":
                        info.get("blockchain_average_delegate_participation"),
                    "connections":
                        info.get("network_num_connections"),
                    "supply_raw":
                        info.get("blockchain_share_supply"),
                    "supply_pts": 176359437.874154
                })

            if path.startswith("/api/block/"):
                height = int(
                    path.rsplit("/", 1)[1]
                )

                block = rpc(
                    "blockchain_get_block",
                    [height]
                )

                block_hash = rpc(
                    "blockchain_get_block_hash",
                    [height]
                )

                return self.send_json({
                    "hash": block_hash,
                    "block": block
                })

            if path.startswith("/api/address/") and path.endswith("/balance"):
                parts = path.strip("/").split("/")

                if len(parts) != 4 or parts[0] != "api" or parts[1] != "address" or parts[3] != "balance":
                    return self.send_json({"error": "invalid address endpoint"}, 400)

                address = parts[2]

                base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

                try:
                    if not address.startswith("PTS"):
                        raise ValueError

                    encoded = address[3:]
                    if not encoded or any(ch not in base58 for ch in encoded):
                        raise ValueError

                    n = 0
                    for ch in encoded:
                        n = n * 58 + base58.index(ch)

                    decoded = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
                    decoded = b"\x00" * (len(encoded) - len(encoded.lstrip("1"))) + decoded

                    if len(decoded) != 24:
                        raise ValueError

                    payload = decoded[:20]
                    checksum = decoded[20:]
                    expected = hashlib.new("ripemd160", payload).digest()[:4]

                    if checksum != expected:
                        raise ValueError

                except (ValueError, TypeError):
                    return self.send_json({"error": "invalid PTS address"}, 400)

                balances = rpc(
                    "blockchain_get_balance_for_key",
                    [address]
                )

                balance_raw = 0

                for item in balances or []:
                    if item.get("asset_id") == 0:
                        balance_raw += int(item.get("amount", 0))

                return self.send_json({
                    "address": address,
                    "symbol": "PTS",
                    "asset_id": 0,
                    "balance_raw": balance_raw,
                    "balance_pts": balance_raw / 1000000.0,
                    "balances": balances
                })

            if path.startswith("/api/tx/"):
                txid = path.rsplit("/", 1)[1]

                tx = rpc(
                    "blockchain_get_transaction",
                    [txid, True]
                )

                return self.send_json({
                    "txid": txid,
                    "transaction": tx
                })

            if path == "/api/latest":
                info = rpc("get_info")

                head = int(
                    info["blockchain_head_block_num"]
                )

                blocks = []

                start = max(1, head - 19)

                for height in range(
                    head,
                    start - 1,
                    -1
                ):
                    block = rpc(
                        "blockchain_get_block",
                        [height]
                    )

                    block_hash = rpc(
                        "blockchain_get_block_hash",
                        [height]
                    )

                    delegate = rpc(
                        "blockchain_get_block_signee",
                        [str(height)]
                    )

                    txids = block.get(
                        "user_transaction_ids",
                        []
                    )

                    blocks.append({
                        "height": height,
                        "hash": block_hash,
                        "delegate": delegate,
                        "timestamp":
                            block.get("timestamp"),
                        "transactions":
                            len(txids)
                    })

                return self.send_json({
                    "network": "PTS Production",
                    "head": head,
                    "blocks": blocks
                })

            if path == "/api/recent-transactions":
                info = rpc("get_info")

                head = int(
                    info["blockchain_head_block_num"]
                )

                transactions = []

                # Scan recent blocks dynamically.
                # No historical lab/test transaction is hardcoded.
                start = max(1, head - 99)

                for height in range(
                    head,
                    start - 1,
                    -1
                ):
                    block = rpc(
                        "blockchain_get_block",
                        [height]
                    )

                    txids = block.get(
                        "user_transaction_ids",
                        []
                    )

                    for txid in txids:
                        try:
                            record = rpc(
                                "blockchain_get_transaction",
                                [txid, True]
                            )
                        except Exception:
                            record = None

                        transactions.append({
                            "txid": txid,
                            "block": height,
                            "timestamp":
                                block.get("timestamp"),
                            "record": record
                        })

                        if len(transactions) >= 20:
                            break

                    if len(transactions) >= 20:
                        break

                return self.send_json({
                    "transactions": transactions
                })

            return self.send_json({
                "service":
                    "PTS Production Explorer API",
                "network":
                    "PTS Production",
                "endpoints": [
                    "/api/status",
                    "/api/latest",
                    "/api/recent-transactions",
                    "/api/block/<height>",
                    "/api/tx/<txid>",
                    "/api/address/<PTS-address>/balance",
                    "/api/tx/broadcast"
                ]
            })

        except Exception:
            return self.send_json({
                "error": "internal API error"
            }, 500)

    def log_message(self, fmt, *args):
        pass


class ThreadedHTTPServer(
    ThreadingMixIn,
    HTTPServer
):
    daemon_threads = True


if __name__ == "__main__":
    server = ThreadedHTTPServer(
        ("0.0.0.0", 18081),
        Handler
    )

    print(
        "PTS Production Explorer API "
        "listening on 0.0.0.0:18081",
        flush=True
    )

    server.serve_forever()
