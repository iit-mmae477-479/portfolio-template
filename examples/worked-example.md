# Worked Example: What Good Portfolio Entries Look Like

*Reference only, do not edit. These examples use a deliberately different
product, a bike-mounted phone holder, so the **form** transfers but the
content cannot be copied. Your entries must be about your design.*

---

## 1. A good project summary (for your root README)

> Designed and validated a handlebar-mounted phone holder for road cycling:
> ≤ 85 g, ≤ $6 in materials, holding a 230 g phone through a 40 g shock load
> (pothole case) with FoS ≥ 2. Explored five clamp concepts, selected a
> two-piece PETG design via weighted criteria, sized the cantilever arm with
> beam analysis, verified in FEA (peak stress within 8% of hand calc), and
> confirmed by instrumented shake test: measured deflection 1.1 mm vs.
> 1.3 mm predicted.

Why it works: every claim is a number, the workflow is visible
(concepts → analysis → FEA → test).

## 2. Good decision-log rows

| # | Date | Decision | Alternatives considered | Criteria used | Evidence | Assumptions still uncertain |
|---|---|---|---|---|---|---|
| 3 | Sep 12 | Two-piece clamshell clamp over cam-lever and zip-tie mounts | cam-lever, zip-tie, one-piece flex clip, suction | tool-free install, print time, failure mode under shock, cost | `02-concepts/pugh-chart.md`: clamshell won 4 of 5 criteria | clamp preload needed to resist rotation is estimated, not measured. Test planned in validation. |
| 5 | Sep 26 | Arm cross-section: 12×6 mm hollow rectangle, 2 mm wall | solid rect, I-beam, circular tube | stress at root ≤ 25 MPa (FoS 2 on PETG yield), printability without supports, mass | `03-structural-analysis/arm-sizing.ipynb`: hollow rect is 31% lighter than solid at same stress | assumes printed layer adhesion is at least 80% of bulk strength per datasheet; not yet verified for our printer |

Why they work: the alternatives are real (not strawmen), the criteria are
stated *before* the winner, the evidence is a link into this repo, and the
last column names exactly what would have to be measured to
close the decision. Note row 5's uncertainty became a validation-test item.

A **bad** row for contrast:

| # | Date | Decision | Alternatives | Criteria | Evidence | Uncertain |
|---|---|---|---|---|---|---|
| — | — | Chose PETG because it's strong and cheap | PLA | strength | — | — |

No numbers, one strawman alternative, no evidence link.

## 3. Mass budget done right (excerpt)

| Subsystem | Component | Mass (g) | Source | Margin held |
|---|---|---|---|---|
| Payload | Phone (Pixel 8, case on) | 231 | measured, lab scale | 0 |
| Structure | Clamp halves (×2) | 24 | estimate, CAD volume × ρ | +20% |
| Structure | Arm | 18 | estimate, CAD volume × ρ | +20% |
| Hardware | M4 bolts + nuts (×4) | 9 | datasheet (McMaster) | 0 |

Change log:

| Date | What changed | Δ (g) | Why |
|---|---|---|---|
| Oct 3 | Clamp halves: estimate → measured print | −4.1 | printed at 25% infill, lighter than CAD solid estimate. Margin released to arm budget. |

Why it works: every mass carries its source. Estimates hold margin; measurements
don't. When an estimate became a measurement, the freed margin was logged and
handed to another part of the budget. That is the budget working correctly.

## 4. Requirements: good vs. bad

| | |
|---|---|
| **Bad** | "The holder should be lightweight and hold the phone securely." |
| **Good** | "R3: Total holder mass ≤ 85 g (verified: lab scale before install). R4: Phone shall not translate > 2 mm under a 3g vertical shock (verified: shake-table test, 13-validation). Traces to: mission need — no rider distraction on rough pavement." |

The test of a requirement: a stranger with your repo and the lab equipment
could determine pass/fail without asking you anything.
