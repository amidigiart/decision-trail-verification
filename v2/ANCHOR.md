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


## Version note (8 October 2026): verifier updated for pqcrypto 1.0

`pqcrypto` 1.0, released after this folder was anchored, changed how ML-DSA verification reports success: it
returns nothing and raises on a bad signature, where earlier versions returned `True` or `False`. With a fresh
`pip install pqcrypto`, the anchored `verify.py` therefore rejected valid hybrid signatures. The signatures and
the data are unchanged; only two lines of `verify.py` that read the library's answer were changed, so it works
with both behaviours.

| | `verify.py` SHA-256 |
|---|---|
| anchored version (git commit `6a008841d94360113b7db9927d63bfbf65ddc2cd`) | `f56d59e742cf08380df7c9c6ff9abbc1a13075df36abfe2868a16351e53ac86b` |
| current version | `c5e30cc39e1e9e9a29f5ccaa3b639ebc64253a5225a824d21f5eda9e93e8db01` |

`SHA256SUMS.txt` now lists the current `verify.py`. The anchored files, including the anchored `verify.py`,
remain retrievable at commit `6a008841d94360113b7db9927d63bfbf65ddc2cd`, and their root still matches the anchor above. The new version will be
timestamped in the next batch.

## Batch 4 (8 October 2026, evening): the current version is timestamped

The current `SHA256SUMS.txt` of this folder (with the updated `verify.py`) is a leaf of batch 4:

| # | Leaf | SHA-256 |
|---|---|---|
| 0 | previous anchored root (batch 3: `oversight/` + `vehicle-forensics/`) | `03a7909ac3197326d8e213209adb9f6197b93b6b9eaec7d674be9b7c0e934973` |
| 1 | `self_adaptive_robot_pack_root` | `80ffed6b0c7445b6444896396acf7f83722857cb2686de13b3f92c2925403724` |
| 2 | `robot_report_json` (`self-adaptive-robot/results/robot_report.json`) | `ab4eb5267309a08599c6364f7a91cb81145542e09aacc0ad901b9a759a431316` |
| 3 | `oversight_pack_root_v3_1` | `53cf03d8a40b03a589086decda21fa7d86304296341fbcb25ba79367b38c2cb3` |
| 4 | `vehicle_forensics_pack_root_v3_1` | `d120e25580702af982876ff87a48f77b06117c1e13f1353552da06d57fcb029d` |
| 5 | `v2_pack_root_pq1` | `5323b0526263f8b79887469fc55da0c49854d68b6be1b62ae70d8cc6a6011fb8` |
| 6 | `verifier_v3_1_py` (`verify.py` in oversight/, vehicle-forensics/, self-adaptive-robot/) | `8ee51b61d39155e239ce37a8ab223937dcfc4298e760a4a1ca9fe69d231a407c` |
| 7 | `verifier_v2_pq1_py` (`v2/verify.py`) | `c5e30cc39e1e9e9a29f5ccaa3b639ebc64253a5225a824d21f5eda9e93e8db01` |
| 8 | `limitations_md` (`LIMITATIONS.md`) | `08ead7cc153044da35c4514a6b1b2caba4ada0c9974c35bd6eb3f4c7692bebf1` |
| 9 | `dssad_note_md` (`notes/vehicle-forensics-vs-DSSAD.md`) | `652150a6348ffc4e5a378f9f7bcff6c53fc56524f3873e25f26c71532ef0bc58` |

| | |
|---|---|
| Batch root | `fc94dbae93af993c5e47ccb533145bd95eafd53e6692e74f704070a0e62438d7` |
| Transaction | [`oo3XFvUjKR6QENmVAkpXtLNyr9ccbR5PqahNakJrjXtispfxXBA`](https://tzkt.io/oo3XFvUjKR6QENmVAkpXtLNyr9ccbR5PqahNakJrjXtispfxXBA) |
| Block | 15288382, 2026-10-08 20:05:10 UTC |
| Contract | `KT1S1YVjwGy4iFcbrN7QgTFY5sdGDhDAMZBV`, entrypoint `anchor_batch` |

Leaf 0 is the root of the previous batch, so all versions form one chain. The batch root uses the same Merkle
scheme as `verify.py` (leaf = SHA-256(0x00 || h), node = SHA-256(0x01 || left || right), an odd node is
promoted unchanged), over leaves 0–9 in the order above.
