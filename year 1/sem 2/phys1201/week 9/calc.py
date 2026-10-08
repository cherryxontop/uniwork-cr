from dataclasses import dataclass
from math import pi, log
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from uncertainties import ufloat


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


def proportional_model(p, x):
    return p[0] * x


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


# SPEED OF SOUND

L = ufloat(1.004, 0.0025)     # m, pipe length
a = ufloat(0.043, 0.0025)     # m, pipe radius
sigma_f = 15                  # Hz, uncertainty on one peak frequency
T_room = ufloat(22, 1)        # deg C

# resonant frequencies (Hz) as {mode number: frequency}: clap, tap, white noise
# (closed pipe mode 1 left out: the 90-110 Hz hump is in every spectrum, so it is not a pipe mode)
open_data = [
    {1: 166.6, 2: 326.5, 3: 465.6, 4: 655.1, 5: 817.8, 6: 982.3},
    {1: 161.0, 2: 322.1, 3: 472.3},
    {5: 819, 6: 982, 7: 1125},
]
closed_data = [
    {2: 258.3, 3: 413.9, 4: 595.5, 5: 758.9, 6: 931.2, 7: 1098.0, 8: 1263.7},
    {2: 257.4, 3: 415.7, 4: 578.3, 6: 930.0, 8: 1240.7},
    {2: 259, 3: 419, 4: 590, 5: 753, 6: 930, 7: 1110, 8: 1252},
]

# f = c * x
x_open = lambda modes: [n / (2 * (L + 1.2 * a)) for n in modes]
x_closed = lambda modes: [(2 * n - 1) / (4 * (L + 0.6 * a)) for n in modes]

c_methods = []
for pipe, data, x_func in [("open", open_data, x_open), ("closed", closed_data, x_closed)]:
    for label, d in zip(["clap", "tap", "white noise"], data):
        modes = sorted(d)
        f = [ufloat(d[n], sigma_f) for n in modes]
        res = odr_fit(x_func(modes), f, proportional_model, beta0=[340])
        c = ufloat(res.parameters[0], res.parameter_errors[0])
        print(f"{pipe} {label}: c = {c:.2f} m/s, R^2 = {res.r_squared:.4f}")
        plot_fit(res, proportional_model, "x (1/m)", "Resonant frequency (Hz)",
                 f"{pipe.capitalize()} pipe, {label}", f"speed_{pipe}_{label.replace(' ', '_')}")
        c_methods.append(c)

c_open, c_closed, c_mean = sum(c_methods[:3]) / 3, sum(c_methods[3:]) / 3, sum(c_methods) / 6
print(f"\nopen pipe average: c = {c_open:.2f} m/s")
print(f"closed pipe average: c = {c_closed:.2f} m/s")
print(f"average of all six: c = {c_mean:.2f} m/s")

c_theory = 331.3 + 0.606 * T_room    # m/s
print(f"theoretical c at {T_room} C = {c_theory:.2f} m/s")
sigma_test(c_open.n, c_open.s, c_closed.n, c_closed.s, label="open vs closed")
sigma_test(c_mean.n, c_mean.s, c_theory.n, c_theory.s, label="average c vs theory")


# RESONANCE DECAY

decay_freqs = [166.6, 326.5, 465.6]   # Hz, open clap modes 1-3
Dt = 0.03                     # s, window length
sigma_t = 0.002               # s, uncertainty on each t_n
sigma_L = 2.0                 # dB, uncertainty on one level
# level (dB) of each mode in window n, t_n = n * Dt (band level within +/-25 Hz of the mode)
decay_L = [
    [-26.8, -28.1, -31.3, -43.7, -46.0, -53.8, -56.2],
    [-23.5, -25.2, -35.7, -37.8, -44.4, -47.0],
    [-27.8, -29.5, -36.2, -32.4, -41.7],
]

for i in range(3):
    t = [ufloat(n * Dt, sigma_t) for n in range(len(decay_L[i]))]
    L_db = [ufloat(v, sigma_L) for v in decay_L[i]]
    res = odr_fit(t, L_db, linear_model, beta0=[-100, 0])
    slope = ufloat(res.parameters[0], res.parameter_errors[0])
    T_half = 3 / (-slope)
    Q = pi * decay_freqs[i] * T_half / log(2)
    print(f"\nmode {i + 1} ({decay_freqs[i]} Hz): slope = {slope:.1f} dB/s, R^2 = {res.r_squared:.4f}, "
          f"T_1/2 = {T_half * 1000:.1f} ms, Q = {Q:.1f}")
    plot_fit(res, linear_model, "$t_n$ (s)", "Level (dB)", f"Decay of mode {i + 1}", f"decay_mode{i + 1}")