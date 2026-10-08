# Vehicle incident forensics scenario: results

AEB intervention, driver input, over-the-air update, offline period. Not a model of any vehicle or OEM system: signals and numbers are invented; only the evidence structure is tested.

Seeds 0–9, 200 steps per run.

## Baseline assumptions (A)

- an event data recorder keeps the last 25 samples (speed, brake, AEB flag) before the incident
- ECU logs are time-stamped with each ECU's own clock; the OTA log is kept at the backend with backend time
- the software id is logged at the backend when an update is installed, not in the vehicle's event log
- nothing is signed or hash-chained; someone with physical access can edit the vehicle logs

## Questions answered (A baseline / B trail, out of runs)

| Scenario | software_version | sensor_inputs | aeb_recommendation | aeb_actuation_authorized | driver_input | event_order | Edit after the incident detected |
|---|---|---|---|---|---|---|---|
| online_incident | 10 / 10 | 0 / 10 | 10 / 10 | 0 / 10 | 10 / 10 | 10 / 10 | — |
| offline_incident | 10 / 10 | 0 / 10 | 10 / 10 | 0 / 10 | 10 / 10 | 10 / 10 | — |
| ota_before_incident | 0 / 10 | 0 / 10 | 10 / 10 | 0 / 10 | 10 / 10 | 10 / 10 | — |
| clock_skew ≈ | 10 / 10 | 0 / 10 | 10 / 10 | 0 / 10 | 10 / 10 | 10 / 10 | — |
| tamper_after_incident | 10 / 10 | 0 / 10 | 0 / 10 | 0 / 0 | 10 / 0 | 0 / 0 | 0 / 10 |
| version_rollback_claim | 0 / 0 | 0 / 0 | 10 / 0 | 0 / 0 | 10 / 0 | 10 / 0 | 0 / 10 |
| destroyed_before_sync ⚠ | 10 / 0 | 0 / 0 | 10 / 0 | 0 / 0 | 10 / 0 | 10 / 0 | — |

In the two edit scenarios the trail's answers are computed on the edited copy; what matters there is the last column: the edit is detected because the vehicle's checkpoint roots had already reached the witness. The baseline returns the edited answer without any sign of the edit.

## Where the trail does not help

- **clock_skew** (≈): the event data recorder samples on one clock, so the order of events survives the ECU clock skew there too; the trail adds the full sensor context and the signed actuation, not the order.
- **destroyed_before_sync** (⚠): the vehicle's chain was never synced; a crash-hardened event data recorder survives the impact and still answers part of the questions, while the trail answers none.
- Data written while offline is exposed until the vehicle reconnects and its roots reach the witness.
- The trail shows that the safety controller signed the braking; it does not show that the braking was right.
