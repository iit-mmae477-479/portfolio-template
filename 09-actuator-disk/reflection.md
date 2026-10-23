# Actuator-Disk Lab — Derivations and Reflection

**Name:**

**Instructions:** Replace the `[Your work here]` placeholders with your calculations and explanations. Keep the section and question labels so they can be checked against `results.csv`. Use plain text/Markdown equations; short algebraic steps are sufficient when the derivation is clear. Consult `README.md` for the complete definitions, assumptions, and questions.

## Part A — Tip-speed dimensional analysis

**A1.** Give the fundamental dimensions of thrust, density, tip speed, and diameter. Solve for the powers a, b, and c, and define the dimensionless thrust coefficient C_T,U.

[Your work here]

**A2.** Show the conversion between C_T,U and C_T,Omega. Why is it only a change of normalization?

[Your work here]

**A3.** At constant thrust coefficient, how does thrust scale with diameter when (i) angular speed is fixed and (ii) tip speed is fixed? Explain.

[Your work here]

## Part B — Actuator-disk assumptions and mass conservation

**B1.** Briefly describe the streamtube control volume, the assumptions of the model, and why a fixed-area upstream cylinder is inappropriate.

[Your work here]

**B2.** Obtain the mass-flow rate at the disk, define the pressure jump, and relate pressure jump to thrust.

[Your work here]

## Part C — Momentum conservation

**C1.** Show the axial momentum balance (downward positive) and substitute the mass flow rate.

[Your work here]

**C2.** Why is another equation needed to determine both induced velocity and far-wake velocity?

[Your work here]

## Part D — Bernoulli and the pressure jump

**D1.** Apply Bernoulli separately above and below the disk. Derive the pressures p'^− and p'^+.

[Your work here]

**D2.** Obtain the pressure jump and combine it with the momentum balance to derive the far-wake speed and actuator-disk thrust equation.

[Your work here]

**D3.** Why cannot Bernoulli be applied directly across the disk? Why can the gravitational term be removed from the pressure-perturbation form without neglecting the quadcopter's weight?

[Your work here]

## Part E — Power and diameter

**E1.** Derive induced velocity vi from a specified thrust and then derive ideal induced power Pi. Check the units.

[Your work here]

**E2.** Obtain total ideal hover power for N rotors supporting mass M. How does it depend on diameter at fixed vehicle weight and rotor count?

[Your work here]

**E3.** Explain why ideal induced power alone is insufficient for selecting a commercial propeller.

[Your work here]

## Part F — Inflow ratio and model limitations

**F1.** Define lambda, derive the relationship between lambda and C_T,U, and show how this connects the tip-speed and induced-air-speed thrust formulas.

[Your work here]

**F2.** Can dimensional analysis plus actuator-disk theory determine motor RPM? What additional information is needed?

[Your work here]

## Part G — Your quadcopter

**G1. Design inputs and units.** Give the all-up mass of your quadcopter (including battery and payload), planned commercial propeller diameter, and a comparison diameter. State whether the mass is measured or estimated, identify the propeller size/model if known, show the conversions to SI, and explain whether the comparison propeller would fit the frame.

[Your work here]

**G2. Actuator-disk calculation.** Using the mass of your quadcopter and installed rotor diameter, show intermediate calculations for disk area `A`, hover thrust per rotor `T`, mass flow `m_dot`, induced velocity `vi`, far-wake velocity `vw`, pressure jump `Delta_p`, and ideal power per rotor `Pi`. Enter the selected outputs in `results.csv`.

[Your work here]

**G3. Rotor diameter comparison.** Calculate total ideal induced hover power at your planned diameter and chosen comparison diameter at the *same total weight and rotor count*. Check your computed ratio against the diameter scaling law. What practical considerations might prevent choosing the larger rotor?

[Your work here]

**G4. Connecting blade and air speeds (conditional).** If you have a measured or documented estimate of the **loaded hover RPM**, give the source, convert it to `Omega` and `U_tip`, and calculate `lambda` and `C_T,U` in two ways. If this information is unavailable, leave the three RPM-dependent CSV entries blank and explain why actuator-disk theory cannot determine them by itself. Note that a motor's `KV` value is not a loaded hover-RPM measurement.

[Your work here]

## Final synthesis

Explain in 2–4 sentences why the tip-speed thrust scaling and actuator-disk thrust equation are compatible, and what each model can and cannot predict.

[Your work here]
