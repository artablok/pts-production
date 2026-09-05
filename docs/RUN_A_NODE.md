# Run a PTS Production node

This guide lets you run an independent read-only node on the PTS Production network.

PTS Production is an independent open-source continuation of the ProtoShares/PTS blockchain technology. It is not presented as the historical public PTS mainnet.

No delegate keys, wallet keys, or public RPC access are required.

## Requirements

- Docker
- x86-64 Linux host
- approximately 2 GB of free disk space
- outbound TCP access to port 39012

## Published Docker images

| Tag | Digest | Notes |
|---|---|---|
| `v1` | `sha256:477c1bf91b3166f0a00cb076be0fe9bcdbbb868131e5e3fce949cccc67c6e05b` | Original release. Immutable — this digest will never change. |
| `v1.1.0` | `sha256:160c66f5d67e73af5f59c1aa6c6760c45d8aefd53e053ad27d3ddb0a2ab94aa4` | Adds `blockchain_get_balance_for_key` RPC method (see [PR #3](https://github.com/artablok/pts-production/pull/3)). Same genesis, additive change only. |

Both tags are immutable and will keep working — pick whichever fits.
New setups should generally use the latest tag (`v1.1.0`) for the
extra RPC method, but `v1` remains fully supported.

Pull either:

    docker pull ghcr.io/artablok/pts-production-node:v1.1.0
    docker pull ghcr.io/artablok/pts-production-node:v1

Both are publicly accessible without GitHub authentication.

## Production genesis

Genesis:

    genesis/production-genesis-v1.json

SHA-256:

    b2c7f3551e0ab1668f2b042f3a65a5df13e8a3243e5ab64cb6a7d909372ba679

PTS Production chain ID:

    3a658e5846c3258dfbcfd4df712aa31cff81b25b2800e213fbe64c05c134ec60

The Docker image contains the Production genesis at:

    /opt/pts/genesis/production-genesis-v1.json

## Public P2P seed

    188.137.177.230:39012

## Start a read-only node

Create persistent storage:

    docker volume create pts-my-node-data

Start the node:

    docker run -d \
      --name pts-my-node \
      --restart unless-stopped \
      --network bridge \
      -v pts-my-node-data:/var/lib/pts \
      --entrypoint /bin/bash \
      ghcr.io/artablok/pts-production-node:v1 \
      -lc 'tail -f /dev/null | /usr/local/bin/pts_client \
        --data-dir /var/lib/pts \
        --genesis-config /opt/pts/genesis/production-genesis-v1.json \
        --disable-default-peers \
        --connect-to 188.137.177.230:39012 \
        --accept-incoming-connections=0 \
        --upnp=0 \
        --min-delegate-connection-count=0'

This configuration does not expose RPC, does not contain private keys,
and does not accept incoming P2P connections.

## Watch synchronization

    docker logs -f pts-my-node

During initial synchronization you should see messages including:

    Attempting to connect to peer 188.137.177.230:39012
    --- there are now 1 active connections to the p2p network
    --- syncing with p2p network, N blocks left to fetch
    --- in sync with p2p network

This clean-node synchronization procedure was tested end-to-end against
the public PTS Production seed using an empty data directory.

## Stop and start

Stop:

    docker stop pts-my-node

Start again:

    docker start pts-my-node

Blockchain data remains in the Docker volume `pts-my-node-data`.

## Remove

Remove the container:

    docker rm -f pts-my-node

Delete its blockchain data if no longer needed:

    docker volume rm pts-my-node-data

## Security

Do not put delegate private keys, wallet private keys, or historical
claim keys on a read-only community node.

RPC is intentionally disabled in this configuration. If RPC is enabled
later, bind it to localhost and protect it with strong unique credentials.

See also:

- [Network endpoints](./NETWORK_ENDPOINTS.md)
- [Become a delegate](./BECOME_A_DELEGATE.md)
