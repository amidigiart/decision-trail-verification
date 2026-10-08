# Limitations, in one place

*Added 8 October 2026. This file gathers the limits already stated in each folder's README and results; it adds
no new claim. It is not part of any anchored set.*

The trail proves that a record **existed** at a given point and **has not been changed** since. It does not prove
that the record was **true**, that a decision was **right**, or that anything was **prevented**.

## What the trail does not catch

| Case | What happens | Where it is shown |
|---|---|---|
| **Sensors lie** | Both the baseline and the trail faithfully record a wrong picture. | root README |
| **The node that writes the trail is compromised** | It can write false records, signed with its own key; they verify. Same class as lying sensors. | (follows from the above) |
| **An operator key is stolen** | A destructive action signed with the stolen key executes and verifies. Only key custody (e.g. a hardware key) helps. | `samples/stolen_key_trail.json` passes |
| **The digital twin is confident and wrong** | The adaptation runs and exceeds the limit; the trail records it faithfully and verifies. | `self-adaptive-robot/`, `sim_to_real_gap` |
| **An operator signs a poor decision** | Recorded faithfully: who signed, not whether it was wise. | `oversight/` |
| **"Explanation shown"** | Records what the system displayed, not what the operator understood. | `oversight/` |

## What the trail cannot protect

| Case | What happens | Where it is shown |
|---|---|---|
| **The unwitnessed tail** | Records written after the last checkpoint that reached the witness can be rewritten consistently. The verifier reports how many (at most 32 with the current setting); it cannot detect the rewrite. | root README |
| **A node destroyed during a partition / a vehicle destroyed before it reconnects** | Its local, not-yet-witnessed records are lost. A crash-hardened event data recorder survives; our trail does not. | root README, `vehicle-forensics/` |
| **An edit made while offline, before any checkpoint reached the witness** | Not detectable this way. | `notes/vehicle-forensics-vs-DSSAD.md` |

## What we do not claim

- No immunity to attacks, no autonomous defence, **no Byzantine fault tolerance**.
- The external witness is a **time witness**, not a source of truth. In the samples, the witnessed roots are
  given as a file; in production they are on a public ledger.
- The policy gate is a **runtime check, tested, not formally verified**.
- We do not tell lost communication from an attack: the trail records the gap, it is not an intrusion detector.
- **Energy** was not measured.
- Every scenario is a **simulation** with invented processes and numbers. Nothing is validated against a real
  plant, vehicle, robot or digital twin, and none is a model of any named project or company.
- The baselines (A) are our assumptions about common practice. **Your system is the real baseline.**
- The trail is not designed for minimal disclosure; how to erase personal data while keeping the chain
  verifiable is an open question.
- The producing code is proprietary. Only the verifier, the samples and the results are public.
