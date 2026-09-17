# Reflection — beam deflection, hand calc vs. Inventor

## Carried forward from 02 and 03

- Plate width, b (mm):
- Plate thickness, h (mm):
- Material (CF or aluminum):
- P = T_hover (gf):
- I = b h^3 / 12 (mm^4), from `03`:

## Young's modulus

- E, from a datasheet or reference (GPa):
- Source (link or citation):
- E converted to gf/mm^2 (E_GPa x 101,972):

## Hand calc

- EI (gf*mm^2):
- y_hand = P L^3 / (3 E I), L = 120 mm (mm):

## Inventor model and simulation

- Material assigned in Inventor (exact match, or closest substitute — say
  which):
- Constraint and load setup (brief description — confirms it matches the
  hand-calc assumptions):
- y_fea, maximum displacement (mm):
- % difference between y_fea and y_hand:
- If the % difference is large (over ~25%), what did you check, and what
  did you find?

## Stress check: root vs. mid-span

- sigma_vM, root, top surface — hand value (from `03`) (gf/mm^2):
- sigma_vM, root, top surface — Inventor probe (gf/mm^2):
- sigma_vM, mid-span (x = 60 mm), top surface — hand value (from `03`)
  (gf/mm^2):
- sigma_vM, mid-span, top surface — Inventor probe (gf/mm^2):
- Which station's hand and FEA values agree more closely?
- Does this match the prediction you made in `03`'s "thinking ahead to
  FEA" section? If not, what do you think explains the difference?

## Anything still hard to pin down

*(What's still an assumption or a guess here, and why? Real gaps are fine
to name.)*
