from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr, constants, stats
from uncertainties import ufloat


#constants
N = 700  # no. of turns in the solenoid
mu_0 = constants.mu_0  # permeability of free space (Wb / A m)

r_outer = ufloat(5.7, 0.25) / 100
r_inner = ufloat(3.8, 0.25) / 100

R_solenoid = (r_outer + r_inner) / 2  # radius of solenoid (m)
L_solenoid = ufloat(14.9, 0.25) / 100  # length of solenoid (m)
I_solenoid = ufloat(2.32, 2.32 * 0.01)  # solenoid current (A)

V_0 = ufloat(2.52, 2.52*0.01)  # hall sensor's 0 field voltage
S_sensor = ufloat(3.13, 0.09) * 0.001 / 0.0001  # sensitivity

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
        print(f"did notconverge (info={odr_result.info})")

    y_pred = solenoid_model(parameters, x_nom)
    residuals = y_nom - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_nom - np.mean(y_nom)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan
    rmse = np.sqrt(np.mean(residuals**2))

    # res_var is ODR's own reduced chi-squared, weighted by both x_err and
    # y_err -- use it directly rather than recomputing by hand.
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


def chi_squared_test(chi2_stat, dof):
    p_value = stats.chi2.sf(chi2_stat, dof)  # sf = 1 - cdf, "survival function"
    print(f"chi-squared: {chi2_stat:.3f}  (dof = {dof})")
    print(f"reduced chi-squared: {chi2_stat/dof:.3f}")
    print(f"p-value: {p_value:.4f}")
    if p_value > 0.05:
        print("results AGREE with the model (p > 0.05)")
    else:
        print("results DISAGREE with the model (p <= 0.05)")
    return p_value


def sigma_test(k1, sk1, k2):
    sigma_diff = abs(k1 - k2) / sk1

    print("SIGMA TEST")
    print(f"derived g  : {k1:.3f} +/- {sk1:.3f} m/s^2")
    print(f"accepted g : {k2:.4f} m/s^2")
    print(f"discrepancy: {sigma_diff:.2f} sigma")

    if sigma_diff <= 3.0:
        print("results AGREE within experimental uncertainty")
    else:
        print("results DISAGREE")

    return sigma_diff


distances_cm = [-5,
                -4,
                -3,
                -1,
                0,
                1,
                2,
                2.5,
                3,
                4,
                5,
                6,
                6.5,
                7.5,
                8,
                8.5,
                9,
                9.5,
                10,
                10.5,
                11, 
                12,
                13,
                15,
                15, 
                18]
sigma_d_cm = 0.25  # uncertainty in position (cm)
distances_m = [ufloat(d / 100.0, sigma_d_cm / 100.0) for d in distances_cm]
voltages_measured = np.array([2.90,
                     2.91,
                     2.92,
                     2.91,
                     2.91,
                     2.91,
                     2.92,
                     2.92,
                     2.93,
                     2.92,
                     2.91,
                     2.90,
                     2.88,
                     2.84,
                     2.79,
                     2.74,
                     2.69,
                     2.66,
                     2.62,
                     2.61,
                     2.58,
                     2.56,
                     2.54,
                     2.54,
                     2.53,
                     2.53]) # V
sigma_v = voltages_measured * (0.5 / 100) + 0.01  # uncertainty in voltage (V)


magnetic_fields = []
print("~~~SOLENOID MAGNETIC FIELD RESULTS~~~")
for d, v_val, sv in zip(distances_m, voltages_measured, sigma_v):
    V_meas = ufloat(v_val, sv)
    diff = V_meas - V_0
    B_val = ufloat(abs(diff.n), diff.s) / S_sensor  # eq2
    magnetic_fields.append(B_val)
    print(f"d = {d} m | V = {V_meas} V | B = {B_val * 1000:.2f} mT")

result = odr_fit(distances_m, magnetic_fields)

print("\n~~~FIT SUMMARY~~~")
print(f"Scale factor : {result.parameters[0]:.4f} +/- {result.parameter_errors[0]:.4f}")
print(f"Field offset : {result.parameters[1]:.6f} +/- {result.parameter_errors[1]:.6f} T")
print(f"R^2          : {result.r_squared:.4f}")
print(f"RMSE         : {result.rmse:.6f} T")

dof = len(distances_m) - 2  # number of points minus number of fit params
chi2_stat = result.reduced_chi_squared * dof
chi_squared_test(chi2_stat, dof)

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