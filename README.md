# PTS Production

**PTS is an independent open-source continuation of the ProtoShares/PTS
blockchain technology.**

This is **not** the historical public PTS mainnet, and it does **not**
claim ownership over or continuity with the original 2013-2014
development team. It is a from-source restoration of the historical
PTS v2.0.1 client, running with the original genesis balances preserved
1:1, currently in its **bootstrap stage** — actively working toward
decentralization, not there yet.

For the full research/evidence trail (how the genesis was traced,
verified, and reconstructed), see
[artablok/pts-historical-restoration](https://github.com/artablok/pts-historical-restoration).

For the independent, non-custodial wallet implementation, see
[artablok/pts-wallet-core](https://github.com/artablok/pts-wallet-core)
(private — request access for research/verification).

## Current status

- **Network:** PTS Production
- **Chain ID:** `3a658e5846c3258dfbcfd4df712aa31cff81b25b2800e213fbe64c05c134ec60`
- **Genesis SHA-256:** `b2c7f3551e0ab1668f2b042f3a65a5df13e8a3243e5ab64cb6a7d909372ba679`
- **Block interval:** 10 seconds
- **Delegates:** 101
- **Genesis supply:** 176,359,437.874154 PTS (preserved 1:1 from historical balances)
- **Live explorer:** [explorer.ptscrypto.com](https://explorer.ptscrypto.com)

### Honest infrastructure status (as of 2026-09-04)

- 2 nodes, both currently operated by the same person
- **All 101 delegate private keys are currently held by a single
  operator** — this is a real centralization risk, not hidden here
- 100% delegate participation reflects one operator's uptime right now,
  not independent participation yet
- Public P2P seed is live and externally reachable — see
  [`docs/NETWORK_ENDPOINTS.md`](./docs/NETWORK_ENDPOINTS.md)

See [`docs/ROADMAP.md`](./docs/ROADMAP.md) for the path toward genuine
decentralization, including how to run your own node or apply to become
a delegate.

## Contents

| Path | What it is |
|---|---|
| `source/` | The PTS v2.0.1 client source, patched to build on a modern toolchain (see [pts-historical-restoration/build-patches](https://github.com/artablok/pts-historical-restoration/tree/main/build-patches) for what changed and why) |
| `genesis/production-genesis-v1.json` | The genesis file this network runs, preserving historical balances 1:1 |
| `genesis/production-genesis-v1.json.sha256` | Checksum — verify before trusting |
| `docs/RUN_A_NODE.md` | Sync and independently verify the chain yourself, no delegate key needed |
| `docs/NETWORK_ENDPOINTS.md` | Current public seed node address |
| `docs/BECOME_A_DELEGATE.md` | Process for taking over one of the 101 delegate keys |
| `docs/ROADMAP.md` | Path to decentralization |

## RPC methods added beyond the historical client

- `blockchain_get_balance_for_key` — returns balances owned by a given
  address, grouped by asset. Complements the original
  `blockchain_get_balance` (lookup by balance_id) and
  `blockchain_list_balances`. Added in
  [PR #3](https://github.com/artablok/pts-production/pull/3).

## License

MIT (matching the original BitShares/PTS toolkit license)
