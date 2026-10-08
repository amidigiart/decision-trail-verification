# Self-adaptive robot scenario: results

collaborative robot cell that adapts its own speed; each adaptation validated on a digital twin. Not a model of any project, robot or digital twin: the cell, force model and numbers are invented; only the structure of the evidence is tested.

Seeds 0–9, 200 steps per run, contact-force limit 150.0 N (invented). An automatic adaptation is allowed only if the twin and the safety monitor agree that the plan is safe and both uncertainties are ≤ 1.0.

## Baseline assumptions (A)

- the robot controller logs each adaptation (new speed scale) with controller time
- the digital twin logs its simulation runs on its own server, with its own clock and no adaptation id
- the safety monitor raises alarms but its estimate is not stored with the adaptation
- the safety engineer's approval is a ticket in free text; no signature
- nothing is signed or hash-chained; an adaptation manager that writes a new speed directly is not stopped

## Adaptation context recovered afterwards (A logs / B trail)

| Scenario | Decisions (engineer / automatic) | Twin version | Twin prediction + uncertainty | Validated before execution | Who authorised | Unvalidated automatic adaptation | Limit exceeded after validation |
|---|---|---|---|---|---|---|---|
| normal | 30 (0 / 30) | 0 / 30 | 0 / 30 | 0 / 30 | 30 / 30 | 0 / 0 | 0 / 0 |
| novel_payload | 30 (10 / 20) | 0 / 30 | 0 / 30 | 0 / 30 | 30 / 30 | 0 / 0 | 0 / 0 |
| human_in_zone | 40 (10 / 30) | 0 / 40 | 0 / 40 | 0 / 40 | 30 / 40 | 0 / 0 | 0 / 0 |
| twin_recalibrated | 30 (0 / 30) | 0 / 30 | 0 / 30 | 0 / 30 | 30 / 30 | 0 / 0 | 0 / 0 |
| rogue_adaptation_manager | 30 (10 / 20) | 0 / 30 | 0 / 30 | 0 / 30 | 30 / 30 | 10 / 0 | 0 / 0 |
| sim_to_real_gap | 30 (0 / 30) | 0 / 30 | 0 / 30 | 0 / 30 | 30 / 30 | 0 / 0 | 10 / 10 |

In A, 'who authorised' comes from a free-text ticket and cannot be verified; in B it is a signature by the safety engineer or by the adaptation manager, and the verifier recomputes whether an automatic adaptation respected the policy.

## Attacks on the adaptation record (B, independent verifier)

| Attack | Detected |
|---|---|
| insider_automatic_authorization_outside_policy | 20/20 |
| relabel_engineer_decision_as_automatic | 20/20 |
| remove_the_policy_record | 20/20 |
| delete_the_explanation_shown | 20/20 |
| claim_a_different_twin_version | 20/20 |
| delete_the_twin_validation | 20/20 |

## Limits

- **sim_to_real_gap** is a failure on purpose: the twin and the monitor are both confident and both wrong, the adaptation runs, and the first cycle exceeds the limit. The trail records it faithfully; it does not prevent it. A record proves what was validated, not that the twin was right.
- The cell, force model, limit and numbers are invented; nothing is validated against a real robot.
- The policy gate is a runtime check, tested here; it is not formally verified.
- The baseline is our assumption of separate controller and twin logs; your system is the real baseline.
