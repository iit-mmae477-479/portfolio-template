# Reflection — 3D forces and moments on a quadcopter arm

**Write brief answers based on your calculations and the notebook plots.** Refer to the values in `results.csv` where useful; there is no need to copy all numerical output into this file.

## Reference inputs

All groups use the same prescribed beam: **L = 120 mm**, **b = 20 mm**, **h = 10 mm**, **E = 3.0 GPa**, **T = 250 gf**. These values provide a common comparison with the earlier 120 mm arm analysis; they need not match your group's previously selected plate.

## Step 1 — Vertical bending

- How closely does the FEA vertical tip deflection agree with the beam-theory prediction? Give the approximate percentage difference.
- How can we extract a representative tip deflection from the 3D FEA displacement field for comparison with the centerline deflection predicted by beam theory?

## Step 2 — Bending in a second plane

- Which is greater: the vertical tip deflection from `Fy` or the lateral tip deflection from `Fz`? By what approximate factor?
- Explain the difference using the two second moments of area, `I_y` and `I_z`.

## Step 3 — Thrust and motor reaction moment

- Which tip translations and rotations are expected to be nonzero under `Fy+My` according to the beam compliance matrix?
- Compare the results for vertical thrust alone (`Fy`) and combined thrust and motor reaction moment (`Fy+My`). Which tip displacement components change when the motor reaction moment is included? How significant is the additional displacement relative to the vertical deflection produced by thrust?

## Step 4 — Torsion

- Compare the deformation produced by `Fy` and `Mx`. Why is the displacement of the tip center a useful measure of bending deformation but not torsional deformation? What quantity should be used to characterize torsion?
- How well does the FEA tip rotation agree with the beam-theory torsion prediction? Identify one reason why the two might differ.

## Model limitations

What is one assumption of this idealized beam/FEA model that could have an important effect on an actual manufactured quadcopter arm?
