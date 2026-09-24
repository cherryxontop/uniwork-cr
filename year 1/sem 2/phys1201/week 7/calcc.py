from dataclasses import dataclass
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import odr, stats
from uncertainties import ufloat

g = 9.7976
FPS = 30
sT = 1 / (2 * FPS)     # timing uncert half a frame
sVy = 0.05             # m/s, velocity uncert from pixel-tracking


@dataclass
class odr_fit_result:
    parameters: np.ndarray
    parameter_errors: np.ndarray
    r_squared: float
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

    residuals = y_nom - model_func(parameters, x_nom)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_nom - np.mean(y_nom)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan

    return odr_fit_result(
        parameters=parameters,
        parameter_errors=parameter_errors,
        r_squared=r_squared,
        reduced_chi_squared=odr_result.res_var,
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


# no drag (Eq. 1). p = [v0], slope fixed at -g
def no_drag_model(p, t):
    return p[0] - g * t


# drag (Eq. 4), rewritten for a y-axis pointing up so vT < 0, p = [v0, vT]
def drag_model(p, t):
    v0, vT = p
    ratio = np.clip(v0 / vT, -0.999999, 0.999999)  # blows up at +/-1
    return vT * np.tanh(-g * t / vT + np.arctanh(ratio))


def load_data(path):
    df = pd.read_csv(path).rename(columns={"v_y": "vy"})
    df["t"] = df["t"] - df["t"].iloc[0]
    df = df.dropna(subset=["vy"])

    t = [ufloat(val, sT) for val in df["t"]]
    vy = [ufloat(val, sVy) for val in df["vy"]]
    return t, vy


def plot_fit(fit_result, model_func, title, filename):
    x, y = fit_result.x_nom, fit_result.y_nom
    x_fit = np.linspace(min(x), max(x), 200)
    y_fit = model_func(fit_result.parameters, x_fit)

    plt.figure(figsize=(7, 5))
    plt.errorbar(x, y, xerr=fit_result.x_err, yerr=fit_result.y_err, fmt="o", capsize=3,
                 color="navy", ecolor="crimson", label="Tracker Data")
    plt.plot(x_fit, y_fit, "k--", label=f"Drag fit ($R^2$ = {fit_result.r_squared:.3f})")
    plt.xlabel("Time $t$ (s)")
    plt.ylabel("Velocity $v_y$ (m/s)")
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()


def plot_residuals(fit_nodrag, fit_drag, title, filename):
    x, y = fit_drag.x_nom, fit_drag.y_nom
    resid_nodrag = y - no_drag_model(fit_nodrag.parameters, x)
    resid_drag = y - drag_model(fit_drag.parameters, x)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    for ax, resid, colour, marker, name in [
        (ax1, resid_nodrag, "darkorange", "^", "No-drag residuals (Eq. 1)"),
        (ax2, resid_drag, "navy", "o", "Drag residuals (Eq. 4)"),
    ]:
        ax.axhline(0, color="black", linestyle="--")
        ax.scatter(x, resid, color=colour, marker=marker, label=name)
        ax.set_ylabel("residual (m/s)")
        ax.grid(True, alpha=0.6)
        ax.legend()
    ax2.set_xlabel("t (s)")
    ax1.set_title(title)
    fig.tight_layout()
    fig.savefig(filename, dpi=300)
    plt.show()


def analyse_pan(label, csv_path, graph_dir):
    t_data, vy_data = load_data(csv_path)
    vy = np.array([v.n for v in vy_data])

    fit_nodrag = odr_fit(t_data, vy_data, no_drag_model, beta0=[vy[0]])
    fit_drag = odr_fit(t_data, vy_data, drag_model, beta0=[vy[0], vy.min() * 1.2])

    v0_nodrag = ufloat(fit_nodrag.parameters[0], fit_nodrag.parameter_errors[0])
    v0_drag = ufloat(fit_drag.parameters[0], fit_drag.parameter_errors[0])
    vT = ufloat(fit_drag.parameters[1], fit_drag.parameter_errors[1])

    print(f"\n{label}")
    print(f"no-drag fit (Eq. 1): v0 = {v0_nodrag:.3f} m/s | R^2 = {fit_nodrag.r_squared:.4f}")
    print(f"drag fit    (Eq. 4): v0 = {v0_drag:.3f} m/s, vT = {vT:.3f} m/s | R^2 = {fit_drag.r_squared:.4f}")

    n = len(vy)
    print("\nno-drag chi-squared")
    chi_squared_test(fit_nodrag.reduced_chi_squared * (n - 1), n - 1)
    print("\ndrag chi-squared")
    chi_squared_test(fit_drag.reduced_chi_squared * (n - 2), n - 2)

    name = label.lower().replace(" ", "_")
    plot_fit(fit_drag, drag_model, f"{label}: Drag Fit", f"{graph_dir}/{name}_drag_fit.png")
    plot_residuals(fit_nodrag, fit_drag, f"{label}: Residuals", f"{graph_dir}/{name}_residuals.png")

    return vT


def main():
    print("DATA ANALYSIS")

    graph_dir = "graphs"

    vT_single = analyse_pan("Single patty pan", "files/one_pan.csv", graph_dir)
    vT_double = analyse_pan("Two nested patty pans", "files/two_pan.csv", graph_dir)

    ratio = vT_double / vT_single
    print(f"\nvT (single)  = {vT_single:.3f} m/s")
    print(f"vT (double)  = {vT_double:.3f} m/s")
    print(f"measured vT ratio = {ratio:.3f}")

    sigma_test(ratio.n, ratio.s, np.sqrt(2), 0.0, label="vT ratio vs sqrt(2)")


if __name__ == "__main__":
    main()