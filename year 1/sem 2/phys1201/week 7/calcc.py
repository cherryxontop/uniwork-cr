import os
import numpy as np
import pandas as pd

# ---- your numbers ---------------------------------------------------------
L, sL = 0.879, 0.003        # slit-to-screen distance (m)
LAM, sLAM = 654e-9, 2e-9    # laser wavelength (m)
POS = 0.0003                # reading error on one minimum/maximum position (m)
TOL = 0.05                  # 5% slit tolerance

FOLDER = "files"            # folder with the csv files (leave "" if same folder)


def sigma_test(k1, sk1, k2, sk2, label="parameter"):
    sigma_diff = abs(k1 - k2) / np.sqrt(sk1**2 + sk2**2)
    print(f"\nSIGMA TEST ({label})")
    print(f"measured value    : {k1:.3f} +/- {sk1:.3f}")
    print(f"theoretical value : {k2:.3f} +/- {sk2:.3f}")
    print(f"discrepancy       : {sigma_diff:.2f} sigma")
    print("results AGREE within experimental uncertainty" if sigma_diff <= 3.0 else "results DISAGREE")
    return sigma_diff


def load(file):
    df = pd.read_csv(os.path.join(FOLDER, file))
    return df.iloc[:, 0].values * 0.01, df.iloc[:, 1].values     # cm -> m


def smooth(y, n=15):
    return np.convolve(y, np.ones(n) / n, mode="same")


def find_points(x, y, kind, w, frac=0.03):
    """Positions where the smoothed curve is the lowest/highest point within +-w
    points, and stands out by more than frac of the full range."""
    ys = smooth(y)
    depth = frac * (ys.max() - ys.min())
    hit = (lambda i, seg: ys[i] == seg.min() and seg.max() - ys[i] > depth) if kind == "min" \
        else (lambda i, seg: ys[i] == seg.max() and ys[i] - seg.min() > depth)
    return np.array([x[i] for i in range(w, len(ys) - w) if hit(i, ys[i - w:i + w + 1])])


def minima_slope(file, first_order=1, w=40):
    """y_m = distance of minimum m from the centre. Fit y_m = slope * m."""
    x, y = load(file)
    mins = find_points(x, y, "min", w)
    peak = x[np.argmax(smooth(y))]
    left, right = mins[mins < peak][::-1], mins[mins > peak]
    centre = (left[0] + right[0]) / 2
    left, right = mins[mins < centre][::-1], mins[mins > centre]
    ym = np.concatenate([centre - left, right - centre])
    m = np.concatenate([np.arange(len(left)), np.arange(len(right))]) + first_order

    slope = np.sum(m * ym) / np.sum(m**2)
    s_fit = np.sqrt(np.sum((ym - slope * m) ** 2) / (len(m) - 1) / np.sum(m**2)) if len(m) > 1 else 0
    s_slope = max(s_fit, POS / np.sqrt(np.sum(m**2)))

    print(f"\n{file}: minima at {np.round(mins * 100, 3)} cm, centre {centre * 100:.3f} cm")
    print(f"  m = {m}, y_m = {np.round(ym * 100, 3)} cm")
    print(f"  slope = {slope * 100:.4f} +/- {s_slope * 100:.4f} cm")
    return slope, s_slope


def solve_from_slope(file, solve_for, known, known_rel_err, first_order=1, w=40):
    """slope = L*lambda/width. Give the known quantity (width or wavelength) and
    get the other one back, with its propagated relative uncertainty. Used by
    single_slit, hair, and the slit half of babinet - they're all the same
    y = L*m*lambda/w relation, just solved for a different unknown."""
    slope, s_slope = minima_slope(file, first_order, w)
    val = slope * known / L if solve_for == "wavelength" else L * known / slope
    rel = np.sqrt((s_slope / slope) ** 2 + known_rel_err ** 2 + (sL / L) ** 2)
    return val, val * rel


def single_slit(file, w=0.04e-3):
    lam, s_lam = solve_from_slope(file, "wavelength", known=w, known_rel_err=TOL)
    print(f"  wavelength = {lam * 1e9:.1f} +/- {s_lam * 1e9:.1f} nm")
    sigma_test(lam * 1e9, s_lam * 1e9, LAM * 1e9, sLAM * 1e9, "wavelength, nm")


def double_slit(file, d_stated=0.25e-3, x_from=0.013, x_to=1.0):
    """Uses the bright fringes between x_from and x_to (m) - skips the weak outer ones."""
    x, y = load(file)
    peaks = find_points(x, y, "max", 15)
    peaks = peaks[(peaks > x_from) & (peaks < x_to)]
    gap = np.median(np.diff(peaks))
    k = np.round((peaks - peaks[0]) / gap)
    dy = np.polyfit(k, peaks, 1)[0]
    s_dy = POS / np.sqrt(np.sum((k - k.mean()) ** 2))
    d = LAM * L / dy
    rel = np.sqrt((s_dy / dy) ** 2 + (sLAM / LAM) ** 2 + (sL / L) ** 2)
    print(f"\n{file}: peaks at {np.round(peaks * 100, 3)} cm")
    print(f"  fringe numbers {k.astype(int)}")
    print(f"  fringe spacing = {dy * 1e3:.4f} mm, d = {d * 1e6:.1f} +/- {d * rel * 1e6:.1f} um")
    sigma_test(d * 1e6, d * rel * 1e6, d_stated * 1e6, TOL * d_stated * 1e6, "slit separation, um")


def babinet(slit_file, line_file, w=0.08e-3):
    width, s_width = solve_from_slope(slit_file, "width", known=LAM, known_rel_err=sLAM / LAM, w=25)
    print(f"  slit width from pattern = {width * 1e6:.1f} +/- {s_width * 1e6:.1f} um")
    sigma_test(width * 1e6, s_width * 1e6, w * 1e6, TOL * w * 1e6, "slit width vs nominal, um")

    x, y = load(line_file)
    mins = find_points(x, y, "min", 40)
    slope1 = LAM * L / width  # back out the slope used above, for the comparison note
    print(f"\n{line_file}: minima found at {np.round(mins * 100, 3)} cm")
    print(f"  slit minima are at +-{slope1 * 100:.3f} cm and +-{2 * slope1 * 100:.3f} cm from its centre")


def hair(file, first_order=2):
    w, s_w = solve_from_slope(file, "width", known=LAM, known_rel_err=sLAM / LAM, first_order=first_order, w=30)
    print(f"  hair thickness = {w * 1e6:.1f} +/- {s_w * 1e6:.1f} um")


# ---- run the experiments (comment out any you don't want) ------------------
single_slit("singleslit.csv", w=0.04e-3)
double_slit("doubleslit.csv", d_stated=0.25e-3)
babinet("babinetslit.csv", "babinet_opaque.csv", w=0.08e-3)
hair("hair.csv", first_order=2)