# Timestamp on Tezos (folder `key-revocation/`)

**The root of this folder**

`SHA256SUMS.txt` in this folder lists the SHA-256 of every file it covers. The Merkle root over those hashes,
in the order listed, is:

```
99f50ed2354f023319e1f057dd463f6447f657e3a7fcf1bc5bf36ed215edb874
```

(The README says timestamping is pending; it was written before this batch, and changing it would change the
anchored hashes. This file, which is not covered by `SHA256SUMS.txt`, records the anchoring.)

**The anchored batch (batch 5)**

| # | Leaf | SHA-256 |
|---|---|---|
| 0 | previous anchored root (batch 4) | `fc94dbae93af993c5e47ccb533145bd95eafd53e6692e74f704070a0e62438d7` |
| 1 | `key_revocation_pack_root` | `99f50ed2354f023319e1f057dd463f6447f657e3a7fcf1bc5bf36ed215edb874` |
| 2 | `verifier_v3_2_py` (`verify.py` in this folder) | `52947de10973d8d7bd2240f6824c9f172a1c9e80ef0472c80337523f3a56e53a` |
| 3 | `delegated_verification_spec_md` (specification of delegated verification and key custody; private repository, as stored in git) | `f806f6eb5d020c806c9fda3e382501ab8dfa4f32d654271c3591df042d4eafc6` |
| 4 | `demonstrator_verifier_py` (private repository, as stored in git) | `7a419500a71e23310b55b2055bdfb526c9616ff6af4f7d94eedc565b0a70665b` |
| 5 | `demonstrator_trail_py` (private repository, as stored in git) | `6aaffdefb93fdbf4bca8c3dd7153a295ccd58ddfec4d11c5d4c9461d22ce79f8` |

| | |
|---|---|
| Batch root | `82e413861cde62c4fdafe6ca7f2d9b203dd7bb366f96c2a6d3a56a4867792855` |
| Transaction | [`ooCk2cT8vUKC5UyYNnAoPPwBMBzS9B2j12Acoafi6dHdvRUBCd6`](https://tzkt.io/ooCk2cT8vUKC5UyYNnAoPPwBMBzS9B2j12Acoafi6dHdvRUBCd6) |
| Block | 15301700, 2026-10-09 18:26:52 UTC |
| Contract | `KT1S1YVjwGy4iFcbrN7QgTFY5sdGDhDAMZBV`, entrypoint `anchor_batch` |

Leaf 0 is the root of batch 4 (see `../self-adaptive-robot/ANCHOR.md`), so all versions form one chain. The batch
root uses the same Merkle scheme as `verify.py` (leaf = SHA-256(0x00 || h), node = SHA-256(0x01 || left || right),
an odd node is promoted unchanged), over leaves 0–5 in the order above. Leaves 3–5 are files that are not
published; their hashes prove they existed in this exact form at this time.
