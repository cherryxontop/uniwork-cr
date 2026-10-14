import numpy as np

d = 1e-3 / 600              # grating spacing (m), 600 lines/mm
sANG = 0.33                 # uncertainty on reading one angle off the degree scale (one division, deg), from the demonstrator

# from the lab notes: (wavelength nm, element)
spectral_lines = [
    (706.5, "He"),
    (703.2, "Ne"),
    (670.8, "Li"),
    (667.8, "He"),
    (650.6, "Ne"),
    (643.8, "Cd"),
    (640.2, "Ne"),
    (636.2, "Zn"),
    (633.4, "Ne"),
    (610, "Eu"),
    (589.0, "Na"),
    (589.6, "Na"),
    (587.5, "He"),
    (579, "Hg"),
    (576.9, "Hg"),
    (546.1, "Hg"),
    (508.6, "Cd"),
    (501.5, "He"),
    (481, "Zn"),
    (480, "Cd"),
    (472, "Zn"),
    (467.8, "Cd"),
    (460.3, "Li"),
    (447.1, "He"),
    (435.8, "Hg"),
    (404.6, "Hg"),
    (388.8, "He"),
    (365.4, "Hg"),
    (360, "Cd")
]


def sigma_test(k1, sk1, k2, sk2):
    sigma_diff = abs(k1 - k2) / np.sqrt(sk1**2 + sk2**2)

    print(f"\nSIGMA TEST")
    print(f"measured value    : {k1:.3f} +/- {sk1:.3f}")
    print(f"accepted value    : {k2:.3f} +/- {sk2:.3f}")
    print(f"discrepancy       : {sigma_diff:.2f} sigma")

    if sigma_diff <= 3.0:
        print("results AGREE within experimental uncertainty")
    else:
        print("results DISAGREE")

    return sigma_diff


# centre of the pattern from the mercury line read on both sides
def centre(left, right):
    mid = (left + right) / 2
    smid = sANG / np.sqrt(2)
    print(f"\ncentre = {mid:.4f} +/- {smid:.4f} deg")
    return mid, smid


def centre_wavelength(x_left, x_right, n):
    theta = np.radians(abs(x_left - x_right) / 2)
    stheta = np.radians(sANG / np.sqrt(2))
    lam = d * np.sin(theta) / n * 1e9
    slam = d * np.cos(theta) * stheta / n * 1e9
    print(f"\nlambda = {lam:.1f} +/- {slam:.1f} nm")
    return lam, slam


# first order wavelength of one reading, measured from the centre
def wavelength(x, mid, smid, n):
    theta = np.radians(abs(x - mid))
    stheta = np.radians(np.sqrt(sANG**2 + smid**2))
    lam = d * np.sin(theta) / n * 1e9
    slam = d * np.cos(theta) * stheta / n * 1e9
    return lam, slam


# closest line to each reading of one lamp
def identify(readings, mid, smid, n):
    for x in readings:
        lam, slam = wavelength(x, mid, smid, n)
        w, el = min(spectral_lines, key=lambda line: abs(line[0] - lam))
        print(f"centre {mid:.2f} deg")
        print(f"calculated wavelength: {lam:.1f} +/- {slam:.1f} nm")
        print(f"closest line in list: {el} {w} nm")
        sigma_test(lam, slam, w, 0)


# readings (degrees + minutes / 60)
centre(107 + 6 / 60, 92)
mid, smid = centre(148 + 8 / 60, 67 + 3 / 60) 
centre_wavelength(107 + 6 / 60, 92, 1)
centre_wavelength(148 + 8 / 60, 67 + 3 / 60, 2)
identify([84 + 30/60], mid, smid, 1)