# Reflection — truss arm force paths

## Case 2A vs. Case 2B

- Case 2A: which member has the largest \(|N|\), and is it in tension or
  compression?
- Case 2B: which member has the largest \(|N|\), and is it in tension or
  compression?
- Is the maximum force magnitude the same or different between 2A and 2B?
- If the magnitudes are the same, why can the distinction between tension
  and compression still matter for a slender truss member?

## The vertical member in Case 2B

- What force did you obtain in member `BC`?
- Explain this result directly from equilibrium of joint `B`. Which forces
  are available to balance the vertical direction at that joint?
- Does this mean `BC` is unnecessary in a real quadcopter arm? Why or why
  not? Name at least two loading situations in which the answer could
  change.

## Adding more cells at fixed arm size

For this section, `L_total = 120 mm`, `h = 30 mm`, and `P = 250 gf` remain
fixed while the number of cells is increased.

- As `n` increases, what happens to the cell width?
- What happens to the magnitude of the diagonal-member force? Explain this
  geometrically in terms of the diagonal angle.
- What happens to the maximum \(|N|\) anywhere in the truss as `n`
  increases?
- Why is this trend different from the trend in the diagonal force? Relate
  your answer to the overall bending moment that the arm has to transmit
  near the body.
- In Family A, is the root-region chord carrying the largest load primarily
  in tension or compression?
- In Family B, is the root-region chord carrying the largest load primarily
  in tension or compression?

## Design interpretation

- Based only on axial-force magnitude, does increasing the number of cells
  make the truss unambiguously better?
- What additional penalties or failure modes could appear as more members
  are added? Consider at least mass, joints/fasteners, manufacturability,
  and buckling.
- If you had to choose between Family A and Family B for this idealized
  upward-thrust load before doing a full buckling analysis, which load-path
  feature would you pay the most attention to, and why?

## Anything still hard to pin down

*(What assumptions in this pin-jointed, force-only model are least realistic
for an actual quadcopter arm?)*
