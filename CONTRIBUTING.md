# Contributing to pts-production

This repository hosts the patched PTS v2.0.1 client source and the
production genesis file for the restored network.

## Ways to contribute right now

- **Run a node** — see [`docs/RUN_A_NODE.md`](./docs/RUN_A_NODE.md)
- **Become a delegate** — see [`docs/BECOME_A_DELEGATE.md`](./docs/BECOME_A_DELEGATE.md)
- **Report inconsistencies** — if the genesis checksum, chain ID, or any
  claim in the README doesn't match what you observe on your own node,
  please open an issue. This kind of scrutiny is exactly what a
  bootstrap-stage network needs.
- **Source code changes** — this is a patched historical codebase; any
  proposed changes to consensus-relevant code should reference the
  corresponding patch rationale in
  [pts-historical-restoration/build-patches](https://github.com/artablok/pts-historical-restoration/tree/main/build-patches).

## Security

Do not open a public issue for anything involving a private key,
credential, or vulnerability that could be exploited before it's fixed.
Reach out privately first.
