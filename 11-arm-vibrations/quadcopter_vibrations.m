%% QUADCOPTER ARM VIBRATIONS — COMPUTATIONAL LAB (MATLAB R2024a+)
% Follow README.md Parts 1–5. Run the entire script.
% Local helper functions appear beside the corresponding section.
% For older MATLAB versions, move local functions to the end of the file.
% x along arm, y vertical, z lateral; solid constant rectangular section.
% One short coding task appears in Part 2 (adding motor point mass).
clear; clc; close all;

%% Part 1 — Geometry and physical parameters
% Part 1 action: Replace L, bz, hy, E, rho, and motorMass with your values.
% Use a uniform solid rectangle; state approximations in reflection Q1.
% Other numerical/excitation inputs are illustrative defaults.
p.L = 0.22;             % arm length [m]
p.bz = 0.016;           % solid rectangle width in lateral z [m]
p.hy = 0.008;           % solid rectangle height in vertical y [m]
p.E = 70e9;             % beam Young modulus [Pa]
p.rho = 2700;           % beam material density only [kg/m^3]
p.motorMass = 0.055;    % point mass at free arm tip [kg]
p.zeta = 0.03;          % assumed modal damping ratio [-]
p.rpmLow = 3500;        % SET from YOUR motor: lower operating speed [rpm]
p.rpmHigh = 12500;      % SET from YOUR motor: upper operating speed [rpm]
p.mUnbalance = 0.00015; % hypothetical eccentric mass [kg]
p.eccentricity = 0.002;% distance from spin axis [m]
p.nBlades = 2;          % SET from YOUR propeller: number of blades
p.Tref = 3.0;           % assumed mean thrust [N] at midpoint of selected RPM range
p.bpfFraction = 0.02;   % assumed blade-passing-frequency (BPF) thrust ripple / mean thrust
p.harmonicFraction = 0.004; % assumed 2*BPF thrust ripple / mean thrust
% Reference speed for illustrative thrust model (not measured motor data).
assert(p.rpmLow > 0 && p.rpmHigh > p.rpmLow, ...
    'Set rpmLow and rpmHigh to a positive increasing range for your motor.');
assert(p.nBlades >= 1 && p.nBlades == round(p.nBlades), ...
    'nBlades must be a positive integer.');
p.rpmRef = (p.rpmLow+p.rpmHigh)/2;
nElem = 12;             % number of short elements used to represent beam

A = p.bz*p.hy;            % uniform solid rectangular beam area [m^2]
Iy = p.hy*p.bz^3/12;      % lateral z bending: bend around y [m^4]
Iz = p.bz*p.hy^3/12;      % vertical y bending: bend around z [m^4]
mu = p.rho*A;            % Beam mass per length [kg/m]; does not include motor
mArm = mu*p.L;           % total beam mass [kg]
fprintf('Part 1 — Uniform solid rectangular arm\n');
fprintf('A = %.6g m^2, Iy = %.6g m^4, Iz = %.6g m^4\n',A,Iy,Iz);
fprintf('rho = %.1f kg/m^3 (beam only), mu = %.4f kg/m\n',p.rho,mu);
fprintf('Arm mass = %.3f g; motor point mass = %.3f g\n',1000*mArm,1000*p.motorMass);
% Equivalent tip stiffness / effective mass from the earlier spring-mass model.
mEffectiveBare = (33/140)*mArm;
mEffectiveMotor = p.motorMass + mEffectiveBare;
kY = 3*p.E*Iz/p.L^3;
kZ = 3*p.E*Iy/p.L^3;
fBareEstY = sqrt(kY/mEffectiveBare)/(2*pi);
fBareEstZ = sqrt(kZ/mEffectiveBare)/(2*pi);
fMotorEstY = sqrt(kY/mEffectiveMotor)/(2*pi);
fMotorEstZ = sqrt(kZ/mEffectiveMotor)/(2*pi);
fprintf('Bare beam estimates: vertical %.3f Hz; lateral %.3f Hz\n',fBareEstY,fBareEstZ);
fprintf('With motor estimates: vertical %.3f Hz; lateral %.3f Hz\n',fMotorEstY,fMotorEstZ);
fprintf('Part 1 reporting (reflection Q1 only): chosen inputs, four approximate\n');
fprintf('frequencies (bare/with motor, vertical/lateral) and their differences.\n');

%% Part 2 — Beam finite elements, before and after adding motor mass
% In the lecture's two-mass, three-spring model, fixed outer walls held
% springs 1 and 3; each moving mass also connects to middle spring 2.
% A moving mass receives restoring forces from both attached springs.
% Here, neighboring beam elements likewise contribute at shared nodes.
% The assembly and eigensolver are supplied.
[K_y,M_y] = assembleBeam(p,'y',nElem);
[K_z,M_z] = assembleBeam(p,'z',nElem);
bareY = findModes(K_y,M_y,nElem);
bareZ = findModes(K_z,M_z,nElem);
fprintf('\nPart 2 — First frequency before attaching the motor\n');
fprintf('Bare beam, vertical y bending: %.3f Hz\n',bareY.omega(1)/(2*pi));
fprintf('Bare beam, lateral z bending:  %.3f Hz\n',bareZ.omega(1)/(2*pi));

M_y_motor = M_y; M_z_motor = M_z;
tipPosition = 2*nElem+1; % position of free-end displacement (not slope)
% Part 2 coding task: uncomment the two lines below, then DELETE the error.
% Add the motor mass to the tip displacement entry in both bending models.
% Do not change K_y or K_z. This is one physical motor, not two motors.
% M_y_motor(tipPosition,tipPosition) = M_y_motor(tipPosition,tipPosition) + p.motorMass;
% M_z_motor(tipPosition,tipPosition) = M_z_motor(tipPosition,tipPosition) + p.motorMass;
error('Part 2 coding task: enable the two mass-addition lines');

motorY = findModes(K_y,M_y_motor,nElem);
motorZ = findModes(K_z,M_z_motor,nElem);
fprintf('First frequency with motor point mass\n');
fprintf('With motor, vertical y bending: %.3f Hz\n',motorY.omega(1)/(2*pi));
fprintf('With motor, lateral z bending:  %.3f Hz\n',motorZ.omega(1)/(2*pi));

% Supporting functions for Part 2 are placed here (MATLAB R2024a+).
function [Ke,Me] = elementMatrices(EI,mu,ell)
    % EI: bending rigidity [N*m^2], ell: one beam element length [m].
    % End values: [deflection-left, slope-left, deflection-right, slope-right]
    Ke = EI/ell^3*[12, 6*ell, -12, 6*ell; ...
                   6*ell, 4*ell^2, -6*ell, 2*ell^2; ...
                   -12, -6*ell, 12, -6*ell; ...
                   6*ell, 2*ell^2, -6*ell, 4*ell^2];
    Me = mu*ell/420*[156, 22*ell, 54, -13*ell; ...
                     22*ell, 4*ell^2, 13*ell, -3*ell^2; ...
                     54, 13*ell, 156, -22*ell; ...
                     -13*ell, -3*ell^2, -22*ell, 4*ell^2];
end

function [K,M] = assembleBeam(p,direction,n)
    area = p.bz*p.hy;
    muBeam = p.rho*area;           % kg/m, uniform beam only
    if strcmp(direction,'y')      % vertical y deflection: bending around z
        I = p.bz*p.hy^3/12;
    else                          % lateral z deflection: bending around y
        I = p.hy*p.bz^3/12;
    end
    ell = p.L/n;                 % length of one short beam element [m]
    [Ke,Me] = elementMatrices(p.E*I,muBeam,ell);
    K = zeros(2*(n+1)); M = zeros(2*(n+1));
    for element = 1:n
        positions = [2*element-1,2*element,2*element+1,2*element+2];
        K(positions,positions) = K(positions,positions) + Ke;
        M(positions,positions) = M(positions,positions) + Me;
    end
end

function model = findModes(K,M,n)
    free = 3:size(K,1);       % clamp root displacement and slope = 0
    Kff = K(free,free); Mff = M(free,free);
    [V,D] = eig(Kff,Mff);
    [lam,ord] = sort(real(diag(D)),'ascend');
    V = real(V(:,ord));
    assert(all(lam > 0),'A nonpositive eigenvalue was found.');
    for j = 1:size(V,2)
        V(:,j) = V(:,j)/sqrt(V(:,j)'*Mff*V(:,j));
    end
    tipPosition = 2*n+1;
    tipLocal = find(free==tipPosition,1);
    model = struct('K',K,'M',M,'Kff',Kff,'Mff',Mff,'free',free, ...
                   'V',V,'omega',sqrt(lam),'tipLocal',tipLocal, ...
                   'tipPosition',tipPosition,'nElements',n);
end

%% Part 3 — Natural frequencies, mode shapes, convergence
fy = motorY.omega(1:3)/(2*pi);
fz = motorZ.omega(1:3)/(2*pi);
fprintf('\nPart 3 — First three natural frequencies with motor\n');
for j = 1:3
    fprintf('Mode %d: vertical %9.3f Hz; lateral %9.3f Hz\n',j,fy(j),fz(j));
end
figure('Name','Vertical bending modes'); hold on;
for j = 1:3
    [x,w] = modeCurve(motorY,j,p.L,30);
    plot(x/p.L,w,'LineWidth',1.8, ...
         'DisplayName',sprintf('Mode %d: %.1f Hz',j,fy(j)));
end
xlabel('Position along arm, x/L');
ylabel('Mode shape (normalized displacement)');
title('Vertical bending: first three mode shapes');
yline(0,':','HandleVisibility','off'); legend('Location','best'); grid on;

meshSizes = [2,4,8,16,32];
convY = zeros(numel(meshSizes),3);
for k = 1:numel(meshSizes)
    modl = modelWithMotor(p,'y',meshSizes(k));
    convY(k,:) = modl.omega(1:3).'/(2*pi);
end
fprintf('\nMesh convergence: vertical natural frequencies (Hz)\n');
fprintf('Elements       f1        f2        f3\n');
for k = 1:numel(meshSizes)
    fprintf('%8d  %8.2f  %8.2f  %8.2f\n',meshSizes(k),convY(k,:));
end
figure('Name','Frequency convergence'); hold on;
for j = 1:3
    plot(meshSizes,convY(:,j),'o-','LineWidth',1.5, ...
         'DisplayName',sprintf('Mode %d',j));
end
xlabel('Number of beam elements'); ylabel('Natural frequency (Hz)');
title('Mesh convergence: vertical bending'); legend('Location','best'); grid on;

% Supporting functions for Part 3.
function [xCurve,wCurve] = modeCurve(model,j,L,nPoints)
    n = model.nElements; ell = L/n;
    q = zeros(2*(n+1),1);
    q(model.free) = model.V(:,j);
    xCurve = []; wCurve = [];
    for e = 1:n
        xi = linspace(0,1,nPoints+1);
        N1 = 1-3*xi.^2+2*xi.^3;
        N2 = ell*(xi-2*xi.^2+xi.^3);
        N3 = 3*xi.^2-2*xi.^3;
        N4 = ell*(-xi.^2+xi.^3);
        positions = [2*e-1,2*e,2*e+1,2*e+2];
        u = q(positions);
        w = u(1)*N1+u(2)*N2+u(3)*N3+u(4)*N4;
        if e>1
            xi = xi(2:end); w = w(2:end);
        end
        xCurve = [xCurve, (e-1+xi)*ell]; %#ok<AGROW>
        wCurve = [wCurve, w]; %#ok<AGROW>
    end
    if wCurve(end)<0, wCurve = -wCurve; end
    wCurve = wCurve/max(abs(wCurve));
end

function model = modelWithMotor(p,direction,n)
    [K,M] = assembleBeam(p,direction,n);
    M(2*n+1,2*n+1) = M(2*n+1,2*n+1) + p.motorMass;
    model = findModes(K,M,n);
end

%% Part 4 — Motor imbalance and blade-passing excitation
% BPF = blade-passing frequency; 1P = once per rotor revolution.
% The plot extends 15% above YOUR selected motor operating RPM range.
rpm = linspace(0,1.15*p.rpmHigh,4001);
Omega = 2*pi*rpm/60;        % actual motor angular speed [rad/s]
selected = rpm>=p.rpmLow & rpm<=p.rpmHigh;

% 1P: rotating imbalance creates lateral z force at motor RPM frequency.
U = p.mUnbalance*p.eccentricity;       % mass unbalance [kg*m]
F1P = U*Omega.^2;
response1P = tipAmplitude(motorZ,Omega,F1P,p.zeta,3);

% Blade-passing frequency (BPF): hypothetical vertical thrust ripple.
% The blade count by
% itself does not imply the total thrust varies; see README discussion.
meanThrust = p.Tref*(rpm/p.rpmRef).^2; % assumed average thrust [N]
OmegaBPF = p.nBlades*Omega;
FBPF = p.bpfFraction*meanThrust;
responseBPF = tipAmplitude(motorY,OmegaBPF,FBPF,p.zeta,3);

% Second BPF harmonic: hypothetical additional periodic vertical forcing.
Omega2BPF = 2*p.nBlades*Omega;
F2BPF = p.harmonicFraction*meanThrust;
response2BPF = tipAmplitude(motorY,Omega2BPF,F2BPF,p.zeta,3);
response2BPFoneMode = tipAmplitude(motorY,Omega2BPF,F2BPF,p.zeta,1);

figure('Name','Comparison of motor-induced vibration scenarios'); hold on;
plot(rpm,1000*response1P,'LineWidth',1.8,'DisplayName','1P imbalance: lateral z');
plot(rpm,1000*responseBPF,'LineWidth',1.8, ...
     'DisplayName',sprintf('%dP BPF: vertical y',p.nBlades));
plot(rpm,1000*response2BPF,'LineWidth',1.8, ...
     'DisplayName',sprintf('%dP (2xBPF): vertical y',2*p.nBlades));
xline(p.rpmLow,':','HandleVisibility','off');
xline(p.rpmHigh,':','HandleVisibility','off');
xlabel('Motor speed (rpm)'); ylabel('Steady-state tip amplitude (mm)');
title('Different excitation mechanisms and bending directions');
legend('Location','best'); grid on;

% Separate vertical-only plot: these amplitudes are far smaller than 1P.
% Use micrometers, not millimeters, to make small peaks visible.
figure('Name','Vertical thrust-ripple details'); hold on;
plot(rpm,1e6*responseBPF,'LineWidth',1.8,'DisplayName','BPF: vertical y');
plot(rpm,1e6*response2BPF,'LineWidth',1.8,'DisplayName','2xBPF: vertical y');
xline(p.rpmLow,':','HandleVisibility','off');
xline(p.rpmHigh,':','HandleVisibility','off');
xlabel('Motor speed (rpm)'); ylabel('Vertical tip amplitude (micrometers)');
title('Vertical excitation: thrust-ripple details');
legend('Location','best'); grid on;

figure('Name','Higher modes with blade-passing harmonics'); hold on;
plot(rpm,1e6*response2BPFoneMode,'LineWidth',1.8, ...
     'DisplayName','First vertical mode only');
plot(rpm,1e6*response2BPF,'--','LineWidth',1.8, ...
     'DisplayName','First three vertical modes');
xline(p.rpmLow,':','HandleVisibility','off');
xline(p.rpmHigh,':','HandleVisibility','off');
xlabel('Motor speed (rpm)'); ylabel('Vertical tip amplitude (micrometers)');
title('2xBPF thrust ripple: effect of higher bending modes');
legend('Location','best'); grid on;

figure('Name','Blade-count comparison'); hold on;
for nb = [2,3]
    a = tipAmplitude(motorY,nb*Omega,p.bpfFraction*meanThrust,p.zeta,3);
    plot(rpm,1e6*a,'LineWidth',1.8, ...
         'DisplayName',sprintf('%d blades: %dP',nb,nb));
end
xline(p.rpmLow,':','HandleVisibility','off');
xline(p.rpmHigh,':','HandleVisibility','off');
xlabel('Motor speed (rpm)'); ylabel('Vertical tip amplitude (micrometers)');
title('Illustrative effect of blade count on BPF frequency');
legend('Location','best'); grid on;

fprintf('\nPart 4 — Motor operating range: %.0f to %.0f rpm, %d blades\n', ...
    p.rpmLow,p.rpmHigh,p.nBlades);
% Every excitation is checked against each of the three retained bending modes.
fprintf('Motor speed at which each excitation frequency equals a bending natural frequency\n');
excLabels = {'1P', sprintf('%dP (BPF)',p.nBlades), sprintf('%dP (2xBPF)',2*p.nBlades)};
excOrders = [1, p.nBlades, 2*p.nBlades];
excDirections = {'lateral','vertical','vertical'};
excModes = {fz, fy, fy};
for k = 1:3
    for j = 1:3
        rpmMatch = 60*excModes{k}(j)/excOrders(k);
        if rpmMatch >= p.rpmLow && rpmMatch <= p.rpmHigh
            rangeNote = '  <-- inside operating range';
        else
            rangeNote = '';
        end
        fprintf('  %-11s %-8s mode %d (%7.1f Hz): %8.0f rpm%s\n', ...
            excLabels{k},excDirections{k},j,excModes{k}(j),rpmMatch,rangeNote);
    end
end
% Significant figures, not fixed decimals: small peaks must not print as zero.
fprintf('Peak amplitudes from %.0f to %.0f rpm (mm):\n',p.rpmLow,p.rpmHigh);
fprintf('  1P lateral: %.4g; BPF vertical: %.4g; 2xBPF vertical: %.4g\n', ...
        1000*max(response1P(selected)),1000*max(responseBPF(selected)), ...
        1000*max(response2BPF(selected)));

% Supporting function for Part 4.
function amplitude = tipAmplitude(model,omegaExc,forceAmplitude,zeta,nModes)
    omegaExc = omegaExc(:);
    if isscalar(forceAmplitude)
        forceAmplitude = forceAmplitude + zeros(size(omegaExc));
    else
        forceAmplitude = forceAmplitude(:);
    end
    assert(numel(omegaExc) == numel(forceAmplitude));
    r = min(nModes,numel(model.omega));
    omJ = model.omega(1:r);
    phiTip = model.V(model.tipLocal,1:r).';
    amplitude = zeros(size(omegaExc));
    for k = 1:numel(omegaExc)
        w = omegaExc(k);
        denom = omJ.^2 - w^2 + 2i*zeta*omJ*w;
        H = sum(phiTip.^2./denom);
        amplitude(k) = abs(forceAmplitude(k)*H);
    end
end

%% Part 5 — Compare three geometry changes
% Increase one dimension by the same factor in each separate scenario.
% The remaining dimensions and the motor mass are unchanged in each case.
changeFactor = 1.15;  % keep +15% for the required three-case comparison
caseLabels = {'Length L','Width bz','Height hy'};
caseFields = {'L','bz','hy'};
caseResults = zeros(3,5); % mass g, f_y Hz, f_z Hz, percent y, percent z
for k = 1:3
    modified = p;
    field = caseFields{k};
    modified.(field) = p.(field)*changeFactor;
    massG = 1000*modified.rho*modified.bz*modified.hy*modified.L;
    modY = modelWithMotor(modified,'y',nElem);
    modZ = modelWithMotor(modified,'z',nElem);
    fVert = modY.omega(1)/(2*pi);
    fLat = modZ.omega(1)/(2*pi);
    percentVert = 100*(fVert/fy(1)-1);
    percentLat = 100*(fLat/fz(1)-1);
    caseResults(k,:) = [massG,fVert,fLat,percentVert,percentLat];
end
fprintf('\nPart 5 — Three separate changes, each +%.0f%%\n',100*(changeFactor-1));
fprintf('Case           Mass (g)  Vertical (Hz) Lateral (Hz)  dVert (%%) dLat (%%)\n');
for k = 1:3
    fprintf('%-13s %8.3f %14.3f %12.3f %11.2f %8.2f\n', ...
        caseLabels{k},caseResults(k,:));
end
fprintf('Baseline       %8.3f %14.3f %12.3f\n',1000*mArm,fy(1),fz(1));
% Most sensitive case: largest MEAN absolute percentage shift across both modes.
% A large change is not automatically a better design.
score = mean(abs(caseResults(:,4:5)),2);
[~,chosen] = max(score);
fprintf('Largest shift by this criterion: %s\n',caseLabels{chosen});
fprintf('For results.csv, report this selected case:\n');
fprintf('  modified_beam_mass = %.3f g\n',caseResults(chosen,1));
fprintf('  modified_f1_vertical = %.3f Hz\n',caseResults(chosen,2));
fprintf('  modified_f1_lateral = %.3f Hz\n',caseResults(chosen,3));
