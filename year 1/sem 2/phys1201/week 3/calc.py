import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from uncertainties import ufloat

g = 9.796

def odr_fit(x_data, y_data, zero_intercept: bool = False):
    x = np.array([v.n for v in x_data])
    sx = np.array([v.s for v in x_data])
    y = np.array([v.n for v in y_data])
    sy = np.array([v.s for v in y_data])

    data = odr.RealData(x, y, sx=sx, sy=sy)

    if zero_intercept:
        linear_model = odr.Model(lambda p, x: p[0] * x)
        beta0 = [10.0]
    else:
        linear_model = odr.Model(lambda p, x: p[0] * x + p[1])
        beta0 = [10.0, 0.0]

    odr_result = odr.ODR(data, linear_model, beta0=beta0).run()

    slope = odr_result.beta[0]
    slope_err = odr_result.sd_beta[0]
    
    if zero_intercept:
        intercept = 0.0
        intercept_err = 0.0
    else:
        intercept = odr_result.beta[1]
        intercept_err = odr_result.sd_beta[1]

    return slope, slope_err, intercept, intercept_err, (x, y, sx, sy)


def plot(x, y, sx, sy, slope, slope_err, intercept, xlabel, ylabel, title, filename):
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = slope * x_fit + intercept
    
    plt.figure(figsize=(7, 5))
    plt.errorbar(
        x, y,
        xerr=sx, yerr=sy,
        fmt='o',
        color="navy",
        ecolor="crimson",
        capsize=3,
        label="Experimental Data"
    )
    plt.plot(
        x_fit, y_fit,
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


def sigma_test(k1, sk1, k2, sk2):
    sigma_diff = abs(k1 - k2) / np.sqrt(sk1**2 + sk2**2)
    print("SIGMA TEST")
    print(f"static k  : {k1:.3f} +/- {sk1:.3f} N/m")
    print(f"dynamic k : {k2:.3f} +/- {sk2:.3f} N/m")
    print(f"discrepancy: {sigma_diff:.2f} sigma")

    if sigma_diff <= 3.0:
        print("results AGREE within experimental uncertainty")
    else:
        print("results DISAGREE")



"""

# EXPERIMENT 1: angle dependence of g

# Measured data for 3 initial angles (low, medium, high)
# angles in degrees, lengths in meters, time for 10 oscillations in seconds
angles_deg = [5.0, 25.0, 40.0]
lengths_p1_cm = [99.5, 99.5, 99.5]  # measured length
time_10_oscillations = [20.06, 20.25, 20.85]

# Uncertainties
sigma_L = 0.001  # length uncertainty in meters (1 mm)
sigma_t = 0.20   # total time uncertainty for 10 oscillations in seconds

g_results_p1 = []

for i in range(len(angles_deg)):
    theta_deg = angles_deg[i]
    theta_rad = np.deg2rad(theta_deg)
    
    L = ufloat(lengths_p1_cm[i] / 100.0, sigma_L)
    t_total = ufloat(time_10_oscillations[i], sigma_t)
    T = t_total / 10.0  # Period for one oscillation
    
    # Equation 4 correction factor: 1 + (1/16)*theta_0^2
    correction_factor = 1.0 + (1.0 / 16.0) * (theta_rad**2)
    
    # g = 4 * pi^2 * L / T^2 * (correction_factor^2)  [or equivalent expansion]
    # Rearranging Equation 4: T = 2*pi*sqrt(L/g)*(1 + 1/16*theta_0^2) => g = 4*pi^2*L*(1 + 1/16*theta_0^2)^2 / T^2
    g_val = 4.0 * (PI**2) * L * (correction_factor**2) / (T**2)
    
    g_results_p1.append(g_val)
    print(f"Angle: {theta_deg}° | L = {L} m | T = {T} s | g = {g_val}")

# ==========================================
# EXPERIMENT 2: Part 2 - Length Dependence of Period
# ==========================================
print("\n--- EXPERIMENT 2: Part 2 (Length Dependence) ---")

# Measurements for 4 different lengths at small angle (< 10 deg)
lengths_p2_cm = [40.0, 60.0, 80.0, 100.0]
time_10_p2 = [12.72, 15.58, 17.98, 20.06]

# Convert lengths to meters with uncertainty
lengths_m = [ufloat(l / 100.0, sigma_L) for l in lengths_p2_cm]

# Calculate periods T with uncertainties
periods = [ufloat(t, sigma_t) / 10.0 for t in time_10_p2]

# Linearisation: T = 2*pi*sqrt(L/g) => T^2 = (4*pi^2 / g) * L
# Let y = T^2, x = L. Then slope = 4*pi^2 / g => g = 4*pi^2 / slope
x_dynamic = lengths_m
y_dynamic = [T**2 for T in periods]

slope, slope_err, intercept, intercept_err, plot_data = odr_fit(x_dynamic, y_dynamic)

# Calculate g from slope
g_experimental = 4.0 * (PI**2) / slope
# Propagate error: sigma_g = g * (sigma_slope / slope)
g_experimental_err = g_experimental * (slope_err / slope)

print(f"Linear Fit Slope: {slope:.4f} ± {slope_err:.4f} s²/m")
print(f"Derived g: {g_experimental:.4f} ± {g_experimental_err:.4f} m/s²")
print(f"Intercept: {intercept:.4f} ± {intercept_err:.4f} s²")

# Test agreement with accepted Canberra value (9.7976 m/s^2)
sigma_test(g_experimental.n, g_experimental.s, G_ACCEPTED, 0.0001, name1="Derived g", name2="Accepted g")

# Plotting results for Part 2
plot(
    *plot_data,
    slope,
    slope_err,
    intercept,
    xlabel="Length $L$ (m)",
    ylabel="Period Squared $T^2$ ($\text{s}^2$)",
    title="Simple Pendulum: $T^2$ vs Length $L$",
    filename="pendulum_length_dependence.png"
)


if __name__ == "__main__":
    main()

"""





