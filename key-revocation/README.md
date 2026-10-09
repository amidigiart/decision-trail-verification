# A stolen key, revoked in the trail: what still verifies, and what no longer can

**The question:** if a signer's key is stolen, can an independent party later see exactly from which point the
key stopped being valid, and catch anything signed with it after that point, even if an insider writes it
straight into the trail and re-witnesses it?

**The answer in this folder:** yes, from the moment the revocation is recorded; **not before**.

## The story in `samples/revocation_trail.json`

1. The key authority is declared in the trail (a `state` record: `"key_authority": "key-admin"`).
2. Normal operation: the operator signs six adjustments.
3. **The thief, holding the stolen operator key, signs `open_bypass_valve`.** Nobody knows yet. This action
   **verifies**: a signature cannot tell who held the key. That is the limit, and it stays.
4. The key authority records a **revocation** (`key_event: revoke`, reason "operator key reported stolen").
5. The thief tries again. The gate **refuses** and records the refusal.
6. The key authority records a **rotation** (`key_event: rotate`): the operator gets new keys. The old ones
   are dead from that record on.
7. Normal operation continues with the new keys.

`signer_keys.json` holds the keys **at the start** of the trail. Every later change is a signed record in the
trail, verified in order, so nobody can swap a key file to rewrite history.

## Rules (in the verifier's docstring, "key events")

- A key event is signed like an authorization, over the hash of what it says (event, subject, new keys,
  reason). Changing any of these after signing breaks the signature.
- **Revoke:** signed by the key authority, or by the key holder itself (someone who lost a token can revoke it).
- **Rotate:** **only** the key authority. A thief cannot give the stolen identity new keys.
- A revoked signer can sign nothing afterwards, not even key events. A revoked key authority can change no keys.
- Every authorization is checked with the keys valid at its position in the chain.

## Verify

Requirements: Python 3.10 or newer, plus `pip install cryptography pqcrypto`.

```
python verify.py samples/revocation_trail.json samples/revocation_witness.json samples/signer_keys.json
python verify.py samples/tampered_revoked_key_written_directly.json samples/tampered_revoked_key_witness.json samples/signer_keys.json
python verify.py samples/tampered_old_key_after_rotation.json samples/tampered_old_key_witness.json samples/signer_keys.json
python verify.py samples/tampered_thief_rotation.json samples/tampered_thief_rotation_witness.json samples/signer_keys.json
python verify.py samples/tampered_revocation_deleted.json samples/revocation_witness.json samples/signer_keys.json
```

1. **Passes.** The thief's action before the revocation is in it and verifies (the limit); the refused attempt
   after it is recorded.
2. **Fails:** "authorization signed with revoked keys". An insider inserted an authorization with the revoked
   key between the revocation and the rotation, recomputed every hash and **re-witnessed** the result. The
   witness is on his side; the key history still catches him.
3. **Fails:** the old key, used after the rotation, no longer matches the keys valid at that point.
4. **Fails:** "'operator' may not rotate the keys of 'operator'". The thief tried to renew the stolen identity.
5. **Fails:** the revocation was deleted after it had been witnessed.

## The verifier

`verify.py` here is **version 3.2** = version 3.1 (the one in `../oversight/`, `../vehicle-forensics/` and
`../self-adaptive-robot/`) plus key events. On every published sample in those folders and in `../v2/` it gives
the same result as their own verifier; the workflow `verify-samples` checks this on Linux, Windows and macOS.
(The samples at the root of the pack use the older v1 format and their own `verify.py`.)

## Limits

- **Before a revocation is recorded, a stolen key works.** Revocation limits the damage from that record on.
- How fast a revocation is signed, and who backs up the key authority, is an organisational procedure, not code.
- The demo keys are software keys derived from fixed seeds; in production they belong on hardware.

`SHA256SUMS.txt` in this folder covers every file in it except itself. Timestamping on the Tezos mainnet is
pending.
