from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from uncertainties import ufloat


#constants


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

def solenoid_model(p, d):
    scale, offset = p
    L = L_solenoid.n
    R = R_solenoid.n
    I = I_solenoid.n
 
    term1 = (d + L / 2) / np.sqrt((d + L / 2) ** 2 + R ** 2)
    term2 = (d - L / 2) / np.sqrt((d - L / 2) ** 2 + R ** 2)
    B_z = (mu_0 / (4 * np.pi)) * (2 * np.pi * N * I / L) * (term1 - term2)
 
    return scale * B_z + offset
 
 
def odr_fit(x: list[ufloat], y: list[ufloat]) -> odr_fit_result:
    x_nom = np.array([v.n for v in x])
    x_err = np.array([v.s for v in x])
    y_nom = np.array([v.n for v in y])
    y_err = np.array([v.s for v in y])
 
    data = odr.RealData(x_nom, y_nom, sx=x_err, sy=y_err)
    model = odr.Model(solenoid_model)
    beta0 = [1.0, 0.0]
 
    odr_result = odr.ODR(data, model, beta0=beta0).run()
 
    parameters = odr_result.beta
    parameter_errors = odr_result.sd_beta
    converged = odr_result.info in (1, 2, 3)
    if not converged:
        print(f"WARNING: ODR did not clearly converge (info={odr_result.info})")
 
    y_pred = solenoid_model(parameters, x_nom)
    residuals = y_nom - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_nom - np.mean(y_nom)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan
    rmse = np.sqrt(np.mean(residuals**2))
 
    # res_var is ODR's own reduced chi-squared, weighted by both x_err and
    # y_err — use it directly rather than recomputing by hand.
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
 
 
def plot_field(x, y, sx, sy, fit_result, xlabel, ylabel, title, filename):
    x_fit = np.linspace(min(x), max(x), 200)
    y_fit = solenoid_model(fit_result.parameters, x_fit)
 
    plt.figure(figsize=(7, 5))
    plt.errorbar(x, y, xerr=sx, yerr=sy, fmt="o", capsize=3,
                 label="Experimental Data (Hall Sensor)")
    plt.plot(x_fit, y_fit, "k--",
             label=f"Fit ($\\chi_v^2$ = {fit_result.reduced_chi_squared:.2f})")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()
 
 
def plot_residuals(x, y, sy, fit_result, xlabel, filename):
    residuals = y - solenoid_model(fit_result.parameters, x)
 
    plt.figure(figsize=(7, 4))
    plt.errorbar(x, residuals, yerr=sy, fmt="o", capsize=3, color="crimson")
    plt.axhline(0, color="black", linestyle="--")
    plt.xlabel(xlabel)
    plt.ylabel("Residual (T)")
    plt.title("Residuals")
    plt.grid(True, alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()
 
 
def chi_squared_test(red_chi2):
    print(f"reduced chi-squared (chi_v^2): {red_chi2:.3f}")
    if 0.5 <= red_chi2 <= 1.5:
        print("results AGREE")
    elif red_chi2 < 0.5:
        print("chi_v^2 << 1: uncertainties may be overestimated")
    else:
        print("chi_v^2 >> 1: results DISAGREE")
    return red_chi2
 



 
result = odr_fit#(distances(m), magnetic_fields)
 
print("\n~~~FIT SUMMARY~~~")
print(f"Scale factor : {result.parameters[0]:.4f} +/- {result.parameter_errors[0]:.4f}")
print(f"Field offset : {result.parameters[1]:.6f} +/- {result.parameter_errors[1]:.6f} T")
print(f"R^2          : {result.r_squared:.4f}")
print(f"RMSE         : {result.rmse:.6f} T")
 
chi_squared_test(result.reduced_chi_squared)
 
plot_field(
    result.x_nom, result.y_nom, result.x_err, result.y_err,
    result,
    xlabel="Axial Distance $d$ (m)",
    ylabel="Magnetic Field Strength $B_z$ (T)",
    title="Magnetic Field Along the Axis of a Solenoid",
    filename="graphs/solenoid_magnetic_field.png",
)
 
plot_residuals(
    result.x_nom, result.y_nom, result.y_err,
    result,
    xlabel="Axial Distance $d$ (m)",
    filename="graphs/solenoid_residuals.png",
)