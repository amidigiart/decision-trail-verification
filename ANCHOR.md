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

## Batch 4 (8 October 2026, evening): `LIMITATIONS.md` and `notes/`

`LIMITATIONS.md` and `notes/vehicle-forensics-vs-DSSAD.md` were added after the earlier batches and say so in
their first lines. Their exact content is now timestamped as leaves 8 and 9 of batch 4:

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
