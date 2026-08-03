import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from uncertainties import ufloat

g = 9.796

# static method
x_0 = 0.150  
m_static = np.array([])         # mass in kg
x_total = np.array([0.171, 0.192, 0.213, 0.235, 0.254])     # total length in me

x_static = x_total - x_0
sx_static = np.array([0.001] * len(m_static))  

# dynamic method
m_dynamic = np.array([])    # mass in kg
T_dynamic = np.array([])    # period T in s
sT = np.array([] * len(m_dynamic))                  # period uncertainty in s

T2 = T_dynamic**2
sT2 = 2 * T_dynamic * sT  


# STATIC METHOD LINE FITTING
# y = mx + c
X_stat = sm.add_constant(m_static)
weights_stat = 1.0 / (sx_static**2)

fit_stat = sm.WLS(x_static, X_stat, weights=weights_stat).fit()
c_stat, slope_stat = fit_stat.params[0], fit_stat.params[1]
sc_stat, sslope_stat = fit_fit_err = fit_stat.bse[0], fit_stat.bse[1]

# calculate k and uncert
k_stat_val = g / slope_stat
sk_stat_val = k_stat_val * (sslope_stat / slope_stat)
k_stat = ufloat(k_stat_val, sk_stat_val)

print("STATIC METHOD RESULTS")
print(f"slope (x vs m) : {slope_stat:.4f} +/- {sslope_stat:.4f} m/kg")
print(f"spring constant: {k_stat} N/m\n")

# static Plot
plt.figure()
plt.errorbar(
    m_static,
    x_static,
    yerr=sx_static,
    fmt="o",
    capsize=4,
    color="black",
    ecolor="red",
)
plt.plot(m_static, slope_stat * m_static + c_stat, color="blue")
plt.xlabel("mass $m$ (kg)")
plt.ylabel("extension $x$ (m)")
plt.title("static method: extension vs mass")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 2/phys1201/week 1/static_method_fit.png", dpi=300)
plt.show()


# STATIC METHOD LINE FITTING
# y = mx + c
X_dyn = sm.add_constant(m_dynamic)
weights_dyn = 1.0 / (sT2**2)

fit_dyn = sm.WLS(T2, X_dyn, weights=weights_dyn).fit()
c_dyn, slope_dyn = fit_dyn.params[0], fit_dyn.params[1]
sc_dyn, sslope_dyn = fit_dyn.bse[0], fit_dyn.bse[1]

# calculate k and uncert
k_dyn_val = (4 * np.pi**2) / slope_dyn
sk_dyn_val = k_dyn_val * (sslope_dyn / slope_dyn)
k_dyn = ufloat(k_dyn_val, sk_dyn_val)

print("DYNAMIC METHOD RESULTS")
print(f"slope (T^2 vs m): {slope_dyn:.4f} +/- {sslope_dyn:.4f} s^2/kg")
print(f"ppring constant : {k_dyn} N/m\n")

# dynamic Plot
plt.figure()
plt.errorbar(
    m_dynamic,
    T2,
    yerr=sT2,
    fmt="s",
    capsize=4,
    color="black",
    ecolor="red",
)
plt.plot(m_dynamic, slope_dyn * m_dynamic + c_dyn, color="green")
plt.xlabel("mass $m$ (kg)")
plt.ylabel("(period)$^2$ $T^2$ ($s^2$)")
plt.title("dynamic method: period$^2$ vs mass")
plt.legend()
plt.tight_layout()
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 2/phys1201/week 1/dynamic_method_fit.png", dpi=300)
plt.show()


# sigma test
t_score = abs(k_stat.n - k_dyn.n) / np.sqrt(k_stat.s**2 + k_dyn.s**2)

print("sigma test")
print(f"k (static)  = {k_stat} N/m")
print(f"k (dynamic) = {k_dyn} N/m")
print(f"t-score = {t_score:.4f}")