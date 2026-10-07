# Decision-trail verification pack

**Can an independent party reconstruct and verify, after the fact, what an AI-assisted system observed,
what each model concluded, and who authorised the response, even when a data source fails, data
arrives late, the network partitions or the models disagree?**

This pack lets you check our answer without trusting us or seeing our source code. It contains:

- the results of a simulation that compares a conventional logging baseline with a verifiable decision trail;
- sample trails from that simulation;
- tampered copies of one sample;
- a small verifier that you can run, read or rewrite in any language.

Author: Mihai Roșca (BRIDGRAI) · October 2026 · status: research demonstrator, not a product

## Verify in two minutes

Requirements: Python 3.10 or newer, plus `pip install cryptography`.

```
python verify.py samples/normal_trail.json samples/normal_witness.json samples/authority_public_key.txt
python verify.py samples/tampered_modify_observation_value.json samples/normal_witness.json samples/authority_public_key.txt
python verify.py samples/tampered_full_rewrite_with_new_checkpoints.json samples/normal_witness.json samples/authority_public_key.txt
```

The first trail verifies (exit code 0). The tampered copies do not (exit code 1), and the verifier names the
failing record or checkpoint. The full rewrite recomputes every hash and every checkpoint consistently. Only
the roots that were already handed to the external witness expose it.

The full specification is the docstring of `verify.py`.

## What was simulated

**The system:**
- one monitored service with three sources (two latency sensors and packet loss);
- two detectors: M1 uses a threshold, M2 an EWMA z-score;
- a recommendation (isolate or restore) that a simulated operator authorises or declines.

**The runs:** 11 scenarios, 10 seeds each. The same event stream is written by two configurations:

| | |
|---|---|
| **A, baseline** | Conventional logging, under the assumptions listed below. |
| **B, decision trail** | Each step is a hash-chained record (observation, inference with model hash and evidence links, disagreement, recommendation, signed authorisation or decline, action, state). Authorisations are single-use, and actions run only through a gate that checks them. Every 32 records a Merkle checkpoint goes to an external witness. A partitioned node keeps a local chain that is merged on reconnection. |

**Baseline assumptions (A):** these are our model of common practice. Your own system is the real baseline.

- telemetry is kept in a time-series store keyed by the sensor timestamp;
- JSON log lines record alerts, actions and state changes, but only for the detector that alerts;
- detectors are named without a version;
- the operator is recorded by name in free text, without a signature;
- a partitioned edge node keeps 16 log lines and 16 points;
- logs are not stored on write-once media.

## Results

The deterministic results are in `results/report.json`; a readable version is in `results/REPORT.md`.

| | A | B |
|---|---|---|
| Inputs the models actually saw, with delayed data | 7 of 28 decisions | 28 of 28 |
| Decision inputs, with missing sensor metadata | 16 of 26 | 26 of 26 |
| Every detector's output, after a model update | 15 of 34 | 34 of 34 |
| Edge data recovered after a partition | 320 of 462 entries | 522 of 522 records |
| Unauthorised action executed (automation script, once per run) | 10 of 10 runs | 0 of 10 |
| 8 tampering attacks × 200 trials: modify, delete, reorder, change model hash, forged authorisation, replayed authorisation, truncation, full rewrite with new checkpoints | not detectable (no integrity mechanism assumed) | 1600 of 1600 detected |

**Where A does as well as B:** under normal conditions, source loss, conflicting sensors and model
disagreement, the baseline reconstructs the decisions as completely as the trail. The difference is in the
disruptions above, in verifiability, and in the gating of actions.

**Overhead** (one laptop, Windows, Python 3.14; see `results/overhead.json`):
- about 18 µs to write a record and 17 µs to verify one;
- storage ×12 raw, ×2.2 after gzip;
- **energy was not measured.**

## Where the layer does not help

These cases are in the results on purpose.

- **All sensors lie.** Both configurations faithfully record a wrong picture. A timestamp proves that a
  record existed and has not changed, not that it was true.
- **The operator key is stolen.** A destructive action signed with the stolen key executes and verifies
  (`samples/stolen_key_trail.json` passes). Only key custody helps, for example a hardware key.
- **A node is destroyed during a partition.** Its local, not-yet-witnessed records are lost with it.
- **The unwitnessed tail.** Records written after the last checkpoint that reached the witness can be
  rewritten consistently. The verifier cannot detect this, but it reports how many records are exposed
  (at most 32 with the current setting).

## What we do not claim

- No immunity to attacks, no autonomous defence and no Byzantine fault tolerance.
- The external witness is a time witness, not a source of truth. In production it is a public ledger;
  in this simulation the witnessed roots are given as a file.
- Signatures are Ed25519, which is not post-quantum. The Merkle scheme uses RFC 6962-style domain separation
  (leaf `0x00`, node `0x01`), but its tree shape differs: an odd node is promoted unchanged.
- The demo authority key is derived from a fixed seed and is used nowhere else.
- This is a simulation, not a measurement on a real network. The comparison that matters is against your
  system, with scenarios you choose.

## Integrity of this pack

`SHA256SUMS.txt` lists the SHA-256 of every file except itself and `.gitattributes`. Its Merkle root will be timestamped on the Tezos
public ledger; until then it is marked as pending.

## Contents

```
verify.py                     the independent verifier (specification in its docstring)
samples/
  authority_public_key.txt    the demo operator's public key
  normal_trail.json           + normal_witness.json       an untampered run
  partition_trail.json        + partition_witness.json    a run with a merged partition
  stolen_key_trail.json       + stolen_key_witness.json   a known failure: verifies despite the theft
  tampered_*.json             one run, tampered three ways (use normal_witness.json)
results/
  report.json                 deterministic results of all scenarios and attacks
  REPORT.md                   readable version
  overhead.json               timings on the machine that produced them
SHA256SUMS.txt
```

Copyright (c) 2026 Mihai Roșca. All rights reserved, except that anyone may run, read and re-implement
`verify.py`, and use the data in this repository, to check the results published here.
