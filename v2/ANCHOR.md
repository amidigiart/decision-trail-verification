# Timestamp of version 2 on Tezos

**The v2 root**

`SHA256SUMS.txt` in this folder lists the SHA-256 of every file it covers. The Merkle root over those
hashes, in the order listed, is:

```
ebe5e87dc7099c07daa487000abe5fef24a04d92660a9df0b1a04ced521f682d
```

It uses the same scheme as `verify.py`:

- leaf = SHA-256(0x00 || h)
- node = SHA-256(0x01 || left || right)
- an odd node is promoted unchanged

**The anchored batch**

The v2 root is one leaf of a batch anchored on the Tezos mainnet. Leaf 0 is the root of the batch that
anchored version 1 (see `../ANCHOR.md`), so the two versions form a chain. The leaves, in order:

| # | Leaf | SHA-256 |
|---|---|---|
| 0 | previous anchored root (version 1 batch) | `5ef7eccf71cc8101a0aa234e488330ea4045854c02700a17b291c747d45dc61f` |
| 1 | `verification_pack_v2_root` | `ebe5e87dc7099c07daa487000abe5fef24a04d92660a9df0b1a04ced521f682d` |
| 2 | `demonstrator_v2_report_json` (`results/report.json`) | `2f2dc429fded85c4eea26c554edf172e909da301fdf18048a655f3ba5c07106c` |
| 3 | `verifier_v2_py` (`verify.py`) | `f56d59e742cf08380df7c9c6ff9abbc1a13075df36abfe2868a16351e53ac86b` |

| | |
|---|---|
| Batch root | `806567ba79971f6b817e5dfd67da8934838f39410f64c06299810c9854b062f9` |
| Transaction | [`opZcUH45VPbhonMPNTpd8bRHGWxEiGZ4sFtY2CKkm2wR2oGPnAn`](https://tzkt.io/opZcUH45VPbhonMPNTpd8bRHGWxEiGZ4sFtY2CKkm2wR2oGPnAn) |
| Block | 15282831, 2026-10-08 10:44:43 UTC |
| Contract | `KT1S1YVjwGy4iFcbrN7QgTFY5sdGDhDAMZBV`, entrypoint `anchor_batch` |

**What the timestamp proves**

It proves that these files existed in this exact form no later than that block. It does not prove that
the results are correct.

This file records the root, so it is not listed in `SHA256SUMS.txt`.
