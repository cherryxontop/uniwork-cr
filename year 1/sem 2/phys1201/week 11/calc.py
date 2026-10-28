from dataclasses import dataclass
from math import log
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from uncertainties import ufloat
from uncertainties import unumpy as unp


@dataclass
class odr_fit_result:
    parameters: np.ndarray
    parameter_errors: np.ndarray
    r_squared: float
    x_nom: np.ndarray
    y_nom: np.ndarray
    x_err: np.ndarray
    y_err: np.ndarray


def linear_model(p, x):
    return p[0] * x + p[1]


def odr_fit(x, y, model_func, beta0):
    x_nom, x_err = np.array([v.n for v in x]), np.array([v.s for v in x])
    y_nom, y_err = np.array([v.n for v in y]), np.array([v.s for v in y])

    data = odr.RealData(x_nom, y_nom, sx=x_err, sy=y_err)
    odr_result = odr.ODR(data, odr.Model(model_func), beta0=beta0).run()

    residuals = y_nom - model_func(odr_result.beta, x_nom)
    r_squared = 1 - np.sum(residuals**2) / np.sum((y_nom - np.mean(y_nom)) ** 2)

    return odr_fit_result(odr_result.beta, odr_result.sd_beta, r_squared, x_nom, y_nom, x_err, y_err)


def sigma_test(k1, sk1, k2, sk2, label="parameter"):
    sigma_diff = abs(k1 - k2) / np.sqrt(sk1**2 + sk2**2)
    print(f"\nSIGMA TEST ({label})")
    print(f"value 1 : {k1:.3f} +/- {sk1:.3f}")
    print(f"value 2 : {k2:.3f} +/- {sk2:.3f}")
    print(f"discrepancy: {sigma_diff:.2f} sigma -> {'AGREE' if sigma_diff <= 3 else 'DISAGREE'}")
    return sigma_diff


def plot_fit(result, model_func, xlabel, ylabel, title, filename):
    x_smooth = np.linspace(min(result.x_nom), max(result.x_nom), 200)
    residuals = result.y_nom - model_func(result.parameters, result.x_nom)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    ax1.errorbar(result.x_nom, result.y_nom, xerr=result.x_err, yerr=result.y_err, fmt="o", capsize=3, label="Data")
    ax1.plot(x_smooth, model_func(result.parameters, x_smooth), "k--", label=f"ODR fit ($R^2$={result.r_squared:.4f})")
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    ax1.grid(True, alpha=0.6)
    ax1.legend()

    ax2.errorbar(result.x_nom, residuals, yerr=result.y_err, fmt="o", capsize=3, color="crimson")
    ax2.axhline(0, color="black", linestyle="--")
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel("Residual")
    ax2.grid(True, alpha=0.6)

    plt.tight_layout()
    plt.savefig(f"graphs/{filename}.png", dpi=300)
    plt.show()


# counts N in time t are Poisson, so the uncertainty on N is sqrt(N)
def rate(N, t):
    return ufloat(N, np.sqrt(N)) / t


# PRE-LAB Q2: iron shielding to block 75% of 1 MeV gamma rays
sigma_fe, rho_fe = 0.1, 7.874     # cm^2/g, g/cm^3
mu_fe = sigma_fe * rho_fe
print(f"Pre-lab Q2: mu = {mu_fe:.4f} /cm, x = {log(4) / mu_fe:.2f} cm")


# DISTANCE DEPENDENCE

t_bg, N_bg = 120, 43          # s, counts: background (mean 0.358 counts/s over 120 s)
t = 120                       # s, counting time at each distance (1 sample/s)
sr = 0.05                     # cm, uncertainty on a source-to-detector distance
# distance (cm), counts
distance_data = [(3.5, 615), (4.5, 397), (5.5, 262), (6.5, 225), (7.5, 181), (8.5, 148), (9.5, 121), (10.5, 101), (11.5, 97), (12.5, 84)]

if distance_data:
    bg = rate(N_bg, t_bg)
    r = [ufloat(d, sr) for d, _ in distance_data]
    R = [rate(N, t) - bg for _, N in distance_data]

    # R = k / r^2, so ln R = -2 ln r + const
    res = odr_fit(unp.log(r), unp.log(R), linear_model, beta0=[-2, 0])
    slope = ufloat(res.parameters[0], res.parameter_errors[0])
    print(f"\nln R vs ln r: slope = {slope:.3f}, R^2 = {res.r_squared:.4f}")
    sigma_test(slope.n, slope.s, -2, 0, label="slope vs inverse square")
    plot_fit(res, linear_model, "ln(r / cm)", "ln(R / counts per s)", "Distance dependence", "distance")


# ATTENUATION

# sheets: lead sheet readings with 1, 2, 3, 4 sheets between the sample and the counter
t_att = 120                   # s, counting time at each thickness
t_sheet, sx = 0.22, 0.01      # cm, thickness of one sheet and its uncertainty (vernier caliper)
N0 = 225                      # counts with no shield (1.875 counts/s)
N_sheets = [97, 57, 52, 54]   # counts with 1, 2, 3, 4 sheets
sigma_nist, rho = 0.3074, 11.35   # NIST lead at 0.356 MeV (interpolated), cm^2/g and g/cm^3

if N_sheets:
    bg = rate(N_bg, t_bg)
    R0 = rate(N0, t_att) - bg
    x = [ufloat(n * t_sheet, n * sx) for n in range(1, len(N_sheets) + 1)]
    R = [rate(n, t_att) - bg for n in N_sheets]

    # I = I0 exp(-mu x), so -ln(R / R0) = mu x
    res = odr_fit(x, [-unp.log(r / R0) for r in R], linear_model, beta0=[1, 0])
    mu = ufloat(res.parameters[0], res.parameter_errors[0])
    print(f"\nlead: mu = {mu:.3f} /cm, R^2 = {res.r_squared:.4f}")
    print(f"sigma = mu / rho = {mu / rho:.3f} cm^2/g")
    plot_fit(res, linear_model, "Thickness (cm)", "-ln(R / R0)", "Attenuation, lead", "attenuation_lead")
    sigma_test(mu.n, mu.s, sigma_nist * rho, 0, label="lead mu vs NIST, /cm")