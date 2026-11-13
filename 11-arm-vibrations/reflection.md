# Quadcopter arm vibrations — reflection

**Name:**

## Part 1 — Geometry and approximate natural frequencies

**Q1.** State the `L`, `hy`, `bz`, `E`, `rho`, and motor mass you used, with units; explain any approximation to your actual arm. Report your **four approximate first bending frequencies** (bare vertical, bare lateral, with-motor vertical, with-motor lateral). Which direction has the smaller bending stiffness and why? What effect does adding the motor have? Name one structural vibration type excluded from this model.

## Part 2 — Finite-element predictions

**Q2.** Compare the first vertical and lateral finite-element frequencies with and without the motor. Explain the effect of adding motor mass. How well do the four finite-element values agree with the corresponding Part 1 estimates?

## Part 3 — Mode shapes and mesh convergence

**Q3.** Describe the first three vertical bending mode shapes. Compare the first and third vertical frequencies with 2 and 32 elements. Which is more sensitive to refinement, and why?

## Part 4 — Motor and propeller excitation

**Q4.** Identify the motor and propeller you chose, your estimated lower and upper operating speeds (rpm), blade count, and the source or assumption behind your RPM range. Distinguish lateral 1P imbalance, vertical blade-passing-frequency (BPF) thrust loading, and vertical 2×BPF loading. Why needn't a balanced multiblade propeller produce fluctuating *total* thrust?

**Q5.** Within your chosen operating range, which excitation frequencies approach a bending resonance? Where do higher modes make a difference to the 2×BPF prediction? What does the two-versus-three-blade comparison illustrate? Why might a frequency match still produce a small displacement?

## Part 5 — Design sensitivity

**Q6.** For separate 15% increases in length, width, and height, give the percentage changes in first vertical and lateral frequencies (a brief three-row table is sufficient). Which dimension has the largest absolute effect on each frequency? Identify the case selected by the code for `results.csv`. Does its frequency shift improve separation from excitations over your motor's operating range? Discuss the mass tradeoff.

## Optional — CAD modal analysis

**Q7 (optional).** State whether you analyzed your **existing quadcopter assembly** or a **standalone arm/beam**. Identify your CAD software, components and material(s), constraints and connections, and one mode shape with its natural frequency in Hz. Compare that mode with the relevant bending behavior or frequency scale in the beam code. For a matching bare rectangular beam, provide a direct numerical frequency comparison; for a full assembly or different geometry, explain why an exact match is not expected. Did you refine the mesh? Identify at least one possible source of disagreement.
