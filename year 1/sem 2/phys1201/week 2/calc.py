import warnings
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from uncertainties import ufloat

g = 9.796

# functions

def odr_fit(x_data, y_data):
    x = [v.n for v in x_data]
    sx = [v.s for v in x_data]
    y = [v.n for v in y_data]
    sy = [v.s for v in y_data]

    linear_model = odr.Model(lambda p, x: p[0] * x + p[1])
    data = odr.RealData(x, y, sx=sx, sy=sy)
    odr_result = odr.ODR(data, linear_model, beta0=[10.0, 0.0]).run()

    slope = odr_result.beta[0]
    slope_err = odr_result.sd_beta[0]
    intercept = odr_result.beta[1]

    return slope, slope_err, intercept, (x, y, sx, sy)


def plot(
    x,
    y,
    sx,
    sy,
    slope,
    slope_err,
    intercept,
    xlabel,
    ylabel,
    title,
    filename,):

    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = slope * x_fit + intercept

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
        label="Experimental Data",
    )
    plt.plot(
        x_fit,
        y_fit,
        "k--",
        label=f"Fit: $k = {slope:.2f} \\pm {slope_err:.2f}$ N/m",
    )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def evaluate_sigma_test(k1, sk1, k2, sk2):
    sigma_diff = abs(k1 - k2) / np.sqrt(sk1**2 + sk2**2)
    print("SIGMA TEST")
    print(f"Static k  : {k1:.3f} +/- {sk1:.3f} N/m")
    print(f"Dynamic k : {k2:.3f} +/- {sk2:.3f} N/m")
    print(f"Discrepancy: {sigma_diff:.2f} sigma")

    if sigma_diff <= 2.0:
        print(
            "results AGREE within experimental uncertainty yayyay"
        )
    else:
        print(
            "results DISAGREE (> 2sigma). check for errors idiot."
        )

def static_method():
    x0 = ufloat(0.30, 0.0025)           # initial spring length (m)
    m_slot = ufloat(0.050, 0.0001)      # mass per slot (kg)

    total_lengths_cm = []
    total_lengths = [ufloat(L / 100.0, 0.0025) for L in total_lengths_cm]

    total_masses = [i * m_slot for i in range(1, 9)]
    force = [m * g for m in total_masses]
    extension = [L - x0 for L in total_lengths]

    k, sk, intercept, plot_data = odr_fit(extension, force)

    plot(
        *plot_data,
        k,
        sk,
        intercept,
        xlabel="Extension $x$ (m)",
        ylabel="Applied Force $mg$ (N)",
        title="Static Determination of Spring Constant ($k$)",
        filename="/Users/chhaya/Documents/uniwork-cr/year 1/sem 2/phys1201/week 2/graphs/static_k_plot.png",
    )

    return k, sk, total_masses

def dynamic_method(total_masses):

    time_20_osc = []
    spring_mass = ufloat(0.043627, 0.000001)  # Spring mass in kg[cite: 1]

    periods = [ufloat(t, 0.10) / 20.0 for t in time_20_osc]
    x_dynamic = [(T / (2 * np.pi)) ** 2 for T in periods]
    y_dynamic = [m + (spring_mass / 3.0) for m in total_masses]

    k, sk, intercept, plot_data = odr_fit(x_dynamic, y_dynamic)

    plot(
        *plot_data,
        k,
        sk,
        intercept,
        xlabel="$(T / 2\\pi)^2$ ($\text{s}^2$)",
        ylabel="Effective Mass $m + m_s/3$ (kg)",
        title="Dynamic Determination of Spring Constant ($k$)",
        filename="/Users/chhaya/Documents/uniwork-cr/year 1/sem 2/phys1201/week 2/graphs/dynamic_k_plot.png",
    )

    return k, sk

def main():
    print("DATA ANALYSIS")

    k_stat, sk_stat, total_masses = static_method()
    print(f"static method results: k = {k_stat:.3f} +/- {sk_stat:.3f} N/m")

    k_dyn, sk_dyn = dynamic_method(total_masses)
    print(f"dynamic method results: k = {k_dyn:.3f} +/- {sk_dyn:.3f} N/m")

    evaluate_sigma_test(k_stat, sk_stat, k_dyn, sk_dyn)


if __name__ == "__main__":
    main()