from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr, stats
from uncertainties import ufloat

# UNCERTS
sigma_N_turns = 1          # uncertainty in turn count
sigma_R_cm = 0.1           # caliper/ruler uncertainty on radius (cm)
sigma_s_frac = 0.05        # fractional uncertainty on speed
sigma_emf_frac = 0.02      # fractional oscilloscope voltage reading uncertainty
sigma_emf_floor = 0.01     # absolute floor (smallest division / last digit), V

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


def theory_model_N(p, N):
    scale = p[0]
    return scale * N

def theory_model_R(p, R):
    scale = p[0]
    return scale * (R ** 1.0) 

def theory_model_s(p, s):
    scale = p[0]
    return scale * s

def odr_fit(x: list[ufloat], y: list[ufloat], model_func, beta0=[1.0]) -> odr_fit_result:
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

def plot_field(x, y, sx, sy, fit_result, model_func, xlabel, ylabel, title, filename):
    x_fit = np.linspace(min(x), max(x), 200)
    y_fit = model_func(fit_result.parameters, x_fit)

    plt.figure(figsize=(7, 5))
    plt.errorbar(x, y, xerr=sx, yerr=sy, fmt="o", capsize=3,
                 label="Experimental Data (Oscilloscope)")
    plt.plot(x_fit, y_fit, "k--",
             label=f"Theoretical Curve ($\\chi_v^2$ = {fit_result.reduced_chi_squared:.2f})")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def plot_residuals(x, y, sy, fit_result, model_func, xlabel, filename):
    residuals = y - model_func(fit_result.parameters, x)

    plt.figure(figsize=(7, 4))
    plt.errorbar(x, residuals, yerr=sy, fmt="o", capsize=3, color="crimson")
    plt.axhline(0, color="black", linestyle="--")
    plt.xlabel(xlabel)
    plt.ylabel("Residual (V)")
    plt.title("Residuals")
    plt.grid(True, alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

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

def sigma_test(k1, sk1, k2, sk2):
    sigma_diff = abs(k1 - k2) / np.sqrt(sk1**2 + sk2**2)

    print("\nSIGMA TEST")
    print(f"measured scaling factor : {k1:.3f} +/- {sk1:.3f}")
    print(f"expected theoretical val: {k2:.3f} +/- {sk2:.3f}")
    print(f"discrepancy             : {sigma_diff:.2f} sigma")

    if sigma_diff <= 3.0:
        print("results AGREE within experimental uncertainty")
    else:
        print("results DISAGREE")

    return sigma_diff

# ~~~~~~PART 1~~~~~~~~~~~~~~~~~~

turns_raw = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
turns_N = [ufloat(n, sigma_N_turns) for n in turns_raw]
emf_N_v = np.array([0.04, 0.08, 0.12, 0.16, 0.20, 0.25, 0.29, 0.33, 0.37, 0.42])
emf_N = [ufloat(v, v * sigma_emf_frac + sigma_emf_floor) for v in emf_N_v]

result_N = odr_fit(turns_N, emf_N, theory_model_N, beta0=[0.004])

print("\n~~~PEAK EMF VS N~~~")
print(f"Scale factor : {result_N.parameters[0]:.4f} +/- {result_N.parameter_errors[0]:.4f}")
print(f"R^2          : {result_N.r_squared:.4f}")
print(f"RMSE         : {result_N.rmse:.4f} V")

dof_N = len(turns_N) - 1  # 1 parameter (scale only)
chi2_stat_N = result_N.reduced_chi_squared * dof_N
chi_squared_test(chi2_stat_N, dof_N)

plot_field(result_N.x_nom, result_N.y_nom, result_N.x_err, result_N.y_err, result_N, theory_model_N,
           xlabel="Number of turns $N$", ylabel="Peak emf $\\varepsilon$ (V)",
           title="Peak emf vs Number of Turns (Theory)", filename="graphs/emf_vs_N.png")
plot_residuals(result_N.x_nom, result_N.y_nom, result_N.y_err, result_N, theory_model_N,
               xlabel="Number of turns $N$", filename="graphs/emf_vs_N_residuals.png")


# ~~~~~~PART 2~~~~~~~~~~~~~~~~~~

radii_cm = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
radii_R = [ufloat(r / 100.0, sigma_R_cm / 100.0) for r in radii_cm]
emf_R_v = np.array([0.03, 0.07, 0.12, 0.19, 0.28, 0.38, 0.49])
emf_R = [ufloat(v, v * sigma_emf_frac + sigma_emf_floor) for v in emf_R_v]

result_R = odr_fit(radii_R, emf_R, theory_model_R, beta0=[1.0])

print("\n~~~PEAK EMF VS COIL RADIUS (R)~~~")
print(f"Scale factor : {result_R.parameters[0]:.4f} +/- {result_R.parameter_errors[0]:.4f}")
print(f"R^2          : {result_R.r_squared:.4f}")
print(f"RMSE         : {result_R.rmse:.4f} V")

dof_R = len(radii_R) - 1
chi2_stat_R = result_R.reduced_chi_squared * dof_R
chi_squared_test(chi2_stat_R, dof_R)

plot_field(result_R.x_nom, result_R.y_nom, result_R.x_err, result_R.y_err, result_R, theory_model_R,
           xlabel="Coil Radius $R$ (m)", ylabel="Peak emf $\\varepsilon$ (V)",
           title="Peak emf vs Coil Radius (Theory)", filename="graphs/emf_vs_R.png")
plot_residuals(result_R.x_nom, result_R.y_nom, result_R.y_err, result_R, theory_model_R,
               xlabel="Coil Radius $R$ (m)", filename="graphs/emf_vs_R_residuals.png")


# ~~~~~~PART 3~~~~~~~~~~~~~~~~~~

speeds_v = np.array([0.60, 0.85, 1.05, 1.20, 1.35, 1.55, 1.70])
speeds_s = [ufloat(v, v * sigma_s_frac) for v in speeds_v]
emf_s_v = np.array([0.13, 0.18, 0.22, 0.25, 0.28, 0.33, 0.36])
emf_s = [ufloat(v, v * sigma_emf_frac + sigma_emf_floor) for v in emf_s_v]

result_s = odr_fit(speeds_s, emf_s, theory_model_s, beta0=[0.2])

print("\n~~~PEAK EMF VS MAGNET SPEED (s)~~~")
print(f"Scale factor : {result_s.parameters[0]:.4f} +/- {result_s.parameter_errors[0]:.4f}")
print(f"R^2          : {result_s.r_squared:.4f}")
print(f"RMSE         : {result_s.rmse:.4f} V")

dof_s = len(speeds_s) - 1
chi2_stat_s = result_s.reduced_chi_squared * dof_s
chi_squared_test(chi2_stat_s, dof_s)

plot_field(result_s.x_nom, result_s.y_nom, result_s.x_err, result_s.y_err, result_s, theory_model_s,
           xlabel="Magnet Speed $s$ (m/s)", ylabel="Peak emf $\\varepsilon$ (V)",
           title="Peak emf vs Magnet Speed (Theory)", filename="graphs/emf_vs_s.png")
plot_residuals(result_s.x_nom, result_s.y_nom, result_s.y_err, result_s, theory_model_s,
               xlabel="Magnet Speed $s$ (m/s)", filename="graphs/emf_vs_s_residuals.png")