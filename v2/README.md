# Version 2: crypto-agility and post-quantum hybrid signatures

The decision trail and its verifier are the same as in version 1 (one folder up); this version adds the
following.

- **Algorithm profiles.** Every trail names its algorithms. The verifier refuses unknown, relabelled or
  non-accepted profiles.
- **`v2-hybrid`.** Each authorisation is signed with both Ed25519 and ML-DSA-65 (FIPS 204), and both
  signatures must verify. The list of algorithms is part of the signed message, so removing the
  post-quantum signature breaks the classic one.
- **Time order.** A record cannot claim an earlier time than the record before it.

## Trust now, forge later

Suppose a quantum computer gives an attacker the operator's Ed25519 key (Shor's algorithm), but not the
ML-DSA-65 key. The table shows how many forgery attempts the verifier detected:

| Forgery | `v1-classic` (Ed25519 only) | `v2-hybrid` |
|---|---|---|
| Inserted into the already-witnessed past | 200 / 200 detected | 200 / 200 detected |
| Appended now with a past time | 200 / 200 detected | 200 / 200 detected |
| Appended now | **0 / 200 detected** | 200 / 200 detected |

The witnessed past is protected by hash functions alone, which Shor's algorithm does not break. A new
forgery is stopped only by the hybrid signature.

## Verify

Requirements: Python 3.10 or newer, plus `pip install cryptography pqcrypto`.

```
python verify.py samples/hybrid_trail.json samples/hybrid_witness.json samples/hybrid_authority_keys.json
python verify.py samples/hybrid_quantum_forgery_appended_now.json samples/hybrid_witness.json samples/hybrid_authority_keys.json
python verify.py samples/classic_quantum_forgery_appended_now.json samples/classic_witness.json samples/classic_authority_keys.json
```

1. The first command passes.
2. The second fails, with the message "ml-dsa-65 signature does not verify".
3. The third **passes**. That is the expected weakness of a classic-only profile, and the reason for v2.

## Cost

Measured on one laptop; see `results/overhead.json`.

| | Signature size | Sign | Verify |
|---|---|---|---|
| ML-DSA-65 | 3309 bytes | ≈ 0.74 ms | ≈ 0.22 ms |
| Ed25519 | 64 bytes | ≈ 0.05 ms | ≈ 0.13 ms |

Storage after gzip is ×2.9 the baseline, compared with ×2.2 for version 1.

## Not claimed

- The demo keys are software keys. The ML-DSA keys are generated at random, so the sample trails differ
  from run to run, while `results/report.json` stays deterministic.
- ML-DSA comes from the PQClean implementation (`pqcrypto` 0.4.0). It is not a certified module.
- The hybrid profile protects authorisations. The hashes (SHA-256) and the external witness are unchanged.
- The public ledger used as a witness signs with classic algorithms. Its own post-quantum migration is
  the ledger's concern. Our roots can be re-anchored, as with the hash-tree renewal of RFC 4998 evidence
  records.

`SHA256SUMS.txt` in this folder covers every file in it except itself.
