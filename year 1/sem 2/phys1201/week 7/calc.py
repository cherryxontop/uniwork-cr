import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import odr
from uncertainties import ufloat

g = 9.7976
FPS = 30
DT = 1 / (2 * FPS)     # timing uncertainty: half a frame
DVY = 0.05             # m/s, velocity uncertainty from pixel-tracking resolution

# eq1: no drag. p = [v0], slope fixed at -g
def no_drag_model(p, t):
    return p[0] - g * t


# eq4: drag. p = [v0, vT]
def drag_model(p, t):
    return p[1] * np.tanh(g * t / p[1] + np.arctanh(p[0] / p[1]))

def load_data(path):
    df = pd.read_csv(path)
    t = [ufloat(val, DT) for val in df["t"]]
    vy = [ufloat(val, DVY) for val in df["vy"]]
    return t, vy


def odr_fit(x_data, y_data, model_func, beta0):
    x = np.array([v.n for v in x_data])
    sx = np.array([v.s for v in x_data])
    y = np.array([v.n for v in y_data])
    sy = np.array([v.s for v in y_data])

    model = odr.Model(model_func)
    data = odr.RealData(x, y, sx=sx, sy=sy)

    odr_result = odr.ODR(data, model, beta0=beta0).run()

    params = odr_result.beta
    params_err = odr_result.sd_beta

    return params, params_err, (x, y, sx, sy)


def plot(
    x,
    y,
    sx,
    sy,
    model_func,
    params,
    label,
    xlabel,
    ylabel,
    title,
    filename,
):
    x_fit = np.linspace(min(x), max(x), 200)
    y_fit = model_func(params, x_fit)

    plt.figure(figsize=(7, 5))
    plt.errorbar(
        x,
        y,
        xerr=sx,
        yerr=sy,
        fmt="o",
        color="navy",
        ecolor="crimson",
        capsize=3,
        label="Tracker Data",
    )
    plt.plot(x_fit, y_fit, "k--", label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()


def residual_plot(x, y, model_func, params_nodrag, params_drag, title, filename):
    resid_nodrag = y - no_drag_model(params_nodrag, x)
    resid_drag = y - drag_model(params_drag, x)

    plt.figure(figsize=(7, 4))
    plt.axhline(0, color="grey", lw=1)
    plt.scatter(x, resid_nodrag, color="darkorange", marker="^", label="No-drag residuals (Eq. 1)")
    plt.scatter(x, resid_drag, color="navy", marker="o", label="Drag residuals (Eq. 4)")
    plt.xlabel("t (s)")
    plt.ylabel("residual (m/s)")
    plt.title(title)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()


def sigma_test(ratio_measured, ratio_err, ratio_predicted):
    sigma_diff = abs(ratio_measured - ratio_predicted) / ratio_err
    print("SIGMA TEST")
    print(f"measured vT ratio  : {ratio_measured:.3f} +/- {ratio_err:.3f}")
    print(f"predicted vT ratio : {ratio_predicted:.3f} (sqrt(2), from mg = C*vT^2, C constant)")
    print(f"discrepancy: {sigma_diff:.2f} sigma")

    if sigma_diff <= 3.0:
        print("results AGREE within experimental uncertainty")
    else:
        print("results DISAGREE")


def analyse_pan(label, csv_path, graph_dir):
    t_data, vy_data = load_data(csv_path)
    v0_guess = vy_data[0].n
    vT_guess = max(abs(v) for v in [v.n for v in vy_data]) * 1.5

    params_nodrag, err_nodrag, plot_data1 = odr_fit(
        t_data, vy_data, no_drag_model, beta0=[v0_guess]
    )
    params_drag, err_drag, plot_data2 = odr_fit(
        t_data, vy_data, drag_model, beta0=[v0_guess, vT_guess]
    )
    x, y, sx, sy = plot_data2  

    print(f"\n{'='*60}\n{label}\n{'='*60}")
    print("point-by-point data")
    for i in range(len(x)):
        print(f"point {i+1}: t = {x[i]:.4f} +/- {sx[i]:.4f} | vy = {y[i]:.4f} +/- {sy[i]:.4f}")

    v0_nodrag = ufloat(params_nodrag[0], err_nodrag[0])
    v0_drag = ufloat(params_drag[0], err_drag[0])
    vT_drag = ufloat(params_drag[1], err_drag[1])

    print(f"no-drag fit (Eq. 1): v0 = {v0_nodrag:.3f} m/s")
    print(f"drag fit    (Eq. 4): v0 = {v0_drag:.3f} m/s, vT = {vT_drag:.3f} m/s")

    plot(
        x, y, sx, sy,
        drag_model, params_drag,
        label=f"Drag fit: $v_T = {vT_drag.n:.2f} \\pm {vT_drag.s:.2f}$ m/s",
        xlabel="Time $t$ (s)",
        ylabel="Velocity $v_y$ (m/s)",
        title=f"{label}: Drag Model Fit",
        filename=f"{graph_dir}/{label.lower().replace(' ', '_')}_drag_fit.png",
    )

    residual_plot(
        x, y, drag_model, params_nodrag, params_drag,
        title=f"{label}: Residuals (No-Drag vs Drag Model)",
        filename=f"{graph_dir}/{label.lower().replace(' ', '_')}_residuals.png",
    )

    return v0_nodrag, v0_drag, vT_drag


def main():
    print("DATA ANALYSIS")
    graph_dir = "graphs"

    _, _, vT_single = analyse_pan("Single patty pan", "data_single_pan.csv", graph_dir)
    _, _, vT_double = analyse_pan("Two nested patty pans", "data_double_pan.csv", graph_dir)

    ratio = vT_double / vT_single
    print(f"\nvT (single)  = {vT_single:.3f} m/s")
    print(f"vT (double)  = {vT_double:.3f} m/s")
    print(f"measured vT ratio = {ratio:.3f}")

    sigma_test(ratio.n, ratio.s, np.sqrt(2))

if __name__ == "__main__":
    main()