# Timestamp on Tezos (folders `oversight/` and `vehicle-forensics/`, one batch)

**The root of this folder**

`SHA256SUMS.txt` in this folder lists the SHA-256 of every file it covers. The Merkle root over those
hashes, in the order listed, is:

```
8f9c8bac9192ae687a7cfc588a790aac9fed55196a21bf9d4ce1a815f1760be7
```

It uses the same scheme as `verify.py`:

- leaf = SHA-256(0x00 || h)
- node = SHA-256(0x01 || left || right)
- an odd node is promoted unchanged

**The anchored batch**

The two folders were published as `sintef/` and `magic/` and renamed afterwards. The leaf labels below are
the ones anchored on chain; the hashes do not depend on folder names.


The roots of both folders are leaves of one batch anchored on the Tezos mainnet. Leaf 0 is the root of the
version 2 batch (see `../v2/ANCHOR.md`), so all versions form one chain. The leaves, in order:

| # | Leaf | SHA-256 |
|---|---|---|
| 0 | previous anchored root (version 2 batch) | `806567ba79971f6b817e5dfd67da8934838f39410f64c06299810c9854b062f9` |
| 1 | `sintef_pack_root` | `8f9c8bac9192ae687a7cfc588a790aac9fed55196a21bf9d4ce1a815f1760be7` |
| 2 | `wastewater_report_json` (`oversight/results/wastewater_report.json`) | `8aba84ed1d451da121488659e30eb413e33416d30a715f83bc8ebb580d0eba9e` |
| 3 | `magic_pack_root` | `eaafa1dcc6785ba46e0b86a32c32d83fbbe535bd90312c90fdb500c200f57f26` |
| 4 | `vehicle_report_json` (`vehicle-forensics/results/vehicle_report.json`) | `09ead063999c3c1fb407ec91be6e12dd49a163ebbfd8556e5ba412903e995f92` |
| 5 | `verifier_v3_py` (`verify.py`, same file in both folders) | `f0f0ff713b291a1bfed7737d898ddd0dcab9a20cbbbda934f0fd563815061bb0` |

| | |
|---|---|
| Batch root | `03a7909ac3197326d8e213209adb9f6197b93b6b9eaec7d674be9b7c0e934973` |
| Transaction | [`oo7L6ycKQ4SBaBGGmYwgEaUKqaPBpD4gqUvTBWCfHWjGpyFb1x9`](https://tzkt.io/oo7L6ycKQ4SBaBGGmYwgEaUKqaPBpD4gqUvTBWCfHWjGpyFb1x9) |
| Block | 15284036, 2026-10-08 12:48:34 UTC |
| Contract | `KT1S1YVjwGy4iFcbrN7QgTFY5sdGDhDAMZBV`, entrypoint `anchor_batch` |

**What the timestamp proves**

It proves that these files existed in this exact form no later than that block. It does not prove that the
results are correct.

This file records the root, so it is not listed in `SHA256SUMS.txt`.


## Version note (8 October 2026): verifier updated for pqcrypto 1.0

`pqcrypto` 1.0, released after this folder was anchored, changed how ML-DSA verification reports success: it
returns nothing and raises on a bad signature, where earlier versions returned `True` or `False`. With a fresh
`pip install pqcrypto`, the anchored `verify.py` therefore rejected valid hybrid signatures. The signatures and
the data are unchanged; only two lines of `verify.py` that read the library's answer were changed, so it works
with both behaviours.

| | `verify.py` SHA-256 |
|---|---|
| anchored version (git commit `6a008841d94360113b7db9927d63bfbf65ddc2cd`) | `f0f0ff713b291a1bfed7737d898ddd0dcab9a20cbbbda934f0fd563815061bb0` |
| current version | `8ee51b61d39155e239ce37a8ab223937dcfc4298e760a4a1ca9fe69d231a407c` |

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
