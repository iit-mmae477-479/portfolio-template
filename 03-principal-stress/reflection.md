# Reflection — principal stresses at two stations

## Carried forward from 02

- Plate width, b (mm):
- Plate thickness, h (mm):
- Material (CF or aluminum):
- V(0), self-weight included, from `02` (gf):
- M(0), self-weight included, from `02` (gf·mm):
- V(60), self-weight included, from `02` (gf):
- M(60), self-weight included, from `02` (gf·mm):

## Cross-section properties (same at both stations)

- Area, A = b h (mm²):
- Moment of inertia, I = b h^3 / 12 (mm^4):
- c = h / 2 (mm):

## Root (x = 0)

**Neutral axis**
- tau_xy = 1.5 V(0) / A (gf/mm²):
- sigma_1 (gf/mm²):
- sigma_2 (gf/mm²):
- theta_p (degrees):
- sigma_vM (gf/mm²):

**Top surface**
- sigma_x = 6 M(0) / (b h^2) (gf/mm²):
- sigma_1 (gf/mm²):
- theta_p (degrees):
- sigma_vM (gf/mm²):

## Mid-span (x = 60 mm)

**Neutral axis**
- tau_xy = 1.5 V(60) / A (gf/mm²):
- sigma_1 (gf/mm²):
- sigma_2 (gf/mm²):
- theta_p (degrees):
- sigma_vM (gf/mm²):

**Top surface**
- sigma_x = 6 M(60) / (b h^2) (gf/mm²):
- sigma_1 (gf/mm²):
- theta_p (degrees):
- sigma_vM (gf/mm²):

## Sanity checks

- Root neutral axis: does sigma_1 - sigma_2 equal 2 * tau_xy? (yes/no, and
  the two numbers):
- Root top surface: does sigma_1 equal your sigma_x there? (yes/no):
- Mid-span neutral axis: does sigma_1 - sigma_2 equal 2 * tau_xy? (yes/no):
- Mid-span top surface: does sigma_1 equal your sigma_x there? (yes/no):
- Did both top-surface sigma_vM values come out equal to their sigma_x?
  (yes/no):

## Root vs. mid-span — thinking ahead to FEA

- Which of your four points has the largest sigma_vM, and does that match
  what you'd expect (the root generally carries more moment than
  mid-span)?
- Given the Saint-Venant framing in the instructions: when you eventually
  check these hand-calc numbers against an FEA model of the same arm,
  which station do you expect to match more closely, and why? What
  specifically about the root makes it a worse fit for the beam-theory
  idealization than mid-span?
- What would you actually be looking at in an FEA contour plot to make
  that comparison — the same sigma_vM number, or something else?

## Anything still hard to pin down

*(What's still an assumption or a guess here, and why? Real gaps are fine
to name.)*
