# Timestamp on Tezos (folder `self-adaptive-robot/`)

**The root of this folder**

`SHA256SUMS.txt` in this folder lists the SHA-256 of every file it covers. The Merkle root over those hashes,
in the order listed, is:

```
80ffed6b0c7445b6444896396acf7f83722857cb2686de13b3f92c2925403724
```

(The README says timestamping is pending; it was written before this batch, and changing it would change the
anchored hashes. This file, which is not covered by `SHA256SUMS.txt`, records the anchoring.)

**The anchored batch (batch 4)**

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
