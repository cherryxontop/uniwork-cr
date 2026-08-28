from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr, constants, stats
from uncertainties import ufloat

MAGNET = "large"

# CALIBRATION DATA (from the supplied spreadsheet)

mu_0 = constants.mu_0

calib_z_cm = {
    "large": np.array([14, 13, 12, 11, 10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3]),
    "small": np.array([10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3]),
}
calib_B_mT = {
    "large": np.array([0.021, 0.049, 0.098, 0.153, 0.245, 0.318, 0.385, 0.466, 0.527,
                        0.671, 0.797, 1.01, 1.23, 1.65, 2.16, 2.95, 3.89, 5.16, 7.49]),
    "small": np.array([0.234, 0.267, 0.309, 0.345, 0.402, 0.493, 0.542, 0.663, 0.791,
                        0.98, 1.19, 1.52, 2.05, 2.73, 4.16]),
}
sigma_z_cm = 0.2   # given uncertainty on z
sigma_B_mT = 0.005  # given uncertainty on B



# uncerts

sigma_N_turns = 1          # miscounting a partial turn, etc.
sigma_R_cm = 0.25          # ruler 
sigma_h_cm = 0.25          # ruler reading on drop height (for computing s)
sigma_emf_frac = 0.02      # fractional oscilloscope voltage reading uncertainty
sigma_emf_floor = 0.01     # absolute floor (smallest division / last digit), V

# FUNCS

@dataclass
class odr_fit_result:
    parameters: np.ndarray
    parameter_errors: np.ndarray
    r_squared: float
    rmse: float
    reduced_chi_squared: float
    converged: bool
    x_nom: np.ndarray
    y_nom: np.ndarray
    x_err: np.ndarray
    y_err: np.ndarray


def odr_fit(x: list[ufloat], y: list[ufloat], model_func, beta0: list[float]) -> odr_fit_result:
    x_nom = np.array([v.n for v in x])
    x_err = np.array([v.s for v in x])
    y_nom = np.array([v.n for v in y])
    y_err = np.array([v.s for v in y])

    data = odr.RealData(x_nom, y_nom, sx=x_err, sy=y_err)
    model = odr.Model(model_func)
    odr_result = odr.ODR(data, model, beta0=beta0).run()

    parameters = odr_result.beta
    parameter_errors = odr_result.sd_beta
    converged = odr_result.info in (1, 2, 3)
    if not converged:
        print(f"did not converge (info={odr_result.info})")

    y_pred = model_func(parameters, x_nom)
    residuals = y_nom - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_nom - np.mean(y_nom)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan
    rmse = np.sqrt(np.mean(residuals**2))
    reduced_chi_squared = odr_result.res_var

    return odr_fit_result(
        parameters=parameters,
        parameter_errors=parameter_errors,
        r_squared=r_squared,
        rmse=rmse,
        reduced_chi_squared=reduced_chi_squared,
        converged=converged,
        x_nom=x_nom,
        y_nom=y_nom,
        x_err=x_err,
        y_err=y_err,
    )


def chi_squared_test(chi2_stat, dof):
    p_value = stats.chi2.sf(chi2_stat, dof)
    print(f"chi-squared: {chi2_stat:.3f}  (dof = {dof})")
    print(f"reduced chi-squared: {chi2_stat/dof:.3f}")
    print(f"p-value: {p_value:.4f}")
    if p_value > 0.05:
        print("results AGREE with the model (p > 0.05)")
    else:
        print("results DISAGREE with the model (p <= 0.05)")
    return p_value


def sigma_test(k1, sk1, k2, sk2, label="parameter"):
    sigma_diff = abs(k1 - k2) / np.sqrt(sk1**2 + sk2**2)

    print(f"\nSIGMA TEST ({label})")
    print(f"measured value    : {k1:.3f} +/- {sk1:.3f}")
    print(f"theoretical value : {k2:.3f} +/- {sk2:.3f}")
    print(f"discrepancy       : {sigma_diff:.2f} sigma")

    if sigma_diff <= 3.0:
        print("results AGREE within experimental uncertainty")
    else:
        print("results DISAGREE")

    return sigma_diff



# CALIBRATE DIPOLE MOMENT

def dipole_field_model(p, z):
    m = p[0]
    return (mu_0 / (2 * np.pi)) * m / z ** 3

z_calib = [ufloat(z / 100, sigma_z_cm / 100) for z in calib_z_cm[MAGNET]]
B_calib = [ufloat(B / 1000, sigma_B_mT / 1000) for B in calib_B_mT[MAGNET]]

calib_result = odr_fit(z_calib, B_calib, dipole_field_model, beta0=[1.0])
m_dipole = calib_result.parameters[0]
sigma_m = calib_result.parameter_errors[0]

print(f"~~~DIPOLE MOMENT CALIBRATION ({MAGNET} magnet)~~~")
print(f"m = {m_dipole:.4f} +/- {sigma_m:.4f} A m^2")
print(f"R^2 = {calib_result.r_squared:.4f}")

dof_calib = len(z_calib) - 1
chi2_calib = calib_result.reduced_chi_squared * dof_calib
chi_squared_test(chi2_calib, dof_calib)

z_fit = np.linspace(min(calib_result.x_nom), max(calib_result.x_nom), 200)

plt.figure(figsize=(7, 5))
plt.errorbar(calib_result.x_nom, calib_result.y_nom,
             xerr=calib_result.x_err, yerr=calib_result.y_err,
             fmt="o", capsize=3, label="Calibration Data")
plt.plot(z_fit, dipole_field_model(calib_result.parameters, z_fit), "k--",
          label=f"Point-dipole fit ($\\chi_v^2$ = {calib_result.reduced_chi_squared:.2f})")
plt.xlabel("Axial distance $z$ (m)")
plt.ylabel("Field $B$ (T)")
plt.title(f"Dipole Field Calibration ({MAGNET} magnet)")
plt.grid(True, alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/dipole_calibration_fit.png", dpi=300)
plt.show()

calib_residuals = calib_result.y_nom - dipole_field_model(calib_result.parameters, calib_result.x_nom)
plt.figure(figsize=(7, 4))
plt.errorbar(calib_result.x_nom, calib_residuals, yerr=calib_result.y_err,
             fmt="o", capsize=3, color="crimson")
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Axial distance $z$ (m)")
plt.ylabel("Residual (T)")
plt.title(f"Dipole Field Calibration Residuals ({MAGNET} magnet)")
plt.grid(True, alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/dipole_calibration_residuals.png", dpi=300)
plt.show()



# PREDICTION


PEAK_EMF_COEFF = 1.5 * (4 / 5) ** 2.5  # ~0.859

def theory_emf_peak(N, v, R):
    return PEAK_EMF_COEFF * N * v * mu_0 * m_dipole / R ** 2


def compare_to_theory(x_vals, y_measured_v, y_theory, xlabel, title, filename_prefix):
    """Compares measured peak emf against the zero-free-parameter theory
    prediction. No fitting happens here - y_theory is computed directly
    from theory (elementwise, so a per-trial speed can be used where that
    varies), then chi_squared_test/sigma_test report how well the DATA
    agrees with those fixed values."""
    x_nom = np.array([v.n for v in x_vals])
    x_err = np.array([v.s for v in x_vals])
    sigma_y = y_measured_v * sigma_emf_frac + sigma_emf_floor
    y_nom = y_measured_v

    residuals = y_nom - y_theory

    chi2_stat = np.sum((residuals / sigma_y) ** 2)
    dof = len(x_nom)  # zero free parameters were fit to this data
    print(f"\n~~~{title.upper()}~~~")
    chi_squared_test(chi2_stat, dof)

    # weighted mean of (data / theory) as a simple, non-fitted diagnostic -
    # should be consistent with 1.0 if theory and data agree overall
    ratio = y_nom / y_theory
    ratio_err = ratio * (sigma_y / y_nom)
    weights = 1 / ratio_err ** 2
    mean_ratio = np.sum(ratio * weights) / np.sum(weights)
    mean_ratio_err = 1 / np.sqrt(np.sum(weights))
    sigma_test(mean_ratio, mean_ratio_err, 1.0, 0.0, label=f"{title}: data/theory ratio")

    # theory plotted as a line through the actual computed points (sorted by
    # x) rather than an idealised smooth curve - honest even when v isn't
    # the same at every point (e.g. the varying-R sub-experiment)
    order = np.argsort(x_nom)

    plt.figure(figsize=(7, 5))
    plt.errorbar(x_nom, y_nom, xerr=x_err, yerr=sigma_y, fmt="o", capsize=3,
                 label="Experimental Data (Oscilloscope)")
    plt.plot(x_nom[order], y_theory[order], "k--o", markersize=4,
             label="Theory (no free parameters)")
    plt.xlabel(xlabel)
    plt.ylabel("Peak emf $\\varepsilon$ (V)")
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{filename_prefix}_fit.png", dpi=300)
    plt.show()

    plt.figure(figsize=(7, 4))
    plt.errorbar(x_nom, residuals, yerr=sigma_y, fmt="o", capsize=3, color="crimson")
    plt.axhline(0, color="black", linestyle="--")
    plt.xlabel(xlabel)
    plt.ylabel("Residual (V)")
    plt.title(f"{title} - Residuals")
    plt.grid(True, alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{filename_prefix}_residuals.png", dpi=300)
    plt.show()

"""
#emf vs number of turns N

R_fixed_N = ufloat(((4.8+4.3)/2)/2, sigma_R_cm) / 100   # m
h_fixed_N = ufloat(20.0, sigma_h_cm) / 100   # m
v_fixed_N = np.sqrt(2 * constants.g * h_fixed_N.n)  # speed at coil, from free fall

turns_list = []
turns_N = [ufloat(n, sigma_N_turns) for n in turns_list]
emf_vs_N_measured = np.array([])  # V - one peak reading per turn count, same convention as R/s below

y_theory_N = np.array([theory_emf_peak(N, v_fixed_N, R_fixed_N.n) for N in turns_list])
compare_to_theory(turns_N, emf_vs_N_measured, y_theory_N,
                  xlabel="Number of turns $N$", title="Peak emf vs Number of Turns",
                  filename_prefix="graphs/emf_vs_N"
                  )
"""

# emf vs coil radius R
# north side up
N_fixed_R = 10
h = [48.3, 49.4, 49.2, 49.1, 49.2]  # cm, per-trial drop height to respective coil

outer_d_cm = [2.5, 3.4, 4.8, 6, 8.9]
inner_d_cm = [2.1, 3, 4.3, 5.5, 8.7]
radii_cm = [(o + i) / 4 for o, i in zip(outer_d_cm, inner_d_cm)]  # mean radius per trial
radii_R = [ufloat(r / 100, sigma_R_cm / 100) for r in radii_cm]  # m

print(radii_R)

heights_R = [ufloat(hi / 100, sigma_h_cm / 100) for hi in h]
speeds_R = [np.sqrt(2 * constants.g * hh.n) for hh in heights_R]  # v per trial, from that trial's height

emf_vs_R_measured = np.array([172, 124, 68, 44.8, 26.4]) / 2 / 1000  # pk-pk mV -> single-peak V

y_theory_R = np.array([theory_emf_peak(N_fixed_R, v, R.n)
                        for v, R in zip(speeds_R, radii_R)])

compare_to_theory(
    radii_R, emf_vs_R_measured, y_theory_R,
    xlabel="Coil radius $R$ (m)", title="Peak emf vs Coil Radius",
    filename_prefix="graphs/emf_vs_R",
)


# emf vs magnet speed s

N_fixed_s = 10
R_fixed_s = ufloat(((3.4 + 3) / 2) / 2, sigma_R_cm) / 100  # m

heights_cm = [48.4, 49.4, 50.4, 51.4, 52.4, 53.4, 54.4, 55.4, 56.4, 57.4, 58.4]  # cm
heights_m = [ufloat(hh / 100, sigma_h_cm / 100) for hh in heights_cm]
speeds_s = [ufloat(np.sqrt(2 * constants.g * hh.n),
                    constants.g * hh.s / np.sqrt(2 * constants.g * hh.n)) for hh in heights_m]

emf_vs_s_measured = np.array([122, 124, 128, 120, 130, 140, 140, 140, 146, 160, 168]) / 2 / 1000  # pkpk mV -> V

y_theory_s = np.array([theory_emf_peak(N_fixed_s, v.n, R_fixed_s.n) for v in speeds_s])

compare_to_theory(
    speeds_s, emf_vs_s_measured, y_theory_s,
    xlabel="Magnet speed $s$ (m/s)", title="Peak emf vs Magnet Speed",
    filename_prefix="graphs/emf_vs_s",
)

"""
print("\n\n~~~ALL MEASUREMENTS~~~")

print("\n-- Coil radius (R) sub-experiment --")
print(f"{'trial':>5} {'outer_d(cm)':>12} {'inner_d(cm)':>12} {'R(cm)':>8} {'h(cm)':>8} {'v(m/s)':>8} {'emf(mV pk-pk)':>14} {'emf(V, peak)':>13}")
for i in range(len(radii_cm)):
    print(f"{i+1:>5} {outer_d_cm[i]:>12} {inner_d_cm[i]:>12} {radii_cm[i]:>8.3f} {h[i]:>8} "
          f"{speeds_R[i]:>8.3f} {emf_vs_R_measured[i]*2000:>14.1f} {emf_vs_R_measured[i]:>13.4f}")
print(f"held fixed: N = {N_fixed_R}")

print("\n-- Magnet speed (s) sub-experiment --")
print(f"{'trial':>5} {'h(cm)':>8} {'v(m/s)':>8} {'emf(mV)':>10} {'emf(V)':>10}")
for i in range(len(heights_cm)):
    print(f"{i+1:>5} {heights_cm[i]:>8} {speeds_s[i].n:>8.3f} "
          f"{emf_vs_s_measured[i]*1000:>10.1f} {emf_vs_s_measured[i]:>10.4f}")
print(f"held fixed: N = {N_fixed_s}, R = {R_fixed_s.n*100:.3f} +/- {R_fixed_s.s*100:.3f} cm")

print(f"\n-- Dipole calibration --")
print(f"magnet = {MAGNET}, m = {m_dipole:.4f} +/- {sigma_m:.4f} A m^2")
"""

# TO DO :
# USE CURSOR TO CHECK THE V = ACCURATE
# TAKE CARE OF HEIGHT
# TAKE LARGER INTERVALS THAN 1 CM in varying height
