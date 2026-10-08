# Forensically sound records of a vehicle incident

**The question:** after an incident, can an independent investigator reconstruct and verify:

- which software version was running;
- what the sensors reported;
- what the emergency-braking (AEB) function recommended, and who authorised the actuation;
- what the driver did, and in which order;

even if the vehicle was offline, had just received an over-the-air update, its control units' clocks
disagreed, or someone edited the logs afterwards?

**The scenario.** It is inspired by the public goals of digital forensics for vehicles: forensic soundness,
trustworthy incident investigations, UNECE R155/R156 and ISO/SAE 21434. **It is not a model of any vehicle or
OEM system.** Signals, functions and numbers are invented; only the structure of the evidence is tested.

## What is recorded

- **Over-the-air updates** are authorised with the OEM key (signed) and recorded as a change of software id.
- **The AEB actuation** is authorised by the safety controller (signed), together with the sensor context of
  the decision.
- **Time.** Records use the logging gateway's monotonic clock, and each ECU's own clock is kept in the record.
  The order of events comes from the chain, not from the ECU clocks.
- **While offline**, the vehicle keeps its chain locally. Its checkpoint roots reach the external witness when
  it reconnects.

## Results

10 seeds per scenario. Full table: `results/VEHICLE_REPORT.md`.

| | Event data recorder + logs | Trail |
|---|---|---|
| Software running at the incident, after an OTA update | 0 / 10 | 10 / 10 |
| Sensor context of the AEB decision | 0 / 10 | 10 / 10 |
| Signed authorisation of the actuation | 0 / 10 | 10 / 10 |
| Edit after the incident detected (braking record deleted; software version rewritten) | 0 / 20 | 20 / 20 |

**Where the trail does not help** (both cases are in the results on purpose):

- **ECU clock skew.** The event data recorder samples on one clock, so the order of events survives the skew
  there too.
- **Vehicle destroyed before reconnection.** The trail is lost with it, while a crash-hardened event data
  recorder survives and still answers part of the questions.

## Verify

Requirements: Python 3.10 or newer, plus `pip install cryptography pqcrypto`.

```
python verify.py samples/ota_incident_trail.json samples/ota_incident_witness.json samples/signer_keys.json
python verify.py samples/edited_after_incident_trail.json samples/edited_after_incident_witness.json samples/edited_after_incident_signer_keys.json
```

1. The first command passes. Its trail shows the OEM-signed update before the AEB decision.
2. The second fails. The copy was edited after the incident (the braking record was deleted and the chain
   recomputed), and the vehicle's roots had already reached the witness.

## Limits

- Data written while offline is exposed until the vehicle reconnects.
- The trail shows that the safety controller signed the braking. It does not show that the braking was right.
- The keys are software keys (Ed25519 + ML-DSA-65, hybrid profile). The event data recorder baseline is our
  assumption; a real investigation would compare against the actual vehicle's records.

`SHA256SUMS.txt` in this folder covers every file in it except itself.
