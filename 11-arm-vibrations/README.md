# Quadcopter arm vibrations — computational lab

**Objective.** Predict the natural frequencies and bending mode shapes of a quadcopter arm, investigate possible motor-induced resonances, and compare the effects of changes to the arm's dimensions.

This is an **individual** computational lab. Use one supplied program: MATLAB (`quadcopter_vibrations.m`), Python (`quadcopter_vibrations.py`), or the Google Colab notebook (`quadcopter_vibrations.ipynb`). The element matrices, finite-element assembly, eigenvalue analysis, and vibration plots are provided. You will choose design and motor parameters, complete one short motor-mass coding task in Part 2, and interpret the results.

**Submit two files only:** `results.csv` (numerical results in the supplied template) and `reflection.md` (short responses to the supplied questions). Do not submit plots, source code, or the notebook. The optional CAD exercise is reported in `reflection.md` and requires no additional file.

| Part | Investigation | Report |
| --- | --- | --- |
| 1. Geometry and frequency estimates | Compare vertical and lateral bending, with and without a motor | Reflection Q1 |
| 2. Beam finite-element model | Calculate frequencies of the bare beam and then add a tip motor mass | Four entries in `results.csv`; reflection Q2 |
| 3. Mode shapes and convergence | Examine higher bending modes and mesh refinement | One CSV entry; reflection Q3 |
| 4. Motor and propeller excitation | Use your chosen motor's RPM range; examine imbalance, blade passing, and harmonics | Three CSV entries; reflection Q4–Q5 |
| 5. Design sensitivity | Increase length, width, and height separately by the same percentage | Three CSV entries for the most sensitive case; reflection Q6 |
| Optional computer-aided design (CAD) analysis | Examine your existing quadcopter assembly **or** a standalone arm/beam; identify and interpret vibration modes | Optional reflection Q7 |

## Part 1 — Arm geometry and approximate natural frequencies

Model a quadcopter arm as a **straight solid rectangular beam of constant cross-section**. It is fixed to the frame at its root (`x = 0`), with the motor at its free tip (`x = L`). If your existing arm is not a uniform rectangle, choose a solid rectangle of similar length and cross-sectional dimensions and explain your approximation in Q1.

We take `x` along the arm, `y` vertically, and `z` laterally. Its height `hy` is measured vertically and width `bz` laterally. We analyze **vertical bending**, displacement in `y` and bending around `z`, separately from **lateral bending**, displacement in `z` and bending around `y`.

| Code name | Definition | Units |
| --- | --- | --- |
| `L` | Beam length from fixed root to motor tip | m |
| `hy` | Height of solid rectangular cross-section, along `y` | m |
| `bz` | Width of solid rectangular cross-section, along `z` | m |
| `E` | Young's modulus of the beam material | Pa |
| `rho` | Mass density of **beam material only**, not including the motor | kg/m³ |
| `motor_mass` (`motorMass` in MATLAB) | Motor mass concentrated at the free end | kg |
| `A = hy*bz` | Cross-sectional area | m² |
| `mu = rho*A` | Beam mass per unit length (no motor mass) | kg/m |
| `m_arm = mu*L` | Mass of the bare beam | kg |
| `Iz = bz*hy^3/12` | Second moment of area for vertical bending | m⁴ |
| `Iy = hy*bz^3/12` | Second moment of area for lateral bending | m⁴ |

A beam's resistance to bending depends on its bending rigidity `EI`, where `I` is `Iz` for vertical bending and `Iy` for lateral bending. For a force applied at the free tip, the equivalent stiffness is

`k = 3*E*I/L^3`.

To approximate the **first natural frequency**, the beam is replaced by an equivalent single-degree-of-freedom spring–mass system. Only part of the beam's mass contributes to the effective moving mass because the beam's displacement is nearly zero at its fixed root and largest near its tip. We use

- **Bare beam:** `m_eff = (33/140)*m_arm`.
- **Beam with motor:** `m_eff = motor_mass + (33/140)*m_arm`.

For either case, `f_est = sqrt(k/m_eff)/(2*pi)`, in hertz (Hz). The factor `33/140` is obtained by assuming the beam deflects in the same shape as it does under a static force at the tip; it is an approximation, not an additional physical mass. The first frequency estimate is not intended to describe higher modes.

**What to do**

1. Enter your own `L`, `hy`, `bz`, `E`, `rho`, and `motor_mass` in the Part 1 input section of the code. Use SI units. State any assumptions if an exact value is unavailable.
2. Run Part 1. Record the **four** frequency estimates printed: bare beam vertical and lateral, and beam with motor vertical and lateral.
3. Compare the bending rigidities `E*Iz` and `E*Iy`. Explain which bending direction has lower stiffness and how the dimensions affect that result. Explain what happens to the frequencies when the motor mass is included.

**Report:** In reflection Q1, give your inputs with units, the four approximate frequencies (Hz), the comparison of bending directions, and one limitation of the model. The beam mass is calculated in the program but is **not** a required Part 1 submission.

**Scope:** These are two *bending* models, not a full description of all structural modes. An actual arm may also undergo torsion (twisting around `x`), axial vibration, or coupled motions.

## Part 2 — Beam finite-element model, before and after adding the motor

Recall the **two-mass, three-spring system from the lecture**, with fixed walls at both ends. Spring `k1` joins the left wall to mass `m1`; spring `k2` joins the two masses; spring `k3` joins mass `m2` to the right wall. Each mass is acted on by the two springs attached to it. Contributions from both springs enter that mass's equation of motion. The matrices for that system are

```text
    K = [ k1+k2    -k2   ]       M = [ m1   0  ]
        [  -k2    k2+k3 ]           [  0  m2  ]
```

Here `K` is the **stiffness matrix**, describing how restoring forces depend on displacement, and `M` is the **mass matrix**, describing the inertia of the system. The equations of free vibration are `M*q_ddot + K*q = 0`, where `q` is the vector of displacements and `q_ddot` contains their accelerations.

The beam program divides the arm into short sections called **elements**, connected at **nodes**. At each node, the two unknowns in one bending direction are a transverse displacement `w` and a local slope `s` (the angle of the bent beam for small deflections). Neighboring beam elements share a node; their stiffness and inertia contributions combine there, just as the forces from adjacent springs combine in the lecture model. The supplied program performs this **matrix assembly** and applies a fixed-root condition (`w = 0` and `s = 0` at `x = 0`). Unlike the simple two-mass example, the beam's element mass matrices include some off-diagonal entries because motion varies continuously within each element.

| Code name | Definition | Units |
| --- | --- | --- |
| `n_elem` (`nElem` in MATLAB) | Number of beam elements | none |
| `ell = L/n_elem` | Length of one element | m |
| `EI = E*I` | Bending rigidity for the chosen bending direction | N·m² |
| `Ke`, `Me` | Stiffness and mass matrices of one beam element | various entries depend on displacement/slope units |
| `K`, `M` | Assembled stiffness and mass matrices for the whole beam | various entries depend on displacement/slope units |
| `w`, `s` | Nodal transverse displacement and slope | m, dimensionless (approximately radians) |
| `omega` | Natural angular frequency | rad/s |

Solving the finite-element eigenvalue problem `K*phi = omega^2*M*phi`, after fixing the root, gives the natural frequencies `f = omega/(2*pi)` and corresponding mode shapes `phi`.

**What to do**

1. Run the **bare-beam** calculation. Observe the first vertical and lateral frequencies before adding the motor.
2. Complete the **Part 2 coding task**: uncomment the two indicated lines that add `motor_mass` to the tip-displacement entry of the *mass matrix* for each bending direction, and remove the indicated stop/error line. Do not change the stiffness matrices. These are two calculations of **one motor** moving in alternative directions, not two motors.
3. Run the completed program. Compare the first frequencies with and without the motor. Compare the finite-element results to the four approximate predictions from Part 1.

**Report:** Enter `bare_f1_vertical`, `bare_f1_lateral`, `motor_f1_vertical`, and `motor_f1_lateral`, in Hz, into `results.csv`. Answer reflection Q2.

## Part 3 — Higher bending modes and mesh convergence

Unlike an equivalent single spring–mass oscillator, a beam can vibrate in multiple bending shapes, each with its own natural frequency. The code plots the first three **vertical** bending modes and calculates their frequencies using 2, 4, 8, 16, and 32 elements. Increasing the number of elements tests **mesh convergence**: whether the calculated frequencies settle as the beam is represented by more, shorter elements.

**What to do:** Inspect the mode-shape plot. Compare the first and third vertical natural frequencies predicted with 2 and 32 elements. Identify which mode is more sensitive to mesh refinement, and why.

**Report:** Enter `motor_f2_vertical` (Hz) in `results.csv` and answer reflection Q3. No code editing is required.

## Part 4 — Motor and propeller excitation

The program estimates **steady-state tip vibration amplitudes** due to periodic forces. It retains up to three bending modes and assumes a damping ratio `zeta` (the same value for each mode). The amplitudes of the forces below are hypothetical modeling assumptions rather than measurements from your motor. Do not interpret them as a validated prediction of actual in-flight vibration levels.

**Use the motor and propeller you selected for your quadcopter.** Enter a lower and upper *operating* motor speed (`rpm_low`, `rpm_high`; MATLAB `rpmLow`, `rpmHigh`) and the blade count (`n_blades`; MATLAB `nBlades`). If available, use the motor/propeller manufacturer's operating data. If operating RPM values are not published, make a justified estimate and state your assumptions. Motor `KV` is approximately a no-load speed constant in revolutions per minute per volt; `KV × voltage` is **not** a measured RPM under propeller load. The program plots speeds from zero to 15% above your chosen upper limit, and highlights your operating interval. All reported peak amplitudes are calculated **only within your interval**.

An excitation frequency of **1P** means once per motor revolution, **2P** means twice per revolution, etc. Motor speed in revolutions per minute (`RPM`) is converted to angular speed with `Omega = 2*pi*RPM/60` (rad/s).

**Case A — rotating imbalance (1P, lateral).** If the rotating assembly is not perfectly balanced, it can produce a lateral force at the rotational frequency. Model the imbalance as an equivalent small eccentric mass `m_unbalance` at a distance `eccentricity` from the rotation axis. Their product `U = m_unbalance*eccentricity` is the *unbalance* (kg·m), and the force amplitude is `F_1P = U*Omega^2`. `m_unbalance` represents the source of forcing and is **not** added to the beam's motor point mass.

**Case B — blade-passing-frequency (BPF) thrust fluctuations, vertical.** The **blade-passing frequency**, abbreviated **BPF**, is `f_BPF = n_blades*RPM/60`. Merely having multiple blades does **not** guarantee fluctuating *total* thrust: an ideal, balanced rotor in uniform flow can produce nearly steady thrust. For this exercise, we **assume** that unsteady aerodynamics produces a small periodic thrust variation at BPF. We model its amplitude as `F_BPF = bpf_fraction*T_mean` with mean thrust `T_mean = T_ref*(RPM/rpm_ref)^2`. The program sets `rpm_ref` to the midpoint of your selected RPM range; `T_ref` and the fluctuation fractions are illustrative input values.

**Case C — second BPF harmonic, vertical.** Non-sinusoidal thrust variations may also contain higher harmonics. The assumed `2×BPF` force has frequency `2*n_blades*RPM/60` and amplitude `F_2BPF = harmonic_fraction*T_mean`. For two blades, this is a `4P` component.

| Code name | Definition | Units |
| --- | --- | --- |
| `rpm_low`, `rpm_high` (`rpmLow`, `rpmHigh`) | Lower and upper operating RPM of your chosen motor | rpm |
| `n_blades` (`nBlades`) | Number of blades of your chosen propeller | none |
| `zeta` | Assumed modal damping ratio | dimensionless |
| `m_unbalance` (`mUnbalance`), `eccentricity` | Equivalent eccentric mass and distance | kg, m |
| `T_ref` (`Tref`) | Assumed mean thrust at the reference speed | N |
| `rpm_ref` (`rpmRef`) | Reference speed, calculated as the midpoint of your RPM interval | rpm |
| `bpf_fraction` (`bpfFraction`) | Assumed BPF amplitude divided by mean thrust | dimensionless |
| `harmonic_fraction` (`harmonicFraction`) | Assumed 2×BPF amplitude divided by mean thrust | dimensionless |

**What to do**

1. Set your motor's `rpm_low` and `rpm_high` and your propeller's `n_blades`. Note the motor model and the source or assumptions behind your RPM values in Q4.
2. Compare lateral 1P imbalance with vertical BPF and 2×BPF responses. These curves use *different* force amplitudes, frequencies, and bending directions, so do not attribute all amplitude differences to resonance alone.
3. For 2×BPF, compare retaining only the first vertical mode with retaining the first three modes. Identify whether higher modes matter within your chosen operating interval.
4. Examine the hypothetical two-blade versus three-blade BPF comparison, holding the assumed forcing fraction fixed. Explain how blade count changes possible resonant speeds without necessarily changing actual thrust-ripple amplitude.
5. Identify possible matches between forcing frequencies and the computed bending natural frequencies within your motor's operating interval. The program lists the motor speed at which each excitation (1P, BPF, 2×BPF) matches each of the first three bending modes, and marks those inside your interval. Distinguish a frequency match from a *large* vibration response.

**Report:** Enter the **peak** vibration amplitudes over your operating interval in `peak_1P_lateral`, `peak_BPF_vertical`, and `peak_2BPF_vertical` (mm), exactly as printed (four significant figures; values such as `4.18e-05` are fine in the CSV), and answer reflection Q4–Q5.

## Part 5 — Compare the effects of three design changes

Increasing a dimension changes both beam mass and bending stiffness. To compare sensitivities fairly, the code runs **three separate scenarios** using the same dimension factor, initially `change_factor = 1.15` (MATLAB `changeFactor = 1.15`):

1. Increase **length** by 15%, keeping width and height unchanged.
2. Increase **width** by 15%, keeping length and height unchanged.
3. Increase **height** by 15%, keeping length and width unchanged.

Keep this factor at 1.15 for the required comparison. The motor mass, material, and other inputs remain fixed. Each scenario starts from your original baseline beam, not from the preceding modified beam. The code prints the new beam mass, first vertical and lateral frequencies, and percentage frequency changes for all three cases.

**What to do:** Compare all three cases. Determine which dimension causes the largest absolute percentage change in the **first vertical frequency** and which causes the largest change in the **first lateral frequency**. For a single consistent CSV entry, the code selects the case with the largest **average of the absolute percentage changes in the two frequencies**; it prints that case and the three values to enter. A larger frequency change is not necessarily an improvement: it might shift a natural frequency *into* the motor operating range.

**Report:** Enter the printed selected-case `modified_beam_mass` (g), `modified_f1_vertical` (Hz), and `modified_f1_lateral` (Hz) in `results.csv`. In reflection Q6, compare all three cases and say whether the selected change improves the frequency separation from excitations over your operating interval. Explain any mass tradeoff. No numerical-method code editing is required.

## Optional extension — Compare against a CAD modal analysis

You may choose either of two approaches, using Autodesk Inventor or another program that supports modal analysis:

- **Existing quadcopter assembly:** Analyze the aircraft model you have already developed. Identify at least one mode involving bending or twisting of an arm, and note whether other components move. The complete assembly is **not** the same mechanical system as the clamped, isolated beam in Parts 1–3; compare the shapes and frequency scales, but do not expect its frequencies to match the beam predictions exactly. State the constraints, connections, and components included.
- **Standalone arm or beam:** Analyze an individual arm from your CAD model, or a solid rectangular beam matching your Part 1 dimensions. Fix its root and leave the other end free. A **bare uniform rectangular beam** gives the most direct numerical comparison with the bare-beam frequencies in Part 2; an arm with different geometry or an attached motor may differ for physical reasons.

For instructions for both options, read the separate text file `OPTIONAL_CAD_MODAL_ANALYSIS.md` in this package. In either approach, match modes by their **shapes**, not just their frequency order. A three-dimensional model may exhibit torsional and other modes absent from the simplified bending model.

**Optional report:** Answer reflection Q7 with the approach chosen, at least one CAD mode and its frequency, a relevant comparison to the beam model, and an explanation of differences. No screenshots or additional submissions are required.

## Running the programs

- **MATLAB:** Open `quadcopter_vibrations.m` and run the entire script. It uses local functions placed near the sections that call them, supported in MATLAB R2024a and later. The code may require rearranging functions for earlier MATLAB versions. Do not edit the supplied helper functions.
- **Python:** Run `quadcopter_vibrations.py` with NumPy, SciPy, and Matplotlib installed, or open `quadcopter_vibrations.ipynb` in Google Colab and run the cells in order.
- The student version intentionally stops in Part 2 until you uncomment the two motor-mass lines and delete the stop/error line. You can view the Part 1 and bare-beam results before completing that task.
- Use the same baseline design inputs for Parts 1–4. Part 5 automatically creates separate changed-geometry cases from that baseline.
