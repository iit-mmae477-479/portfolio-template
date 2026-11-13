"""Quadcopter arm vibrations — computational lab (Python 3).

Follow README.md Parts 1–5. One short coding task appears in Part 2:
add the motor point mass to the two beam mass matrices.
Coordinates: x along the arm, y vertical, z lateral.
The beam is a solid rectangle with constant cross-section.
"""

# %% Part 1 — Geometry and physical parameters
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

# Part 1 action: Replace L, bz, hy, E, rho, and motor_mass with your values.
# Use a uniform solid rectangle, and state any approximations in reflection Q1.
# Other excitation and numerical parameters are illustrative defaults.
p = dict(
    L=0.22,                # arm length [m]
    bz=0.016,              # solid rectangular width in lateral z [m]
    hy=0.008,              # solid rectangular height in vertical y [m]
    E=70e9,                # Young's modulus of beam material [Pa]
    rho=2700.0,            # Density of beam material only [kg/m^3]
    motor_mass=0.055,      # point mass fixed at arm tip [kg]
    zeta=0.03,             # assumed damping ratio of each bending mode [-]
    rpm_low=3500.0,        # SET from YOUR selected motor: lower operating speed [rpm]
    rpm_high=12500.0,      # SET from YOUR selected motor: upper operating speed [rpm]
    m_unbalance=0.00015,   # hypothetical equivalent eccentric rotating mass [kg]
    eccentricity=0.002,   # eccentric distance from spin axis [m]
    n_blades=2,            # SET from YOUR selected propeller: blade count [-]
    T_ref=3.0,             # illustrative mean thrust [N] at midpoint of selected RPM range
    bpf_fraction=0.02,    # assumed blade-passing-frequency (BPF) ripple / mean thrust [-]
    harmonic_fraction=0.004, # hypothetical amplitude of 2*BPF / mean thrust [-]
)
# The midpoint is a reference for the illustrative thrust-versus-RPM model.
# Reference thrust and thrust-ripple fractions are assumptions, not motor measurements.
if not (0 < p['rpm_low'] < p['rpm_high']):
    raise ValueError('Set rpm_low and rpm_high for your motor, with 0 < low < high.')
if p['n_blades'] < 1:
    raise ValueError('n_blades must be a positive integer.')
p['rpm_ref'] = (p['rpm_low'] + p['rpm_high']) / 2.0
n_elem = 12              # baseline mesh; number of short beam pieces

# For a solid rectangle: area A, second moment Iy (sideways z), Iz (vertical y).
A = p['bz'] * p['hy']
Iy = p['hy'] * p['bz']**3 / 12.0
Iz = p['bz'] * p['hy']**3 / 12.0
mu = p['rho'] * A          # Beam mass per unit arm length [kg/m], excluding motor mass
m_arm = mu * p['L']        # total beam mass [kg]
print('Part 1 — Uniform solid rectangular arm')
print(f"A = {A:.6g} m^2, Iy = {Iy:.6g} m^4, Iz = {Iz:.6g} m^4")
print(f"rho = {p['rho']:.1f} kg/m^3 (beam only), mu = {mu:.4f} kg/m")
print(f'Arm mass = {1000*m_arm:.3f} g; motor point mass = {1000*p["motor_mass"]:.3f} g')
# Equivalent tip stiffness / effective mass from earlier spring-mass model.
m_eff_bare = (33.0/140.0)*m_arm
m_eff_motor = p['motor_mass'] + m_eff_bare
k_y = 3*p['E']*Iz/p['L']**3
k_z = 3*p['E']*Iy/p['L']**3
f_bare_est_y = np.sqrt(k_y/m_eff_bare)/(2*np.pi)
f_bare_est_z = np.sqrt(k_z/m_eff_bare)/(2*np.pi)
f_motor_est_y = np.sqrt(k_y/m_eff_motor)/(2*np.pi)
f_motor_est_z = np.sqrt(k_z/m_eff_motor)/(2*np.pi)
print(f'Bare beam estimates:     vertical {f_bare_est_y:.3f} Hz; lateral {f_bare_est_z:.3f} Hz')
print(f'With motor estimates:     vertical {f_motor_est_y:.3f} Hz; lateral {f_motor_est_z:.3f} Hz')
print('Part 1 reporting (reflection Q1 only): state the chosen inputs, the four')
print('approximate frequencies (bare/with motor, vertical/lateral), and explain their differences.')


# %% Part 2 — Finite-element beam and tip motor mass
# Finite-element matrix assembly and the eigenvalue calculation are supplied.
def element_matrices(EI, mass_per_length, ell):
    """One element: EI = bending rigidity [N m^2]; ell = element length in meters."""
    Ke = EI/ell**3 * np.array([
        [12, 6*ell, -12, 6*ell],
        [6*ell, 4*ell**2, -6*ell, 2*ell**2],
        [-12, -6*ell, 12, -6*ell],
        [6*ell, 2*ell**2, -6*ell, 4*ell**2]
    ], dtype=float)
    Me = mass_per_length*ell/420.0 * np.array([
        [156, 22*ell, 54, -13*ell],
        [22*ell, 4*ell**2, 13*ell, -3*ell**2],
        [54, 13*ell, 156, -22*ell],
        [-13*ell, -3*ell**2, -22*ell, 4*ell**2]
    ], dtype=float)
    return Ke, Me


def assemble_beam(params, bend_direction, n_elements):
    """Whole-beam matrices, before adding motor; assembled from short elements."""
    area = params['bz'] * params['hy']
    mu_beam = params['rho'] * area   # kg/m — uniform Beam mass per unit length
    second_moment = (params['bz'] * params['hy']**3 / 12.0 if bend_direction == 'y'
                     else params['hy'] * params['bz']**3 / 12.0)
    ell = params['L']/n_elements  # length of one short beam element [m]
    Ke, Me = element_matrices(params['E']*second_moment, mu_beam, ell)
    size = 2*(n_elements+1)  # two values at each node: transverse motion and slope
    K, M = np.zeros((size, size)), np.zeros((size, size))
    for element in range(n_elements):
        positions = np.arange(2*element, 2*element+4)
        # Analogy: in the lecture's two-mass, three-spring model with fixed
        # outer walls, each mass receives forces from both adjacent springs.
        # Likewise, adjacent beam pieces contribute at a shared node.
        K[np.ix_(positions, positions)] += Ke
        M[np.ix_(positions, positions)] += Me
    return K, M


def find_modes(K, M, n_elements):
    """Clamp root: displacement = slope = 0; solve vibration eigenproblem."""
    free = np.arange(2, K.shape[0])
    Kff, Mff = K[np.ix_(free,free)], M[np.ix_(free,free)]
    eigenvalues, V = eigh(Kff, Mff)  # returns mass-normalized eigenvectors
    if np.any(eigenvalues <= 0):
        raise ValueError('Nonpositive eigenvalue; check stiffness/mass and clamp.')
    tip_position = 2*n_elements  # displacement at free end (not its slope)
    tip_local = int(np.where(free == tip_position)[0][0])
    return dict(K=K, M=M, Kff=Kff, Mff=Mff, free=free, V=V,
                omega=np.sqrt(eigenvalues), tip_local=tip_local,
                tip_position=tip_position, n_elements=n_elements)


# First calculate the frequencies of the beam alone (no motor).
K_y, M_y = assemble_beam(p, 'y', n_elem)
K_z, M_z = assemble_beam(p, 'z', n_elem)
bare_y = find_modes(K_y, M_y, n_elem)
bare_z = find_modes(K_z, M_z, n_elem)
print('\nPart 2 — First frequency before attaching the motor')
print(f'Bare beam, vertical y bending: {bare_y["omega"][0]/(2*np.pi):.3f} Hz')
print(f'Bare beam, lateral z bending:  {bare_z["omega"][0]/(2*np.pi):.3f} Hz')

# The motor is mounted at the far (free) end, so add its MASS to the tip
# displacement in the beam's mass matrix; it adds no beam bending stiffness.
M_y_motor, M_z_motor = M_y.copy(), M_z.copy()
tip_position = 2*n_elem

# Part 2 coding task: enable the two lines below (remove their # symbols).
# Then remove the raise line. Do not change K_y or K_z.
# The same physical motor is modeled in two independent bending directions.
# M_y_motor[tip_position, tip_position] += p['motor_mass']
# M_z_motor[tip_position, tip_position] += p['motor_mass']
raise NotImplementedError('Part 2 coding task: enable the two mass-addition lines')

motor_y = find_modes(K_y, M_y_motor, n_elem)
motor_z = find_modes(K_z, M_z_motor, n_elem)
print('First frequency with motor point mass')
print(f'With motor, vertical y bending: {motor_y["omega"][0]/(2*np.pi):.3f} Hz')
print(f'With motor, lateral z bending:  {motor_z["omega"][0]/(2*np.pi):.3f} Hz')


# %% Part 3 — Natural frequencies, mode shapes, and convergence
# The following helpers are supplied. Students need not edit them.
def interpolated_mode(model, mode_number, length, samples_per_element=30):
    """Smooth curve from the FE mode, using cubic beam interpolation."""
    n = model['n_elements']
    ell = length/n
    q = np.zeros(2*(n+1))
    q[model['free']] = model['V'][:, mode_number]
    xx, yy = [], []
    for e in range(n):
        t = np.linspace(0.0, 1.0, samples_per_element+1)
        N = np.array([1-3*t*t+2*t**3, ell*(t-2*t*t+t**3),
                      3*t*t-2*t**3, ell*(-t*t+t**3)])
        w = q[2*e:2*e+4] @ N
        if e > 0:
            t, w = t[1:], w[1:]
        xx.extend((e+t)*ell)
        yy.extend(w)
    xx, yy = np.asarray(xx), np.asarray(yy)
    if yy[-1] < 0: yy = -yy
    return xx, yy/max(abs(yy))


def model_with_motor(params, direction, n_elements):
    """Convenience for convergence and design variations (already completed)."""
    K, M = assemble_beam(params, direction, n_elements)
    M[2*n_elements, 2*n_elements] += params['motor_mass']
    return find_modes(K, M, n_elements)


fy = motor_y['omega'][:3]/(2*np.pi)
fz = motor_z['omega'][:3]/(2*np.pi)
print('\nPart 3 — First three natural frequencies (motor attached)')
for j in range(3):
    print(f'Mode {j+1}: vertical {fy[j]:9.3f} Hz; lateral {fz[j]:9.3f} Hz')

# Illustrate shapes of first three vertical modes.
fig, ax = plt.subplots(figsize=(8, 4))
for j in range(3):
    x, displacement = interpolated_mode(motor_y, j, p['L'])
    ax.plot(x/p['L'], displacement, lw=1.8,
            label=f'Mode {j+1}: {fy[j]:.1f} Hz')
ax.set(xlabel='Position along arm, x/L',
       ylabel='Mode shape (normalized displacement)',
       title='Vertical bending: first three mode shapes')
ax.axhline(0, lw=0.6, color='gray'); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout()

mesh_sizes = [2, 4, 8, 16, 32]
conv_y = np.array([model_with_motor(p, 'y', n)['omega'][:3]/(2*np.pi)
                   for n in mesh_sizes])
print('\nConvergence: vertical natural frequencies (Hz)')
print('Elements       f1        f2        f3')
for n, f in zip(mesh_sizes, conv_y):
    print(f'{n:8d}   {f[0]:8.2f}  {f[1]:8.2f}  {f[2]:8.2f}')
fig, ax = plt.subplots(figsize=(8, 4))
for j in range(3):
    ax.plot(mesh_sizes, conv_y[:, j], marker='o', label=f'Mode {j+1}')
ax.set(xlabel='Number of beam elements', ylabel='Natural frequency (Hz)',
       title='Mesh convergence: vertical bending')
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()


# %% Part 4 — Three excitation mechanisms (1P, BPF, 2×BPF)
# BPF = blade-passing frequency; 1P = once per rotor revolution.
def tip_amplitude(model, angular_frequency, force_amplitude, damping_ratio, n_modes=3):
    """Steady-state tip displacement from a harmonic tip force in one direction."""
    angular_frequency = np.atleast_1d(np.asarray(angular_frequency, dtype=float))
    force_amplitude = np.broadcast_to(np.asarray(force_amplitude), angular_frequency.shape)
    omj = model['omega'][:n_modes]
    tip_phi = model['V'][model['tip_local'], :n_modes]
    denom = (omj[None, :]**2 - angular_frequency[:, None]**2
             + 2j*damping_ratio*angular_frequency[:, None]*omj[None, :])
    H = np.sum(tip_phi[None, :]**2/denom, axis=1)
    return abs(force_amplitude*H)


# Plot the operating range of the motor the student selected, plus a 15% margin.
# A dense sweep resolves narrow resonance peaks better than a short grid.
rpm = np.linspace(0.0, 1.15*p['rpm_high'], 4001)
Omega = 2*np.pi*rpm/60.0    # motor angular speed [rad/s]
operating = (rpm >= p['rpm_low']) & (rpm <= p['rpm_high'])

# CASE A — 1P rotating mass imbalance: lateral force in z, excitation Omega.
U = p['m_unbalance']*p['eccentricity']  # unbalance [kg*m]
F_1p = U*Omega**2
response_1p = tip_amplitude(motor_z, Omega, F_1p, p['zeta'], 3)

# CASE B — blade-passing-frequency (BPF) thrust ripple: vertical y force.
# Assumed nonzero only when
# unsteady aerodynamics make total thrust fluctuate; N blades alone do not
# guarantee a varying total thrust.
mean_thrust = p['T_ref']*(rpm/p['rpm_ref'])**2  # illustrative scaling
Omega_bpf = p['n_blades']*Omega
F_bpf = p['bpf_fraction']*mean_thrust
response_bpf = tip_amplitude(motor_y, Omega_bpf, F_bpf, p['zeta'], 3)

# CASE C — second harmonic of BPF: another assumed periodic vertical load.
Omega_2bpf = 2*p['n_blades']*Omega
F_2bpf = p['harmonic_fraction']*mean_thrust
response_2bpf = tip_amplitude(motor_y, Omega_2bpf, F_2bpf, p['zeta'], 3)
response_2bpf_one_mode = tip_amplitude(motor_y, Omega_2bpf, F_2bpf, p['zeta'], 1)

fig, ax = plt.subplots(figsize=(8.7, 4.7))
ax.plot(rpm, response_1p*1000, label='1P imbalance — lateral z', lw=1.8)
ax.plot(rpm, response_bpf*1000, label=f'{p["n_blades"]}P BPF — vertical y', lw=1.8)
ax.plot(rpm, response_2bpf*1000, label=f'{2*p["n_blades"]}P (2×BPF) — vertical y', lw=1.8)
ax.axvspan(p['rpm_low'], p['rpm_high'], color='gray', alpha=0.12,
           label='Assumed operating range')
ax.set(xlabel='Motor speed (rpm)', ylabel='Steady-state tip amplitude (mm)',
       title='Different excitation mechanisms and bending directions')
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()

# Separate vertical-only view: its hypothetical force amplitudes are much
# smaller than the imbalance case, so use micrometers instead of millimeters.
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(rpm, response_bpf*1e6, label='BPF: vertical y', lw=1.8)
ax.plot(rpm, response_2bpf*1e6, label='2×BPF: vertical y', lw=1.8)
ax.axvspan(p['rpm_low'], p['rpm_high'], color='gray', alpha=0.12)
ax.set(xlabel='Motor speed (rpm)', ylabel='Vertical tip amplitude (micrometers)',
       title='Vertical excitation: detail of thrust-ripple scenarios')
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(rpm, response_2bpf_one_mode*1e6, label='Vertical: first mode only')
ax.plot(rpm, response_2bpf*1e6, '--', label='Vertical: first three modes')
ax.axvspan(p['rpm_low'], p['rpm_high'], color='gray', alpha=0.12)
ax.set(xlabel='Motor speed (rpm)', ylabel='Vertical tip amplitude (micrometers)',
       title='2×BPF forcing: why higher modes matter')
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()

# How would blade count change excitation frequencies if thrust-ripple fraction
# and mean-thrust model were held fixed purely for comparison?
fig, ax = plt.subplots(figsize=(8, 4))
for nb in [2, 3]:
    amp = tip_amplitude(motor_y, nb*Omega, p['bpf_fraction']*mean_thrust,
                        p['zeta'], 3)
    ax.plot(rpm, 1e6*amp, label=f'{nb} blades: {nb}P')
ax.axvspan(p['rpm_low'], p['rpm_high'], color='gray', alpha=0.12)
ax.set(xlabel='Motor speed (rpm)', ylabel='Vertical tip amplitude (micrometers)',
       title='Illustrative effect of blade count on BPF frequency')
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()

print(f'\nPart 4 — Motor operating range: {p["rpm_low"]:.0f}–{p["rpm_high"]:.0f} rpm; {p["n_blades"]} blades')
# Every excitation is checked against each of the three retained bending modes.
print('Motor speed at which each excitation frequency equals a bending natural frequency')
excitations = [('1P', 1, fz, 'lateral'),
               (f'{p["n_blades"]}P (BPF)', p['n_blades'], fy, 'vertical'),
               (f'{2*p["n_blades"]}P (2×BPF)', 2*p['n_blades'], fy, 'vertical')]
for label, order, f_modes, direction in excitations:
    for j, f_mode in enumerate(f_modes):
        rpm_match = 60*f_mode/order
        inside = p['rpm_low'] <= rpm_match <= p['rpm_high']
        flag = '  <-- inside operating range' if inside else ''
        print(f'  {label:<11} {direction:<8} mode {j+1} ({f_mode:7.1f} Hz): '
              f'{rpm_match:8.0f} rpm{flag}')
peaks_mm = np.array([response_1p[operating].max(), response_bpf[operating].max(),
                     response_2bpf[operating].max()])*1000
# Significant figures, not fixed decimals: small peaks must not print as zero.
print(f'Peak amplitudes over {p["rpm_low"]:.0f}–{p["rpm_high"]:.0f} rpm, in mm:')
print(f'  1P lateral: {peaks_mm[0]:.4g}; BPF vertical: {peaks_mm[1]:.4g}; '
      f'2×BPF vertical: {peaks_mm[2]:.4g}')


# %% Part 5 — Compare length, width, and height changes
# Apply the SAME fractional increase to each dimension in turn.
# Only one dimension changes in each case; the motor mass stays fixed.
change_factor = 1.15       # keep at 1.15 for the required +15% comparison
cases = [('Length L', 'L'), ('Width bz', 'bz'), ('Height hy', 'hy')]
comparisons = []
for case_name, variable in cases:
    modified = dict(p)
    modified[variable] *= change_factor
    new_mass_g = 1000*modified['rho']*modified['bz']*modified['hy']*modified['L']
    new_fy = model_with_motor(modified, 'y', n_elem)['omega'][0]/(2*np.pi)
    new_fz = model_with_motor(modified, 'z', n_elem)['omega'][0]/(2*np.pi)
    pct_y = 100*(new_fy/fy[0] - 1)
    pct_z = 100*(new_fz/fz[0] - 1)
    comparisons.append((case_name, new_mass_g, new_fy, new_fz, pct_y, pct_z))
print('\nPart 5 — Compare three separate geometry changes')
print(f'Each case changes one dimension by +{100*(change_factor-1):.0f}% relative to baseline.')
print('Case           Mass (g)   Vertical (Hz)  Lateral (Hz)  Δvertical (%)  Δlateral (%)')
for name, mass_g, f_vert, f_lat, pct_vert, pct_lat in comparisons:
    print(f'{name:<13} {mass_g:8.3f} {f_vert:15.3f} {f_lat:13.3f}'
          f' {pct_vert:14.2f} {pct_lat:13.2f}')
print(f'Baseline       {1000*m_arm:8.3f} {fy[0]:15.3f} {fz[0]:13.3f}')
# Rank by the MEAN absolute percentage shift of the first frequencies.
# This compares the effect on BOTH bending directions, not design quality.
scores = [(abs(c[4]) + abs(c[5]))/2 for c in comparisons]
best_idx = int(np.argmax(scores))
selected_case = comparisons[best_idx]
print(f'Largest shift by this criterion: {selected_case[0]}')
print('For results.csv, report the mass and two frequencies of this selected case:')
print(f'  modified_beam_mass = {selected_case[1]:.3f} g')
print(f'  modified_f1_vertical = {selected_case[2]:.3f} Hz')
print(f'  modified_f1_lateral = {selected_case[3]:.3f} Hz')

# Optional 1-N structural reference: resonance curves depend on beam/motor,
# while the physical amplitudes above also depend on assumed force amplitudes.
# Computed values for results.csv (printouts above) are intentionally not
# written automatically, to retain the familiar individual CSV submission.
plt.show()
