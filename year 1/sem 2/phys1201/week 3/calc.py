from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from uncertainties import ufloat

g_accepted = 9.7976


@dataclass
class odr_fit_result:
    slope: ufloat
    intercept: ufloat
    r_squared: float
    rmse: float
    x_nom: np.ndarray
    y_nom: np.ndarray
    x_err: np.ndarray
    y_err: np.ndarray

def odr_fit(x: list[ufloat], y: list[ufloat]) -> odr_fit_result:

    x_nom = np.array([v.n for v in x])
    x_err = np.array([v.s for v in x])
    y_nom = np.array([v.n for v in y])
    y_err = np.array([v.s for v in y])

    data = odr.RealData(x_nom, y_nom, sx=x_err, sy=y_err)

    model = odr.Model(lambda p, x: p[0] * x + p[1])
    beta0 = [4.0, 0.0] # rough initial guess; true slope ≈ 4pi²/g ≈ 4

    odr_result = odr.ODR(data, model, beta0=beta0).run()

    slope = ufloat(odr_result.beta[0], odr_result.sd_beta[0])
    intercept = ufloat(odr_result.beta[1], odr_result.sd_beta[1])

    y_pred = model.fcn(odr_result.beta, x_nom)
    residuals = y_nom - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_nom - np.mean(y_nom))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan
    rmse = np.sqrt(np.mean(residuals**2))

    return odr_fit_result(
    slope=slope,
    intercept=intercept,
    r_squared=r_squared,
    rmse=rmse,
    x_nom=x_nom,
    y_nom=y_nom,
    x_err=x_err,
    y_err=y_err,
)

def plot(x, y, sx, sy, slope, slope_err, intercept, xlabel, ylabel, title, filename):
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = slope * x_fit + intercept

    plt.figure(figsize=(7, 5))

    plt.errorbar(
        x, y,
        xerr=sx,
        yerr=sy,
        fmt="o",
        capsize=3,
        label="Experimental Data"
    )

    plt.plot(
        x_fit,
        y_fit,
        "k--",
        label=f"Fit: Slope = {slope:.3f} ± {slope_err:.3f}"
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def sigma_test(k1, sk1, k2):
    sigma_diff = abs(k1 - k2) / sk1

    print("SIGMA TEST")
    print(f"derived g  : {k1:.3f} +/- {sk1:.3f} m/s²")
    print(f"accepted g : {k2:.4f} m/s²")
    print(f"discrepancy: {sigma_diff:.2f} sigma")

    if sigma_diff <= 3.0:
        print("results AGREE within experimental uncertainty")
    else:
        print("results DISAGREE")

    return sigma_diff


# EXPERIMENT 1: angle dependence of g

L_p1_cm = 51.2  # measured length
sigma_L = 0.25 / 100  # m
angles_deg = [5.0, 25.0, 40.0]
time_10_oscillations_trials = [
    [14.53, 14.41, 14.36],
    [14.67, 14.66, 14.68],
    [14.88, 14.92, 14.95]
]
sigma_t = 0.20 # seconds
sigma_theta_deg = 0.5 #degrees

g_results_p1 = []

print("~~~PART 1 RESULTS~~~")
for i in range(len(angles_deg)):
    theta_deg = ufloat(angles_deg[i], sigma_theta_deg)
    theta_rad = theta_deg * np.pi / 180.0

    trials = time_10_oscillations_trials[i]
    mean_time = np.mean(trials)
    std_err_time = np.std(trials, ddof=1) / np.sqrt(len(trials))
    total_time_err = max(std_err_time, sigma_t)

    L = ufloat(L_p1_cm / 100.0, sigma_L)
    t_total = ufloat(mean_time, total_time_err)
    T = t_total / 10.0  # period for one oscillation

    # angle correction factor
    if theta_deg.n >= 10.0:
        correction_factor = 1.0 + (1.0 / 16.0) * (theta_rad**2)
    else:
        correction_factor = ufloat(1.0, 0.0)

    g_val = 4.0 * (np.pi**2) * L * (correction_factor**2) / (T**2)
    g_results_p1.append(g_val)

    print(f"angle: {theta_deg}° | correction: {correction_factor:.4f} | L = {L} m | T = {T} s | g = {g_val}")

    print(f"\nangle: {angles_deg[i]}°")
    sigma_test(g_results_p1[i].n, g_results_p1[i].s, g_accepted)

# plotting results for fun
theta_nom = angles_deg
theta_err = [sigma_theta_deg] * len(angles_deg)
g_nom = [g.n for g in g_results_p1]
g_err = [g.s for g in g_results_p1]

plt.figure(figsize=(7, 5))
plt.errorbar(
    theta_nom, g_nom,
    xerr=theta_err, yerr=g_err,
    fmt='o',
    color="navy",
    ecolor="crimson",
    capsize=3,
    label="Experimental $g$"
)
plt.axhline(g_accepted, color="black", linestyle="--", label=f"Accepted $g$ = {g_accepted} m/s²")
plt.xlabel("Release Angle (°)")
plt.ylabel("Derived $g$ (m/s²)")
plt.title("Part 1: Derived $g$ vs Release Angle")
plt.grid(True, alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/pendulum_angle_dependence.png", dpi=300)
plt.show()


# EXPERIMENT 2: length dependence of period

lengths_p2_cm = [20.0, 40.0, 60.0, 80.0]
time_10_p2 = [
    [9.33, 9.33, 9.41],
    [13.08, 13.08, 13.01],
    [15.68, 15.63, 15.80],
    [18.08, 18.09, 18.08]
]

lengths_m = [ufloat(l / 100.0, sigma_L) for l in lengths_p2_cm]

periods = []
for trials in time_10_p2:
    mean_time = np.mean(trials)
    std_err_time = np.std(trials, ddof=1) / np.sqrt(len(trials))
    total_time_err = max(std_err_time, sigma_t)

    t_total = ufloat(mean_time, total_time_err)
    periods.append(t_total / 10.0)

x = lengths_m
y = [T**2 for T in periods]

result = odr_fit(x, y)

g_experimental = 4.0 * (np.pi**2) / result.slope

print("~~~PART 2 RESULTS~~~")
print(f"linear fit slope : {result.slope} s²/m")
print(f"derived g        : {g_experimental} m/s²")
print(f"intercept        : {result.intercept} s²")
print(f"R^2            : {result.r_squared:.4f}")
print(f"RMSE           : {result.rmse:.4f}")

# test with accepted canberra value (9.796 m/s^2)
sigma_test(g_experimental.n, g_experimental.s, g_accepted)

# Plotting results for Part 2
plot(
    result.x_nom,
    result.y_nom,
    result.x_err,
    result.y_err,
    result.slope.n,
    result.slope.s,
    result.intercept.n,
    xlabel="Length $L$ (m)",
    ylabel=r"Period Squared $T^2$ (s$^2$)",
    title="Simple Pendulum: $T^2$ vs Length $L$",
    filename="graphs/pendulum_length_dependence.png"
)