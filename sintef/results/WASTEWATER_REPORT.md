# Wastewater oversight scenario: results

wastewater denitrification, AI-supported carbon dosing under an oversight policy. Not a model of Veas or any real plant: process and numbers are invented; only the decision structure is tested.

Seeds 0–9, 240 steps per run, limit 8.0 mg/L, automatic action allowed only if the models agree and both uncertainties ≤ 1.0.

## Baseline assumptions (A)

- a SCADA historian keeps sensor values, alarms and setpoint changes
- one model prediction is logged per step, without uncertainty and without model version
- the operator is named in free text; no signature
- dismissed recommendations and the explanation shown to the operator are not logged
- no write-once storage; an engine that sets a setpoint directly is not stopped by the historian

## Decision context recovered afterwards (A historian / B trail)

| Scenario | Decisions (human / automatic) | Model outputs | Uncertainty | Explanation shown | Who decided | Automatic action under high uncertainty |
|---|---|---|---|---|---|---|
| normal | 20 (10 / 10) | 0 / 20 | 0 / 20 | 10 / 20 | 20 / 20 | 0 / 0 |
| degraded_sensor | 27 (13 / 14) | 0 / 27 | 0 / 27 | 14 / 27 | 26 / 27 | 0 / 0 |
| novel_load | 83 (64 / 19) | 0 / 83 | 0 / 83 | 19 / 83 | 80 / 83 | 0 / 0 |
| model_disagreement | 50 (40 / 10) | 0 / 50 | 0 / 50 | 10 / 50 | 20 / 50 | 0 / 0 |
| model_update | 24 (12 / 12) | 0 / 24 | 0 / 24 | 12 / 24 | 24 / 24 | 0 / 0 |
| rogue_policy_engine | 106 (84 / 22) | 0 / 106 | 0 / 106 | 22 / 106 | 106 / 106 | 10 / 0 |

In A, 'who decided' comes from free text and cannot be verified; in B it is a signature by the operator or by the policy engine, and the verifier recomputes whether an automatic decision respected the policy.

## Attacks on the oversight record (B, independent verifier)

| Attack | Detected |
|---|---|
| insider_automatic_authorization_outside_policy | 20/20 |
| relabel_human_decision_as_automatic | 20/20 |
| remove_the_policy_record | 20/20 |
| delete_the_explanation_shown | 20/20 |

## Limits

- The process, sensor, models and limit are invented; this is not Veas and not validated against plant data.
- 'Explanation shown' records what the system displayed, not what the operator understood.
- An insider with the operator's own keys can still sign a bad human decision; the record shows who signed, not whether the decision was wise.
