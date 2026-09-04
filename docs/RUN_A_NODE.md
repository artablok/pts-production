# Run a node — join the restored PTS network

This lets you sync a full copy of the restored PTS chain and verify it
yourself. **No delegate keys required** — this is a read-only participant
node. You'll be independently downloading and validating every block,
not trusting our word for it.

## What this does

- Builds the same historical `pts_client` binary used by the network
  from the source in this repo
- Syncs the full chain from genesis by connecting to the public seed
- Lets you run any read query yourself against **your own copy** of the
  chain, not ours

## Requirements

- Docker
- ~2GB disk space
- A few minutes for initial sync

## Quick start

```bash
git clone https://github.com/artablok/pts-production.git
cd pts-production

# verify the genesis file before trusting it
sha256sum -c genesis/production-genesis-v1.json.sha256

docker build -t pts-node-join -f docker/Dockerfile .

docker run -d \
  --name pts-my-node \
  --restart unless-stopped \
  -v pts-my-node-data:/pts-data \
  -v "$(pwd)/genesis:/pts-genesis:ro" \
  -p 127.0.0.1:19990:19990 \
  pts-node-join \
  /pts-build/programs/client/pts_client \
    --data-dir /pts-data \
    --genesis-config /pts-genesis/production-genesis-v1.json \
    --disable-default-peers \
    --connect-to 188.137.177.230:39012 \
    --accept-incoming-connections=0 \
    --server \
    --rpcuser localuser \
    --rpcpassword "$(openssl rand -hex 16)" \
    --rpcport 19990
```

## Verify you're actually syncing independently

```bash
docker logs -f pts-my-node
```

You should see `Successfully pushed block N` messages advancing. Once
synced, compare your own head block to the public explorer
(explorer.ptscrypto.com) **using your own node**, not by trusting us:

```bash
docker exec pts-my-node curl -s -u localuser:YOUR_PASSWORD \
  -d '{"method":"blockchain_get_block_count","params":[],"id":1}' \
  http://127.0.0.1:19990/rpc
```

## Why run a node

- Independent verification that the genesis and chain state match what's
  claimed — no need to trust the explorer or us
- More independent nodes means less centralization risk for the network
- If you want to help produce blocks, see
  [`BECOME_A_DELEGATE.md`](./BECOME_A_DELEGATE.md)
