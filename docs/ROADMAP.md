# Roadmap toward decentralization

Honest snapshot: right now, one operator holds all 101 delegate private
keys and runs both live nodes on the same infrastructure. This is a
real centralization risk. Here's the concrete path away from it —
tracked here, not just promised.

## Done

- [x] Historical genesis restored and verified 1:1 (see
      [pts-historical-restoration](https://github.com/artablok/pts-historical-restoration))
- [x] Independent wallet implementation, cross-validated against native
      consensus (pts-wallet-core)
- [x] Public P2P seed node reachable externally
- [x] Read-only node-joining guide published ([`RUN_A_NODE.md`](./RUN_A_NODE.md))
- [x] Delegate recruitment process published ([`BECOME_A_DELEGATE.md`](./BECOME_A_DELEGATE.md))
- [x] Added `blockchain_get_balance_for_key` RPC method — look up balances
      by owner address directly, without needing the balance_id (see
      [PR #3](https://github.com/artablok/pts-production/pull/3))

## In progress

- [ ] Public Docker image (so node operators don't rebuild a 2014-era
      C++ toolchain themselves)
- [ ] First external node operators syncing independently
- [ ] First delegate key handed off to a community-run node

## Planned

- [ ] Multiple independent delegate operators across different
      infrastructure/providers
- [ ] Independent technical review by people outside this project
- [ ] Multi-signature or distributed custody for any remaining
      operator-held keys

## How to help

- Run a read-only node: [`RUN_A_NODE.md`](./RUN_A_NODE.md)
- Apply to become a delegate: [`BECOME_A_DELEGATE.md`](./BECOME_A_DELEGATE.md)
- Open an issue with questions, concerns, or things that don't add up —
  that's exactly the kind of scrutiny this project needs
