import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData
from scipy import stats
from dataclasses import dataclass
from uncertainties import ufloat

LASER_WAVEL_cm = ufloat(654e-9, 2e-9)  # m, stated laser wavel_cm
SLIT_WIDTH_NOM = ufloat(0.04e-3, 0.05 * 0.04e-3)  # m, 5% manufacturer tolerance
SLIT_SEP_NOM = ufloat(0.25e-3, 0.05 * 0.25e-3)  # m, 5% manufacturer tolerance


# funcs

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

def odr_fit(x, y, model_func, beta0, x_err=None, y_err=None):
    x_nom = np.asarray(x, dtype=float)
    y_nom = np.asarray(y, dtype=float)

    if x_err is None:
        x_err = np.full_like(x_nom, 1e-12)
    if y_err is None:
        y_err = np.full_like(y_nom, 1e-12)
    x_err = np.asarray(x_err, dtype=float)
    y_err = np.asarray(y_err, dtype=float)

    model = Model(model_func)
    data = RealData(x_nom, y_nom, sx=x_err, sy=y_err)
    odr_obj = ODR(data, model, beta0=beta0)
    odr_result = odr_obj.run()

    converged = "converge" in odr_result.stopreason[0].lower() or odr_result.info in (1, 2, 3)

    y_pred = model_func(odr_result.beta, x_nom)
    residuals = y_nom - y_pred
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y_nom - np.mean(y_nom)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    rmse = np.sqrt(np.mean(residuals ** 2))

    dof = len(x_nom) - len(odr_result.beta)
    reduced_chi_squared = odr_result.res_var if dof > 0 else np.nan

    return odr_fit_result(
        parameters=odr_result.beta,
        parameter_errors=odr_result.sd_beta,
        r_squared=r_squared,
        rmse=rmse,
        reduced_chi_squared=reduced_chi_squared,
        converged=converged,
        x_nom=x_nom,
        y_nom=y_nom,
        x_err=x_err,
        y_err=y_err,
    )


def chi_squared_test(chi2_stat, dof):
    """p-value for a chi-squared statistic with dof degrees of freedom."""
    p_value = stats.chi2.sf(chi2_stat, dof)
    return p_value


def sigma_test(k1, sk1, k2, sk2, label=""):
    """Discrepancy between two values in units of combined sigma."""
    diff = abs(k1 - k2)
    combined_sigma = np.sqrt(sk1 ** 2 + sk2 ** 2)
    n_sigma = diff / combined_sigma if combined_sigma > 0 else np.nan
    print(f"{label}: {k1:.6g} +/- {sk1:.2g} vs {k2:.6g} +/- {sk2:.2g} "
          f"-> {n_sigma:.2f} sigma")
    return n_sigma

def linear_model(beta, x):
    """y = m*x + c"""
    return beta[0] * x + beta[1]

def linear_origin_model(beta, x):
    """y = m*x (forced through the origin, for fringe order vs position)"""
    return beta[0] * x

def pixel_to_metres(pixel_positions, pixel_err, l_cm, l_px, s_l):
    """
    Convert pixel positions on the frosted screen to metres using the
    electrical-tape calibration image.
    """
    scale = l_cm / l_px  # m / pixel
    scale_err = scale * (s_l / l_px)

    x_m = np.asarray(pixel_positions, dtype=float) * scale
    x_m_err = np.sqrt((np.asarray(pixel_err, dtype=float) * scale) ** 2
                       + (np.asarray(pixel_positions, dtype=float) * scale_err) ** 2)
    return x_m, x_m_err

def plot_fit(x, y, x_err, y_err, fit_result, model_func, xlabel, ylabel, title, filename):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt="o", color="navy",
                ecolor="crimson", capsize=3, label="data", zorder=3)

    x_fit = np.linspace(min(x), max(x), 300)
    y_fit = model_func(fit_result.parameters, x_fit)
    ax.plot(x_fit, y_fit, "k--", label="ODR fit", zorder=2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=300)
    plt.close(fig)


# single slit diffraction -> laser wavel_cm
def analyse_single_slit(csv_path, l_cm, l_px, s_l, L, L_err):
    """
    csv columns expected: order_m, minima_pixel, minima_pixel_err
    y_dark = L * m * lambda / w  ->  fit y vs m, slope = L*lambda/w
    """
    df = pd.read_csv(csv_path)
    y_m, y_m_err = pixel_to_metres(df["minima_pixel"], df["minima_pixel_err"],
                                    l_cm, l_px, s_l)

    fit = odr_fit(df["order_m"], y_m, linear_origin_model, beta0=[1e-3])
    slope, slope_err = fit.parameters[0], fit.parameter_errors[0]

    L_val = ufloat(L, L_err)
    slope_u = ufloat(slope, slope_err)
    wavel_cm = slope_u * SLIT_WIDTH_NOM / L_val

    print("\n--- Single slit diffraction (wavel_cm) ---")
    print(f"slope (L*lambda/w) = {slope:.6g} +/- {slope_err:.2g} m")
    print(f"reduced chi^2 = {fit.reduced_chi_squared:.3f}, converged = {fit.converged}")
    print(f"derived wavel_cm = {wavel_cm.n * 1e9:.2f} +/- {wavel_cm.s * 1e9:.2f} nm")
    sigma_test(wavel_cm.n, wavel_cm.s, LASER_WAVEL_cm.n, LASER_WAVEL_cm.s,
               label="Measured vs stated laser wavel_cm")

    plot_fit(df["order_m"], y_m, np.zeros(len(df)), y_m_err, fit, linear_origin_model,
              xlabel="Fringe order m", ylabel="Minima position (m)",
              title="Single slit diffraction: minima position vs order",
              filename="single_slit_diffraction.png")
    return wavel_cm, fit


# double slit interference -> slit spacing d
def analyse_double_slit(csv_path, l_cm, l_px, s_l, L, L_err):
    """
    csv columns expected: order_m, maxima_pixel, maxima_pixel_err
    y_bright = L * m * lambda / d  ->  fit y vs m, slope = L*lambda/d
    """
    df = pd.read_csv(csv_path)
    y_m, y_m_err = pixel_to_metres(df["maxima_pixel"], df["maxima_pixel_err"],
                                    l_cm, l_px, s_l)

    fit = odr_fit(df["order_m"], y_m, linear_origin_model, beta0=[1e-3])
    slope, slope_err = fit.parameters[0], fit.parameter_errors[0]

    L_val = ufloat(L, L_err)
    slope_u = ufloat(slope, slope_err)
    spacing = L_val * LASER_WAVEL_cm / slope_u

    print("\n--- Double slit interference (slit spacing) ---")
    print(f"slope (L*lambda/d) = {slope:.6g} +/- {slope_err:.2g} m")
    print(f"reduced chi^2 = {fit.reduced_chi_squared:.3f}, converged = {fit.converged}")
    print(f"derived spacing d = {spacing.n * 1e3:.4f} +/- {spacing.s * 1e3:.4f} mm")
    sigma_test(spacing.n, spacing.s, SLIT_SEP_NOM.n, SLIT_SEP_NOM.s,
               label="Measured vs stated slit spacing")

    plot_fit(df["order_m"], y_m, np.zeros(len(df)), y_m_err, fit, linear_origin_model,
              xlabel="Fringe order m", ylabel="Maxima position (m)",
              title="Double slit interference: maxima position vs order",
              filename="double_slit_interference.png")
    return spacing, fit


# babinet's principle - slit vs opaque line diffraction pattern
def analyse_babinet(slit_csv, line_csv, l_cm, l_px, s_l):
    """
    csv columns expected: pixel, intensity (raw ImageJ Plot Profile output)
    Overlays the 0.08 mm slit and 0.08 mm opaque-line diffraction patterns.
    Babinet's principle predicts identical patterns away from the central
    order, with the central spot differing in intensity between the two.
    """
    slit_df = pd.read_csv(slit_csv)
    line_df = pd.read_csv(line_csv)

    slit_x, _ = pixel_to_metres(slit_df["pixel"], np.zeros(len(slit_df)),
                                 l_cm, l_px, s_l)
    line_x, _ = pixel_to_metres(line_df["pixel"], np.zeros(len(line_df)),
                                 l_cm, l_px, s_l)

    slit_norm = slit_df["intensity"] / slit_df["intensity"].max()
    line_norm = line_df["intensity"] / line_df["intensity"].max()

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(slit_x, slit_norm, color="navy", label="0.08 mm slit")
    ax.plot(line_x, line_norm, color="crimson", linestyle="--", label="0.08 mm opaque line")
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Normalised intensity")
    ax.set_title("Babinet's principle: slit vs opaque line diffraction pattern")
    ax.legend()
    fig.tight_layout()
    fig.savefig("babinet_principle.png", dpi=300)
    plt.close(fig)

    print("\n--- Babinet's principle (slit vs opaque line) ---")
    print("Check babinet_principle.png: minima/secondary-maxima positions should")
    print("coincide for the two patterns away from the central order, per Babinet's")
    print("principle; only the central spot intensity is expected to differ.")


# hair thickness via single-slit-type diffraction
def analyse_hair_thickness(csv_path, l_cm, l_px, s_l,
                            L, L_err, micrometer_value, micrometer_err):
    """
    csv columns expected: order_m, minima_pixel, minima_pixel_err
    Same y_dark = L*m*lambda/w relation as the single slit case, solved
    for w this time instead of lambda.
    """
    df = pd.read_csv(csv_path)
    y_m, y_m_err = pixel_to_metres(df["minima_pixel"], df["minima_pixel_err"],
                                    l_cm, l_px, s_l)

    fit = odr_fit(df["order_m"], y_m, linear_origin_model, beta0=[1e-3])
    slope, slope_err = fit.parameters[0], fit.parameter_errors[0]

    L_val = ufloat(L, L_err)
    slope_u = ufloat(slope, slope_err)
    hair_thickness = L_val * LASER_WAVEL_cm / slope_u

    micrometer_u = ufloat(micrometer_value, micrometer_err)

    print("\n--- Hair thickness (diffraction vs micrometer) ---")
    print(f"slope (L*lambda/w) = {slope:.6g} +/- {slope_err:.2g} m")
    print(f"reduced chi^2 = {fit.reduced_chi_squared:.3f}, converged = {fit.converged}")
    print(f"diffraction-derived thickness = {hair_thickness.n * 1e6:.2f} +/- "
          f"{hair_thickness.s * 1e6:.2f} um")
    sigma_test(hair_thickness.n, hair_thickness.s, micrometer_u.n, micrometer_u.s,
               label="Diffraction vs micrometer hair thickness")

    plot_fit(df["order_m"], y_m, np.zeros(len(df)), y_m_err, fit, linear_origin_model,
              xlabel="Fringe order m", ylabel="Minima position (m)",
              title="Hair diffraction: minima position vs order",
              filename="hair_thickness_diffraction.png")
    return hair_thickness, fit


# multiple slit interference - principal maximum narrowing with N
def multiple_slit_fwhm_model(beta, N):
    """FWHM = A / N, expected narrowing of the principal maximum with N slits"""
    return beta[0] / N

def analyse_multiple_slit(csv_paths, N_values, l_cm, l_px, s_l):
    """
    csv_paths: dict {N: path}, each csv columns pixel, intensity
    Overlays the N = 2,3,4,5 patterns and fits the principal maximum FWHM
    against N to check the expected 1/N narrowing.
    """
    fwhm_m = []
    fwhm_err = []
    colors = ["navy", "crimson", "darkgreen", "darkorange"]

    fig, ax = plt.subplots(figsize=(7, 5))
    for i, N in enumerate(N_values):
        df = pd.read_csv(csv_paths[N])
        x_m, x_m_err = pixel_to_metres(df["pixel"], np.zeros(len(df)),
                                        l_cm, l_px, s_l)
        intensity_norm = df["intensity"] / df["intensity"].max()

        ax.plot(x_m, intensity_norm, color=colors[i % len(colors)], label=f"N = {N}")

        half_max_mask = intensity_norm >= 0.5
        fwhm = x_m[half_max_mask].max() - x_m[half_max_mask].min()
        fwhm_m.append(fwhm)
        fwhm_err.append(np.mean(x_m_err))  # TODO: refine if you want a tighter FWHM uncertainty

    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Normalised intensity")
    ax.set_title("Multiple slit interference: principal maximum narrowing with N")
    ax.legend()
    fig.tight_layout()
    fig.savefig("multiple_slit_interference.png", dpi=300)
    plt.close(fig)

    fit = odr_fit(N_values, fwhm_m, multiple_slit_fwhm_model, beta0=[1e-4], y_err=fwhm_err)
    A, A_err = fit.parameters[0], fit.parameter_errors[0]

    print("\n--- Multiple slit interference (principal maximum FWHM vs N) ---")
    print(f"FWHM = A/N fit: A = {A:.4g} +/- {A_err:.2g} m")
    print(f"reduced chi^2 = {fit.reduced_chi_squared:.3f}, converged = {fit.converged}")

    x_fit = np.linspace(min(N_values), max(N_values), 300)
    y_fit = multiple_slit_fwhm_model(fit.parameters, x_fit)
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    ax2.errorbar(N_values, fwhm_m, yerr=fwhm_err, fmt="o", color="navy",
                 ecolor="crimson", capsize=3, label="data", zorder=3)
    ax2.plot(x_fit, y_fit, "k--", label="A/N fit", zorder=2)
    ax2.set_xlabel("Number of slits N")
    ax2.set_ylabel("Principal maximum FWHM (m)")
    ax2.set_title("Principal maximum FWHM vs number of slits")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig("multiple_slit_fwhm_fit.png", dpi=300)
    plt.close(fig2)

    return fit


if __name__ == "__main__":
    l_cm = 0.010          # TODO: known l_cm of tape used, metres
    l_px = 100.0         # TODO: measured l_cm in pixels
    s_l = 1.0       # TODO: pixel-reading uncertainty

    L_SLIT_TO_SCREEN = 0.50       # TODO: measured distance, metres
    L_SLIT_TO_SCREEN_ERR = 0.005  # TODO: uncertainty, metres

    # 1
    analyse_single_slit(
        csv_path="single_slit_data.csv",  # TODO: order_m, minima_pixel, minima_pixel_err
        l_cm=l_cm, l_px=l_px,
        s_l=s_l,
        L=L_SLIT_TO_SCREEN, L_err=L_SLIT_TO_SCREEN_ERR,
    )

    # 2
    analyse_double_slit(
        csv_path="double_slit_data.csv",  # TODO: order_m, maxima_pixel, maxima_pixel_err
        l_cm=l_cm, l_px=l_px,
        s_l=s_l,
        L=L_SLIT_TO_SCREEN, L_err=L_SLIT_TO_SCREEN_ERR,
    )

    # 3
    analyse_babinet(
        slit_csv="babinet_slit_data.csv",  # TODO: pixel, intensity
        line_csv="babinet_line_data.csv",  # TODO: pixel, intensity
        l_cm=l_cm, l_px=l_px,
        s_l=s_l,
    )

    # 4
    analyse_hair_thickness(
        csv_path="hair_data.csv",  # TODO: order_m, minima_pixel, minima_pixel_err
        l_cm=l_cm, l_px=l_px,
        s_l=s_l,
        L=L_SLIT_TO_SCREEN, L_err=L_SLIT_TO_SCREEN_ERR,
        micrometer_value=70e-6, micrometer_err=5e-6,  # TODO: your micrometer reading
    )

    # 5
    analyse_multiple_slit(
        csv_paths={  # TODO: pixel, intensity for each N
            2: "multi_slit_N2_data.csv",
            3: "multi_slit_N3_data.csv",
            4: "multi_slit_N4_data.csv",
            5: "multi_slit_N5_data.csv",
        },
        N_values=[2, 3, 4, 5],
        l_cm=l_cm, l_px=l_px,
        s_l=s_l,
    )