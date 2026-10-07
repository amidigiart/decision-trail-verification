# Timestamp of this pack on Tezos

**The pack root**

`SHA256SUMS.txt` lists the SHA-256 of every file it covers. The Merkle root over those hashes, in the
order listed, is:

```
048d5cc133e37d262027a7dbf686af43a84819ad4a3a94c01a3e83c54a16fc44
```

It uses the same scheme as `verify.py`:

- leaf = SHA-256(0x00 || h)
- node = SHA-256(0x01 || left || right)
- an odd node is promoted unchanged

**The anchored batch**

The pack root is one leaf of a batch anchored on the Tezos mainnet. The leaves, in order:

| # | Leaf | SHA-256 |
|---|---|---|
| 0 | previous anchored root in our chain of states | `8994f917f81182f0c5bd4c347c830e27ad32cf57d331abd28b18e16ef0b36d3c` |
| 1 | `verification_pack_root` | `048d5cc133e37d262027a7dbf686af43a84819ad4a3a94c01a3e83c54a16fc44` |
| 2 | `demonstrator_report_json` (`results/report.json`) | `61fd937e75847f462fa2c13288212600593b57105586e515b65e66c390e5c074` |
| 3 | `verifier_py` (`verify.py`) | `fc7db3d654130abdd5125994d9f0f8d7155903521e137cab2ffa4baab5b53504` |

| | |
|---|---|
| Batch root | `5ef7eccf71cc8101a0aa234e488330ea4045854c02700a17b291c747d45dc61f` |
| Transaction | [`op33sdTSvBD6fu5gCZTCHvy58jgTspQbWpZ1EjRsDjoaCeLAc3B`](https://tzkt.io/op33sdTSvBD6fu5gCZTCHvy58jgTspQbWpZ1EjRsDjoaCeLAc3B) |
| Block | 15274599, 2026-10-07 20:55:10 UTC |
| Contract | `KT1S1YVjwGy4iFcbrN7QgTFY5sdGDhDAMZBV`, entrypoint `anchor_batch` |

**To check**

1. Recompute every hash in `SHA256SUMS.txt`, then the pack root.
2. Recompute the batch root from the four leaves above.
3. Look up the transaction: its parameter must be the batch root.

**What the timestamp proves, and what it does not**

It proves that these files existed in this exact form no later than that block. It does not prove that
the results are correct; checking them is what `verify.py` and the samples are for.

**Why this file is not in `SHA256SUMS.txt`**

It records the root, so it could not be part of it. `.gitattributes` is excluded as well.
