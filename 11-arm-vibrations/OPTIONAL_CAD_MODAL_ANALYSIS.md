# Optional extension — Modal analysis in Autodesk Inventor

**Purpose.** Use a three-dimensional computer-aided design (CAD) model to investigate natural frequencies and vibration mode shapes, and compare the behavior with the simplified cantilever-beam model in the lab. You may use Autodesk Inventor or another package with equivalent modal-analysis capabilities.

**Choose ONE of the following two routes.** Both are acceptable; you do not need to create an additional CAD beam if you already have a complete quadcopter assembly.

## Route A — Your existing quadcopter assembly

Use the quadcopter assembly you have developed for the course, including its arms, central frame, and any other relevant components such as motor representations.

1. Open your existing assembly and check the material assignments of the structural components. A correct mass density and Young's modulus are important to the frequencies. Note any simplified or assumed material properties, particularly for 3D-printed components.
2. In Inventor, open **Environments → Stress Analysis**, create a simulation, and select **Modal Analysis**. Check that the software is analyzing the complete intended assembly, rather than only a selected part. If the analysis environment is not available, you can use comparable CAD/FEA software.
3. Review the **contacts and connections between components**. Parts that touch geometrically are not necessarily connected mechanically. Check whether the simulation's bonding/contact assumptions represent how the arms, frame, and motors are attached; remove or suppress unnecessary details if the analysis becomes impractical.
4. Select a physically meaningful boundary condition. A free, unsupported quadcopter is reasonably modeled with **no external fixed supports** (a free–free modal analysis) if your solver supports it. Such a model has six rigid-body motions with zero or nearly zero frequency; these are **not** structural vibration modes. If you instead impose constraints to represent a test stand or other support, state that assumption. Do **not** fix an arm root as though it were attached to a wall while also treating the entire airframe as freely flying.
5. If the simulation has a **Compute Preloaded Modes** option, turn it off for an unstressed natural-frequency comparison. Request enough modes to find elastic bending or twisting patterns after any rigid-body modes. Generate the mesh and run the analysis.
6. Inspect the deformed shapes. Identify at least one mode in which an arm bends vertically, bends laterally, or twists. Note whether the central frame, neighboring arms, and motor representations move with it. The displayed deformation is scaled for visualization; it is not an actual vibration amplitude.
7. Refine the mesh once if practical. Check whether the chosen elastic frequency changes noticeably.

**Interpretation.** A full quadcopter assembly has different supports, geometry, mass distribution, and coupled motion than a single beam clamped at its root. Compare the *types* of bending and the approximate frequency scales to the supplied beam analysis, but do not expect a one-to-one numerical match. A low-frequency motion of the whole aircraft or a loose component is not necessarily an arm-bending mode.

## Route B — A standalone arm or beam

Use an isolated arm from your existing CAD model, or create a simple solid rectangular beam if you prefer a controlled comparison. You do not need to make a new beam if an appropriate standalone arm is available.

1. Open the standalone arm or beam. If using a **uniform solid rectangular beam**, set its length `L`, vertical height `hy`, lateral width `bz`, Young's modulus `E`, and density `rho` to match Part 1. Other arm shapes are permitted, but note their differences from the rectangular model.
2. In **Environments → Stress Analysis**, create a **Modal Analysis** simulation. Disable preloaded modes for a direct comparison with the lab's unstressed model.
3. Apply a **Fixed** constraint to the arm's root face, where it would attach to the central frame, and leave its free end unconstrained. To compare the *bare-beam* calculations, omit the motor or motor representation. If you keep the motor, explain how its mass and connection are represented.
4. Request enough modes to identify the first vertical and lateral bending modes. Run the analysis and inspect the *mode shapes*. Do not assume that the first two modes necessarily correspond to those two directions; torsion or other motions may also appear.
5. Refine the mesh once, if practical, and compare the frequencies with those in the supplied code. For a matching rectangular bare beam, compare directly with `bare_f1_vertical` and `bare_f1_lateral` in `results.csv`. For a nonrectangular arm or a modeled motor, explain any differences in geometry, mass distribution, and support assumptions.

## What to report (optional reflection Q7)

State which route you chose, the CAD software used, the modeled geometry and material(s), and the constraints and connections. Report **at least one elastic mode shape and natural frequency (Hz)**, with a relevant beam-code comparison. For Route B with a matching bare rectangular beam, give a numerical frequency comparison; for Route A, a qualitative comparison and approximate frequency scale are sufficient. State whether you refined the mesh and explain one plausible reason for any discrepancy. No screenshots or additional files are required.

## Autodesk reference documentation

- Autodesk, About Stress Analysis (parts and assemblies): https://help.autodesk.com/cloudhelp/2026/ENU/Inventor-Help/files/GUID-61F01A5D-7E54-45A1-9698-7BB11F0AEE94.htm
- Autodesk, Run a modal frequency analysis: https://help.autodesk.com/cloudhelp/2026/ENU/Inventor-Help/files/GUID-1865721C-53ED-441E-9AAA-CCD0CB0C712B.htm
- Autodesk, Modal Analysis simulation settings: https://help.autodesk.com/cloudhelp/2026/ENU/Inventor-Help/files/GUID-587A1382-2EA2-418C-9365-C2FC86A3CD45.htm
- Autodesk, Preparing a model for stress analysis: https://help.autodesk.com/cloudhelp/2026/ENU/Inventor-Help/files/GUID-34261305-F235-41B6-B02A-F498975677A7.htm

*Software availability and interface labels depend on the Autodesk version, license, and installed analysis tools. If modal analysis is unavailable, skip this optional extension.*
