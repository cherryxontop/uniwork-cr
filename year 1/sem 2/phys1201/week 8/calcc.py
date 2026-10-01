import numpy as np

# constants
L, sL = 0.879, 0.003        # slit-to-screen distance (m)
LAM, sLAM = 654e-9, 2e-9    # laser wavelength (m)
POS = 0.0003                # uncertainty on reading one position off the plot (m) = 0.03 cm
TOL = 0.05                  # 5% slit tolerance


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


def half_separation(x_left, x_right):
    y = (x_right - x_left) / 2 * 0.01
    sy = POS / np.sqrt(2)
    return y, sy


# single slit -> wavelength
def single_slit(x_left, x_right, w=0.04e-3, m=1):
    y, sy = half_separation(x_left, x_right)
    lam = w * y / (m * L)
    rel = np.sqrt((sy / y) ** 2 + TOL**2 + (sL / L) ** 2)
    print(f"\nSingle slit: \ny_{m} = {y * 100:.3f} cm")
    print(f"wavelength = {lam * 1e9:.1f} +/- {lam * rel * 1e9:.1f} nm")
    sigma_test(lam * 1e9, lam * rel * 1e9, LAM * 1e9, sLAM * 1e9, "wavelength, nm")


# double slit -> slit separation
def double_slit(x_first, x_last, n_gaps, d_stated=0.25e-3):
    dy = (x_last - x_first) * 0.01 / n_gaps
    sdy = np.sqrt(2) * POS / n_gaps
    d = LAM * L / dy
    rel = np.sqrt((sdy / dy) ** 2 + (sLAM / LAM) ** 2 + (sL / L) ** 2)
    print(f"\nDouble slit: \nfringe spacing = {dy * 1e3:.3f} mm")
    print(f"d = {d * 1e6:.1f} +/- {d * rel * 1e6:.1f} um")
    sigma_test(d * 1e6, d * rel * 1e6, d_stated * 1e6, TOL * d_stated * 1e6, "slit separation, um")


# width from minima
def width_from_minima(x_left, x_right, m):
    y, sy = half_separation(x_left, x_right)
    w = m * LAM * L / y
    rel = np.sqrt((sy / y) ** 2 + (sLAM / LAM) ** 2 + (sL / L) ** 2)
    return w, w * rel


def babinet(x_left, x_right, m, w_nominal=0.08e-3):
    w, sw = width_from_minima(x_left, x_right, m)
    print(f"\nBabinet slit (m={m} minima): \nwidth = {w * 1e6:.1f} +/- {sw * 1e6:.1f} um")
    sigma_test(w * 1e6, sw * 1e6, w_nominal * 1e6, TOL * w_nominal * 1e6, f"slit width vs nominal, m={m}, um")


def hair(x_left, x_right, m, micrometer=None, s_micrometer=0.005e-3):
    w, sw = width_from_minima(x_left, x_right, m)
    print(f"\nHair (m={m} minima):\nthickness = {w * 1e6:.1f} +/- {sw * 1e6:.1f} um")
    if micrometer is not None:
        sigma_test(w * 1e6, sw * 1e6, micrometer * 1e6, s_micrometer * 1e6, f"hair thickness, m={m}, um")


# readings
single_slit(1.067, 3.544)
double_slit(1.193, 3.154, 10)
babinet(1.147, 2.443, 1)
babinet(0.545, 3.022, 2)
hair(1.313, 3.234, 2, micrometer=115e-6)
hair(0.866, 3.653, 3, micrometer=115e-6)