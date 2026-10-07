# VTT pilot A demonstrator: results

Seeds 0–9, 120 steps per run, checkpoint every 32 records. Deterministic part: `report.json`.

## Baseline assumptions (A)

- telemetry kept in a time-series store keyed by the sensor timestamp (no arrival time)
- JSON log lines for alerts, actions and state changes; only the detector that alerts is logged
- detectors are named in logs without a version or hash
- the authorizing operator is recorded by name in free text, without a signature
- a partitioned edge node keeps at most 16 log lines and 16 telemetry points
- no write-once storage and no integrity protection on logs (a WORM store would change tamper results)

## Reconstruction after the event (decisions with the element recovered)

| Scenario | Decisions | Input A / B | Model outputs A / B | Evidence A / B | Authorization verifiable A / B | Unauthorized actions executed A / B |
|---|---|---|---|---|---|---|
| normal | 24 | 24/24 / 24/24 | 24/24 / 24/24 | 24/24 / 24/24 | 0/24 / 24/24 | 10 / 0 |
| source_loss | 25 | 25/25 / 25/25 | 25/25 / 25/25 | 25/25 / 25/25 | 0/25 / 25/25 | 10 / 0 |
| delayed_data | 28 | 7/28 / 28/28 | 17/28 / 28/28 | 7/28 / 28/28 | 0/28 / 28/28 | 10 / 0 |
| conflicting | 28 | 28/28 / 28/28 | 28/28 / 28/28 | 28/28 / 28/28 | 0/28 / 28/28 | 10 / 0 |
| partition | 32 | 32/32 / 32/32 | 32/32 / 32/32 | 32/32 / 32/32 | 0/32 / 32/32 | 10 / 0 |
| model_disagreement | 62 | 62/62 / 62/62 | 62/62 / 62/62 | 62/62 / 62/62 | 0/62 / 62/62 | 10 / 0 |
| corrupted_metadata | 26 | 16/26 / 26/26 | 26/26 / 26/26 | 16/26 / 26/26 | 0/26 / 26/26 | 10 / 0 |
| state_change | 34 | 34/34 / 34/34 | 15/34 / 34/34 | 15/34 / 34/34 | 0/34 / 34/34 | 10 / 0 |
| spoofed_sensors ⚠ | 12 | 12/12 / 12/12 | 12/12 / 12/12 | 12/12 / 12/12 | 0/12 / 12/12 | 10 / 0 |
| stolen_key ⚠ | 29 | 29/29 / 29/29 | 29/29 / 29/29 | 29/29 / 29/29 | 0/29 / 29/29 | 20 / 10 |
| edge_node_lost ⚠ | 31 | 31/31 / 31/31 | 31/31 / 31/31 | 31/31 / 31/31 | 0/31 / 31/31 | 10 / 0 |

## Partition

- **partition**: edge records kept and merged by B: 522/522; edge log lines and points recovered by A: 320/462
- **edge_node_lost**: edge records kept and merged by B: 0/520; edge log lines and points recovered by A: 0/460

## Tampering, checked by the independent verifier (B)

| Attack | Detected |
|---|---|
| modify_observation_value | 200/200 |
| delete_record | 200/200 |
| reorder_records | 200/200 |
| change_model_hash | 200/200 |
| forge_authorization | 200/200 |
| replay_authorization | 200/200 |
| truncate_end | 200/200 |
| full_rewrite_with_new_checkpoints | 200/200 |
| rewrite of the unwitnessed tail ⚠ | 0/200 (verifier reports 10 unwitnessed records) |

A: not run: the baseline as assumed has no integrity mechanism, so none of these edits is detectable by construction (a write-once store would change this for deletion and edits).

## Where the layer does not help (⚠)

- **spoofed_sensors**: every source lies: both configurations faithfully record a wrong picture; a timestamp proves a record existed, not that it was true
- **stolen_key**: a valid signature from a stolen key is indistinguishable from the operator's: the destructive action is executed and verifies; only key custody (hardware) helps
- **edge_node_lost**: a node destroyed during a partition takes its unwitnessed local records with it
- **unwitnessed tail**: records written after the last checkpoint that reached the witness can be rewritten consistently; the verifier cannot detect it, but reports how many records are exposed (at most 32 with the current setting).

## Overhead (this machine: Windows AMD64 / Python 3.14.3; not part of the deterministic report)

- append: median 17.85 µs per record
- independent verification: median 17.35 µs per record
- storage for one run: A 20717 B, B 256957 B (×12.4); gzip: A 17645 B, B 39160 B (×2.22); A counts log lines plus 48 bytes per time-series point (an assumption); B is the canonical JSON of every record, uncompressed
- energy: not measured (no energy counter available on this machine); to be measured on VTT hardware
