# Become a delegate node operator

We're distributing control of block production away from a single
operator. This is a real handoff of a delegate private key, not a
symbolic gesture — so there's a lightweight process, not a form-fill.

## What a delegate does

Runs `pts_client` with `--server` and a delegate key unlocked, producing
blocks on its assigned rotation slot (every ~1010 seconds per delegate,
at 101 delegates × 10s block interval). No token purchase, no fee — this
is infrastructure participation, not an investment product.

## Requirements

- A server with reliable uptime (VPS is fine) reachable on a P2P port
- Comfort running Docker and reading logs
- Willingness to keep the node online — missed blocks are visible
  on-chain (`blockchain_get_delegate_slot_records`) and public

## Process

1. **Run a read-only node first** — follow
   [`RUN_A_NODE.md`](./RUN_A_NODE.md) and get it syncing. This proves
   you can operate the software before you're trusted with a key.
2. **Open an issue** in this repo titled `Delegate application:
   <your-name-or-handle>` with:
   - Confirmation your read-only node is synced (post your head block
     height and hash)
   - Where you'll run it (region/provider is enough, no need for exact
     IP publicly)
   - Any BitShares-era history/handle, if relevant (not required)
3. **Key handoff** — once reviewed, we'll coordinate a private,
   encrypted key exchange (never posted anywhere in git history or
   issues). You'll receive one of the currently operator-held
   `delegateNNN` keys.
4. **Enable production** — `wallet_import_private_key` your key, then
   `wallet_delegate_set_block_production <name> true`. Blocks you
   produce are publicly attributed to you on-chain from that point.

## Why this matters

Every key handed off is one less key under single-operator control.
The goal is zero single points of failure — not overnight, but visibly
moving in that direction with each handoff, tracked openly in this
repo's issue history.
