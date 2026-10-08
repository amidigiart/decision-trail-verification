# Human oversight you can verify afterwards: wastewater dosing scenario

**The question:** when an AI recommends a process adjustment, sometimes applied automatically and sometimes
decided by a human, can an independent party later reconstruct and verify:

- what the models predicted, and how uncertain they were;
- what explanation the operator saw;
- who decided: the policy engine or the operator;
- whether every automatic decision respected the oversight policy?

**The scenario.** AI-supported carbon dosing for denitrification. The decision structure is inspired by the
public description of AI-supported process control under human oversight in wastewater treatment.
**It is not a model of any real plant.** The process, the sensor, the models and the 8 mg/L limit are
invented. Only the decision structure is tested.

## The decision rule

- Two predictors each declare a prediction and an uncertainty:
  - **M1**, hybrid (physics-informed). Its uncertainty grows outside its training range.
  - **M2**, data-driven and probabilistic. Its uncertainty grows with sensor noise.
- An automatic adjustment, signed by the **policy engine**, is allowed only if both models agree and both
  uncertainties are 1.0 or less.
- Otherwise the **operator** decides. What the operator saw is recorded as an explanation record: both
  predictions, both uncertainties and the main drivers. The operator signs the approval or the decline.
- The policy itself is a record in the chain. The verifier **recomputes** from the inference records
  whether each automatic decision respected it. It does not rely on what the recommendation claims.

## Results

10 seeds, 6 scenarios. Full figures: `results/WASTEWATER_REPORT.md`; the deterministic data is in
`results/wastewater_report.json`.

| Recovered afterwards | Historian baseline | Trail |
|---|---|---|
| Both model outputs, with uncertainty | 0 decisions | all decisions |
| Explanation shown to the operator | not logged | every human decision |
| Who decided | free text, not verifiable | signature, verifiable |
| Automatic action under high uncertainty (rogue policy engine) | executed 10 times | refused 10 times |
| Attacks on the oversight record (insider bypassing the gate, relabelling, removing the policy, deleting an explanation) | not detectable | 80 of 80 detected |

## Verify

Requirements: Python 3.10 or newer, plus `pip install cryptography pqcrypto`.

```
python verify.py samples/plant_trail.json samples/plant_witness.json samples/signer_keys.json
python verify.py samples/tampered_insider_automatic_outside_policy.json samples/plant_witness.json samples/signer_keys.json
python verify.py samples/rogue_engine_trail.json samples/rogue_engine_witness.json samples/rogue_engine_signer_keys.json
```

1. The first command passes.
2. The second fails, and the policy rule names the record: "automatic authorization outside the auto-action policy".
3. The third passes, and its trail contains the gate's `refused` record for the rogue attempt.

## Limits

- The process, models and numbers are invented and have not been validated against plant data.
- "Explanation shown" records what the system displayed, not what the operator understood.
- An operator who signs a poor decision is recorded faithfully. The trail shows who signed, not whether
  they were right.
- Keys are software keys (Ed25519 + ML-DSA-65 hybrid profile). The baseline is our assumption of a
  typical historian; your system is the real baseline.

`SHA256SUMS.txt` in this folder covers every file in it except itself.
