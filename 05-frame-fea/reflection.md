# Reflection — the whole frame in FEA

## Carried forward

- Arm design used in your frame (plate or tube) and material:
- P = T_hover, from `01` (gf, and N):
- P_max = your motor's max thrust at full throttle, from `01` (gf, and N):
- E, from `04` (GPa):
- I for your arm's cross-section (mm^4):

## Strength

- Strength value (MPa), and which kind (yield for aluminum, tensile for CF):
- Source (link or citation):
- Converted to gf/mm^2 (MPa x 101.97):

## Checking the model (Step 1)

- Frame mass from your CAD model (g):
- FEA software used:
- Material assigned in the software (exact match, or closest substitute — say
  which):
- How that compares to the 100 g assumed in `01`:
- If different: what W and T_hover would become with your actual frame
  mass:
- L_cad, arm length in your model, body to motor-mount center (mm):
- y_hand_Lcad = P L_cad^3 / (3 E I) (mm):

## Hover setup (Step 2)

- What region you fixed (which faces, roughly how big), and why that's a
  reasonable stand-in for a vehicle in flight:
- How you applied the four loads (confirm: four separate Force loads):
- Part or assembly? If assembly, what does the default "bonded" contact
  assume about your joints?

## Frame vs. beam (Steps 3–4)

- Where the maximum von Mises stress is, in words:
- Arm tip deflection, probed at the motor mount (mm):
- % difference from y_hand_Lcad:
- Mid-length arm stress (von Mises for aluminum, 1st principal for CF) —
  FEA (MPa and gf/mm^2) vs. beam theory, M c / I
  with M = P L_cad / 2 (gf/mm^2):
- Why does the frame deflect more (or not) than the `04` beam? What did
  `04`'s model assume about the root that this one doesn't?

## Sharp vs. filleted corner (Step 5)

- How you refined the mesh (smaller Average Element Size, Local Mesh
  Control, or your software's equivalent):
- Which stress you tracked (von Mises for aluminum, 1st principal for CF):
- Where the highest stress was in the sharp version, and in the filleted
  version:
- Did max displacement settle as the mesh got finer, in both versions?
- Filleted version — did the highest stress settle? (values at each
  refinement, MPa):
- Sharp version — did the highest stress settle, or keep climbing? (values
  at each refinement, MPa):
- Based on what you saw: which of these stress numbers would you trust for
  a design decision, and why?

## Full throttle and factor of safety (Step 6)

- Predicted peak stress at full throttle, by scaling hover (MPa):
- Predicted tip deflection at full throttle, by scaling hover (mm):
- Simulated peak stress at full throttle (MPa):
- Simulated tip deflection at full throttle (mm):
- Did prediction and simulation agree? If not, what was wrong?
- Highest trustworthy stress at full throttle, and where it is (MPa, and
  gf/mm^2) — von Mises for aluminum, max principal (sigma_1) for CF:
- FoS = strength / that stress:
- If you checked the software's Safety Factor plot: its minimum, and what
  it divides by:
- Does your frame clear FoS >= 1.5 at full throttle?
- Is full-throttle tip deflection more than ~10% of L_cad?

## What you'd change

*(If FoS or mass missed the mark: what would you change, why, and what
would it cost in mass? If both are fine: what's the next thing that could
break this frame that you haven't modeled yet?)*

## Anything still hard to pin down

*(What's still an assumption or a guess here, and why? Isotropic CF,
perfectly rigid bolts, the fixed center, no self-weight — real gaps are
fine to name.)*
