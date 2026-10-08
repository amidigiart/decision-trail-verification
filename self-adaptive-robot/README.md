# A self-adaptive robot: which twin validated the adaptation, and was it before it ran?

**The question:** when a robot adapts its own behaviour and each adaptation is first checked on a digital twin,
can an independent party later reconstruct and verify:

- what triggered the adaptation;
- **which version of the digital twin** validated it, what it predicted and how uncertain it was;
- what the on-board safety monitor said;
- that the validation happened **before** the adaptation ran;
- who authorised it: the adaptation manager, within its policy, or a safety engineer?

**The scenario.** A collaborative robot cell adapts its speed when the payload changes. The decision structure
is inspired by public descriptions of self-adaptive robotics, where planned adaptations are checked on a digital
twin before execution. **It is not a model of any project, robot or digital twin.** The cell, the contact-force
model, the 150 N limit and all numbers are invented. Only the structure of the evidence is tested.

## The decision rule

- For each plan, two inference records are written:
  - the **digital twin**, whose model hash names the twin version and whose uncertainty grows outside its
    calibrated payload range;
  - the **safety monitor**, which alerts when a person is inside the shared zone.
- The **adaptation manager** may authorise automatically (signed) only if both agree that the plan is safe and
  both uncertainties are 1.0 or less. The policy is itself a record in the chain.
- Otherwise a **safety engineer** decides on a recorded explanation: twin version, both predictions,
  uncertainty, payload and human distance. The engineer signs the approval or the decline.
- After the adaptation runs, the measured peak force of the first cycle is recorded.

## Results

10 seeds, 6 scenarios. Full figures: `results/ROBOT_REPORT.md`; the deterministic data is in
`results/robot_report.json`.

| Recovered afterwards | Controller + twin logs (A) | Trail (B) |
|---|---|---|
| Twin version that validated each adaptation | 0 | all |
| Twin prediction with its uncertainty | 0 | all |
| Validated before execution (provable order) | 0 | all |
| Who authorised | free-text ticket, not verifiable | signature, verifiable |
| Automatic adaptation the twin could not vouch for (rogue manager) | executed 10 times | refused 10 times |
| Attacks on the record: claiming another twin version, deleting the twin validation, an insider authorising outside the policy, relabelling, removing the policy, deleting an explanation | not detectable | 120 of 120 detected |

The baseline assumes the twin logs its runs on its own server, with its own clock and no link to the
adaptation. If your twin already links runs to adaptations, the A column improves; the comparison that matters
is against your system.

**Where the trail does not help** (in the results on purpose): in `sim_to_real_gap` the twin and the monitor are
both confident and both wrong. The adaptation runs and the first cycle exceeds the limit. The trail records this
faithfully and verifies; it does not prevent it. **A record proves what was validated, not that the twin was
right.**

## Verify

Requirements: Python 3.10 or newer, plus `pip install cryptography pqcrypto`. `verify.py` is the same file as
in `../oversight/`; only the data differs.

```
python verify.py samples/cell_trail.json samples/cell_witness.json samples/signer_keys.json
python verify.py samples/tampered_claims_another_twin_version.json samples/cell_witness.json samples/signer_keys.json
python verify.py samples/tampered_insider_automatic_outside_policy.json samples/cell_witness.json samples/signer_keys.json
python verify.py samples/rogue_manager_trail.json samples/rogue_manager_witness.json samples/rogue_manager_signer_keys.json
python verify.py samples/sim_to_real_gap_trail.json samples/sim_to_real_gap_witness.json samples/sim_to_real_gap_signer_keys.json
```

1. The first passes.
2. The second fails. Someone rewrote which twin version validated an adaptation and recomputed every hash;
   the roots already given to the witness expose it.
3. The third fails, and the policy rule names the record: an automatic authorisation the twin and the monitor
   did not both vouch for.
4. The fourth passes, and its trail contains the gate's `refused` record for the rogue attempt.
5. The fifth passes, and its trail shows `"exceeds_limit": true` after a validated adaptation: the known failure.

## Limits

- The cell, force model, limit and numbers are invented; nothing is validated against a real robot or twin.
- The policy gate is a runtime check, tested here; it is **not formally verified**.
- Keys are software keys (Ed25519 + ML-DSA-65 hybrid profile).

`SHA256SUMS.txt` in this folder covers every file in it except itself. Timestamping on the Tezos mainnet is
pending.
