# The vehicle-forensics scenario compared with DSSAD

*Added 8 October 2026, after a reader suggested the comparison. This note is not part of any anchored set; the
anchored files in [`../vehicle-forensics/`](../vehicle-forensics/) are unchanged.*

**DSSAD** (Data Storage System for Automated Driving) is the recorder required for automated lane keeping
systems by UN Regulation No 157. The text used here is **paragraph 8 of UN R157 in its original version**, as
published in the Official Journal of the EU ([Regulation 2021/389](https://eur-lex.europa.eu/eli/reg/2021/389/oj/eng)).
Later amendments may have changed details.

**IEEE 1616.1-2023** (DSSAD) was **not read**: its text is not public. Public descriptions say it covers the data
set and a lockout of the diagnostic port against manipulation of EDR and DSSAD data. Nothing below relies on it.

## In one sentence

DSSAD defines **what** the vehicle must record and requires that the stored data be **protected** against
manipulation. Our scenario tests whether, **after the data leaves the vehicle**, an independent party can
**check** that nothing was edited, without trusting the manufacturer or us. The two fit together; neither
replaces the other.

## Paragraph by paragraph

| UN R157 §8 | What it requires | Our scenario |
|---|---|---|
| 8.2.1 (a)–(d) | Activation, deactivation by driver override, transition demand, reduction of driver input | **Not modelled.** The scenario is emergency braking, not lane keeping. Driver brake and steering are recorded, but no system hand-over. |
| 8.2.1 (e) | Start of emergency manoeuvre | **Tested.** The braking actuation is a record signed by the safety controller and linked to the AEB inference it acted on. |
| 8.2.1 (f) | End of emergency manoeuvre | Not modelled. |
| 8.2.1 (g)–(h) | EDR trigger input; involved in a detected collision | Recorded as the incident ("contact") record in the chain. |
| 8.2.1 (i)–(k) | Minimum risk manoeuvre; severe system or vehicle failure | Not modelled. |
| 8.3.1 | Occurrence flag, reason, date, time stamp to 1 s (accuracy ±1 s) | Each record has a kind, a body and the gateway time; the ECU's own clock is kept in the body. The reason is the hash of the inference the action used. **Not tested:** the UTC date and time format. |
| 8.3.2 | The software version present at the time of each event shall be clearly identifiable | **Tested, and the clearest match.** The over-the-air update is signed by the OEM key and recorded in the chain; the inference carries the software id. After an update shortly before the incident, the version at the incident is recovered **10/10** against **0/10** for the logs-plus-recorder baseline, where the update is reported by the backend late. |
| 8.3.3 | Events with the same time stamp must show their chronological order | The chain itself gives a total order. ECU clocks are kept but not used for ordering. With a 3 s ECU skew we show **no advantage**: a recorder with one clock also keeps the order. |
| 8.4.2 | When storage is full, overwrite first in, first out | **Not implemented.** A hash chain cut this way needs the dropped part's witnessed checkpoints kept and the cut itself recorded. |
| 8.4.3 | Data retrievable after a severe impact and without main power | **Our weak point, reported on purpose.** If the vehicle is destroyed before reconnecting, our trail is lost; a crash-hardened recorder survives. |
| 8.4.4–8.4.5 | Readable through a standard interface (OBD) | Out of scope. |
| 8.5.1 | "Adequate protection against manipulation (e.g. data erasure) of stored data such as anti-tampering design" | **Our main contribution.** R157 asks for protection but does not say how anyone outside can check it. In our scenario, edits after the incident (the braking record deleted; the software version rewritten) are detected **20/20** against **0/20**, by a verifier that needs neither our code nor our trust. **Limit:** an edit made while the vehicle is still offline, before any checkpoint reaches the witness, is not detectable this way. |
| 8.6.1 | DSSAD reports that it is operational | Not modelled. |

## How they could work together

1. The vehicle keeps a DSSAD (or EDR) as required: crash-hardened, readable through the standard interface.
2. Each DSSAD occurrence is also written as a record in a hash chain, signed by the unit that caused it
   (e.g. the safety controller for an emergency manoeuvre, the OEM for a software update).
3. When the vehicle is online, the chain's checkpoint roots go to an external witness.
4. After an incident, the investigator reads the DSSAD and the chain and checks with an independent verifier
   that both say the same thing and that neither was edited after the roots were witnessed.

This is a design proposal, not something we have tested on a real vehicle or against a real DSSAD.

## What we did not do

- We did not read IEEE 1616.1-2023 or any later amendment of UN R157.
- We did not model an automated lane keeping system, its hand-over to the driver, or a real time base.
- Signals and numbers in the scenario are invented; only the structure of the evidence is tested.
