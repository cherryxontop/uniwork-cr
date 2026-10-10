from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr, constants, stats
from uncertainties import ufloat


# CALIBRATION DATA (from the supplied spreadsheet, large magnet)

mu_0 = constants.mu_0

calib_z_cm = np.array([14, 13, 12, 11, 10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3])
calib_B_mT = np.array([0.021, 0.049, 0.098, 0.153, 0.245, 0.318, 0.385, 0.466, 0.527,
                        0.671, 0.797, 1.01, 1.23, 1.65, 2.16, 2.95, 3.89, 5.16, 7.49])
sigma_z_cm = 0.2   # given uncertainty on z
sigma_B_mT = 0.005  # given uncertainty on B


# uncerts

sigma_N_turns = 1          # miscounting a partial turn, etc.
sigma_R_cm = 0.25          # ruler read in 0.5 cm increments, so half that
sigma_h_cm = 0.25          # ruler read in 0.5 cm increments, so half that
sigma_emf_frac = 0.02      # 2% of oscilloscope voltage reading

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



# CALIBRATE THE DIPOLE MOMENT m

z_m = calib_z_cm / 100
B_T = calib_B_mT / 1000

k_values = B_T * z_m ** 3           # should be ~constant if B = k/z^3 holds
k_mean = k_values.mean()
k_err = k_values.std(ddof=1) / np.sqrt(len(k_values))  # standard error of the mean

m_dipole = k_mean * 2 * np.pi / mu_0
sigma_m = k_err * 2 * np.pi / mu_0

print(f"~~~DIPOLE MOMENT CALIBRATION~~~")
print(f"m = {m_dipole:.4f} +/- {sigma_m:.4f} A m^2")
print(f"k values (should be roughly constant): {k_values}")
print(f"spread: {k_values.std(ddof=1)/k_mean*100:.1f}% of the mean")

z_smooth = np.linspace(min(z_m), max(z_m), 200)
B_theory = (mu_0 / (2 * np.pi)) * m_dipole / z_smooth ** 3

plt.figure(figsize=(7, 5))
plt.errorbar(z_m, B_T, xerr=sigma_z_cm / 100, yerr=sigma_B_mT / 1000,
             fmt="o", capsize=3, label="Calibration Data")
plt.plot(z_smooth, B_theory, "k--", label="Predicted (point-dipole, $z^{-3}$)")
plt.xlabel("Axial distance $z$ (m)")
plt.ylabel("Field $B$ (T)")
plt.title("Dipole Field: Data vs Predicted Curve")
plt.grid(True, alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/dipole_calibration_fit.png", dpi=300)
plt.show()

B_predicted_at_data = (mu_0 / (2 * np.pi)) * m_dipole / z_m ** 3
calib_residuals = B_T - B_predicted_at_data
plt.figure(figsize=(7, 4))
plt.errorbar(z_m, calib_residuals, yerr=sigma_B_mT / 1000, fmt="o", capsize=3, color="crimson")
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Axial distance $z$ (m)")
plt.ylabel("Residual (T)")
plt.title("Dipole Field Calibration Residuals (large magnet)")
plt.grid(True, alpha=0.6)
plt.tight_layout()
plt.savefig("graphs/dipole_calibration_residuals.png", dpi=300)
plt.show()



PEAK_EMF_COEFF = (3 / 4) * (4 / 5) ** 2.5  # ~0.4293

def theory_emf_peak(N, v, R):
    return PEAK_EMF_COEFF * N * v * mu_0 * m_dipole / R ** 2


def compare_to_theory(x_vals, y_measured_v, y_theory, title):
    x_nom = np.array([v.n for v in x_vals])
    x_err = np.array([v.s for v in x_vals])
    sigma_y = y_measured_v * sigma_emf_frac
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

    return x_nom, x_err, y_nom, sigma_y


def linear_model(p, x):
    return p[0] * x + p[1]


def power_model(p, x):
    return p[0] * x ** p[1]


def plot_with_bestfit(x_nom, x_err, y_nom, sigma_y, y_theory, best_fit_result,
                       model_func, xlabel, title, filename_prefix):
    order = np.argsort(x_nom)
    x_smooth = np.linspace(min(x_nom), max(x_nom), 200)
    y_bestfit_smooth = model_func(best_fit_result.parameters, x_smooth)

    plt.figure(figsize=(7, 5))
    plt.errorbar(x_nom, y_nom, xerr=x_err, yerr=sigma_y, fmt="o", capsize=3,
                 label="Experimental Data (Oscilloscope)")
    plt.plot(x_nom[order], y_theory[order], "k--o", markersize=4,
             label="Theory (no free parameters)")
    plt.plot(x_smooth, y_bestfit_smooth, "g-",
             label=f"Best fit ($R^2$={best_fit_result.r_squared:.3f})")
    plt.xlabel(xlabel)
    plt.ylabel("Peak emf $\\varepsilon$ (V)")
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{filename_prefix}_fit.png", dpi=300)
    plt.show()


#emf vs no. of turns

R_fixed_N = ufloat(((3.4)/2), sigma_R_cm) / 100   # m
h_fixed_N = ufloat(48.4, sigma_h_cm) / 100   # m
v_fixed_N = np.sqrt(2 * constants.g * h_fixed_N.n)  # speed at coil, from free fall

turns_list = [10, 15, 20, 25, 30, 35, 40, 45, 50]
turns_N = [ufloat(n, sigma_N_turns) for n in turns_list]
emf_vs_N_measured = np.array([66, 116, 128, 166, 174, 226, 252, 260, 276]) / 2 / 1000  # V 

y_theory_N = np.array([theory_emf_peak(N, v_fixed_N, R_fixed_N.n) for N in turns_list])
xN, xerrN, yN, syN = compare_to_theory(
    turns_N, emf_vs_N_measured, y_theory_N, title="Peak emf vs Number of Turns",
)


# emf vs coil radius R
# north side up
N_fixed_R = 10
h = np.mean([48.3, 49.4, 49.2, 49.1, 49.2])  # cm
h_R = ufloat(h / 100, sigma_h_cm / 100)
d_cm = [2.5, 3.4, 4.8, 6.0, 8.9] #cm diameter
radii_cm = [d / 2 for d in d_cm] # cm

radii_R = [ufloat(r / 100, sigma_R_cm / 100) for r in radii_cm] # m

speed_R = np.sqrt(2 * constants.g * h_R.n)

emf_vs_R_measured = np.array([172, 124, 68, 44.8, 26.4]) / 2 / 1000  # pk-pk mV -> single-peak V

y_theory_R = np.array([
    theory_emf_peak(N_fixed_R, speed_R, R.n)
    for R in radii_R
])

xR, xerrR, yR, syR = compare_to_theory(
    radii_R,
    emf_vs_R_measured,
    y_theory_R,
    title="Peak emf vs Coil Radius",
)


# emf vs magnet speed s

N_fixed_s = 10
R_fixed_s = ufloat(((4.8) / 2), sigma_R_cm) / 100  # m

heights_cm = [44.9, 39.9, 34.9, 29.9, 24.9, 19.9, 14.9, 9.9, 4.9]  # cm
heights_m = [ufloat(hh / 100, sigma_h_cm / 100) for hh in heights_cm]
speeds_s = [ufloat(np.sqrt(2 * constants.g * hh.n),
                    constants.g * hh.s / np.sqrt(2 * constants.g * hh.n)) for hh in heights_m]

emf_vs_s_measured = np.array([74, 68, 62, 57.2, 47.6, 44, 40.8, 34.8, 29.6]) / 2 / 1000  # mV -> V

y_theory_s = np.array([theory_emf_peak(N_fixed_s, v.n, R_fixed_s.n) for v in speeds_s])

xs, xerrs, ys, sys_ = compare_to_theory(
    speeds_s, emf_vs_s_measured, y_theory_s, title="Peak emf vs Magnet Speed",
)



print("\n\n~~~ LINE OF BEST FIT ~~~")

print("\n-- N: linear fit emf = a*N + b --")
res_N = odr_fit(turns_N, [ufloat(v, s) for v, s in zip(yN, syN)], linear_model, beta0=[0.001, 0])
print(f"a (slope) = {res_N.parameters[0]:.6f} +/- {res_N.parameter_errors[0]:.6f}")
print(f"b (offset) = {res_N.parameters[1]:.6f} +/- {res_N.parameter_errors[1]:.6f}")
print(f"R^2 = {res_N.r_squared:.4f}")
plot_with_bestfit(xN, xerrN, yN, syN, y_theory_N, res_N, linear_model,
                   "Number of turns $N$", "Peak emf vs Number of Turns", "graphs/emf_vs_N")

print("\n-- R: power fit emf = a*R^b --")
res_R = odr_fit(radii_R, [ufloat(v, s) for v, s in zip(yR, syR)], power_model, beta0=[0.0001, -2])
print(f"a (scale) = {res_R.parameters[0]:.8f} +/- {res_R.parameter_errors[0]:.8f}")
print(f"b (exponent) = {res_R.parameters[1]:.4f} +/- {res_R.parameter_errors[1]:.4f}")
print(f"R^2 = {res_R.r_squared:.4f}")
plot_with_bestfit(xR, xerrR, yR, syR, y_theory_R, res_R, power_model,
                   "Coil radius $R$ (m)", "Peak emf vs Coil Radius", "graphs/emf_vs_R")

print("\n-- s: linear fit emf = a*v + b --")
res_s = odr_fit(speeds_s, [ufloat(v, s) for v, s in zip(ys, sys_)], linear_model, beta0=[0.05, 0])
print(f"a (slope) = {res_s.parameters[0]:.6f} +/- {res_s.parameter_errors[0]:.6f}")
print(f"b (offset) = {res_s.parameters[1]:.6f} +/- {res_s.parameter_errors[1]:.6f}")
print(f"R^2 = {res_s.r_squared:.4f}")
plot_with_bestfit(xs, xerrs, ys, sys_, y_theory_s, res_s, linear_model,
                   "Magnet speed $s$ (m/s)", "Peak emf vs Magnet Speed", "graphs/emf_vs_s")
