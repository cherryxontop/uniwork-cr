import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from uncertainties import ufloat

g = 9.796 #m/s^2


#tennis ball run 1

n = np.array([1, 2, 3, 4, 5, 6])
T = np.array([0.440, 0.310, 0.260, 0.190, 0.150, 0.120])
sT = np.array([0.005, 0.005, 0.005, 0.005, 0.005, 0.005])
lnT = np.log(T)
slnT = sT / T

#line fitting
result = sm.WLS(lnT, sm.add_constant(n), weights=1/slnT**2).fit()
c_t1, m, sc_t1, sm_ = result.params[0], result.params[1], result.bse[0], result.bse[1]
eps_t1 = np.exp(m);  se_t1 = eps_t1 * sm_
v0 = np.exp(c_t1)*g/2;  sv = v0 * sc_t1
print(f"tennis run 1: epsilon = {eps_t1:.4f} +/- {se_t1:.4f},  v0 = {v0:.4f} +/- {sv:.4f} m/s")

#plotting
plt.figure()
plt.errorbar(n, lnT, yerr=slnT, fmt="o", capsize=4, color = "black", ecolor = "red", ls="none")
plt.plot(n, m*n + c_t1, color = "blue")
plt.xlabel("n(number of bounces)")
plt.ylabel("ln(T_n) (s)")
plt.title("tennis ball – run 1")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 11/tennis1.png", dpi=300)
plt.show()


#tennis ball run 2

n = np.array([1, 2, 3, 4, 5, 6])
T = np.array([0.420, 0.320, 0.240, 0.190, 0.140, 0.120])
sT = np.array([0.005, 0.005, 0.005, 0.005, 0.005, 0.005])
lnT = np.log(T)
slnT = sT / T

#line fitting
result = sm.WLS(lnT, sm.add_constant(n), weights=1/slnT**2).fit()
c_t2, m, sc_t2, sm_ = result.params[0], result.params[1], result.bse[0], result.bse[1]
eps_t2 = np.exp(m);  se_t2 = eps_t2 * sm_
v0 = np.exp(c_t2)*g/2;  sv = v0 * sc_t2
print(f"tennis run 2: epsilon = {eps_t2:.4f} +/- {se_t2:.4f},  v0 = {v0:.4f} +/- {sv:.4f} m/s")

#plotting
plt.figure()
plt.errorbar(n, lnT, yerr=slnT, fmt="o", capsize=5, color = "black", ecolor = "red", ls="none")
plt.plot(n, m*n + c_t2, color = "blue")
plt.xlabel("n(number of bounces)")
plt.ylabel("ln(T_n) (s)")
plt.title("tennis ball – run 2")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 11/tennis2.png", dpi=300)
plt.show()


#table tennis ball run 1

n = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
T = np.array([0.500, 0.460, 0.440, 0.420, 0.370, 0.350, 0.340, 0.300, 0.280, 0.280, 0.260, 0.230])
sT = np.array([0.005]*12)
lnT = np.log(T)
slnT = sT / T

#line fitting
result = sm.WLS(lnT, sm.add_constant(n), weights=1/slnT**2).fit()
c_tt1, m, sc_tt1, sm_ = result.params[0], result.params[1], result.bse[0], result.bse[1]
eps_tt1 = np.exp(m);  se_tt1 = eps_tt1 * sm_
v0 = np.exp(c_tt1)*g/2;  sv = v0 * sc_tt1
print(f"table tennis run 1: epsilon = {eps_tt1:.4f} +/- {se_tt1:.4f},  v0 = {v0:.4f} +/- {sv:.4f} m/s")

#plotting
plt.figure()
plt.errorbar(n, lnT, yerr=slnT, fmt="o", capsize=5, color = "black", ecolor = "red", ls="none")
plt.plot(n, m*n + c_tt1, color = "blue")
plt.xlabel("n(number of bounces)")
plt.ylabel("ln(T_n) (s)")
plt.title("table tennis ball – run 1")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 11/tt1.png", dpi=300)
plt.show()

#plotting residuals
bm = c_tt1
am = m
model = am*n + bm
plt.figure()
plt.plot(n, lnT - model, "ko")
plt.axhline(0, color="r", ls="--")
plt.xlabel("n(number of bounces)")
plt.ylabel("residual")
plt.title("residuals – table tennis ball – run 1")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 11/residuals_tt1.png", dpi=300)
plt.show()

#table tennis ball run 2

n = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
T = np.array([0.5, 0.480, 0.460, 0.410, 0.380, 0.350, 0.330, 0.320, 0.280, 0.260, 0.240, 0.230])
sT = np.array([0.005]*12)
lnT = np.log(T)
slnT = sT / T

#line fitting
result = sm.WLS(lnT, sm.add_constant(n), weights=1/slnT**2).fit()
c_tt2, m, sc_tt2, sm_ = result.params[0], result.params[1], result.bse[0], result.bse[1]
eps_tt2 = np.exp(m);  se_tt2 = eps_tt2 * sm_
v0 = np.exp(c_tt2)*g/2;  sv = v0 * sc_tt2
print(f"table tennis run 2: epsilon = {eps_tt2:.4f} +/- {se_tt2:.4f},  v0 = {v0:.4f} +/- {sv:.4f} m/s")

#plotting
plt.figure()
plt.errorbar(n, lnT, yerr=slnT, fmt="o", capsize=5, color = "black", ecolor = "red", ls="none")
plt.plot(n, m*n + c_tt2, color = "blue")
plt.xlabel("n(number of bounces)")
plt.ylabel("ln(T_n) (s)")
plt.title("table tennis ball – run 2")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 11/tt2.png", dpi=300)
plt.show()

#sigma tests for comparing epsilon values
eps_t1 = ufloat(0.7663, 0.0101)
eps_t2 = ufloat(0.7679, 0.0053)
eps_tt1 = ufloat(0.9341, 0.0021)
eps_tt2 = ufloat(0.9291, 0.0020)

t_tennis = (eps_t1.n - eps_t2.n)  / (eps_t1.s**2 + eps_t2.s**2)**0.5
t_tt = (eps_tt1.n - eps_tt2.n) / (eps_tt1.s**2 + eps_tt2.s**2)**0.5
t_cross = (eps_t1.n - eps_tt1.n) / (eps_t1.s**2 + eps_tt1.s**2)**0.5

print("t_tennis = ", t_tennis)
print("t_tt = ", t_tt)
print("t_cross = ", t_cross)

#calculate predicted V_0
v0_pred = np.sqrt(2 * g * 0.4)
print("predicted v0 =" + str(v0_pred) + " m/s")

#calculate experimental V_0
v0_t1 = ufloat(np.exp(c_t1)*g/2,  np.exp(c_t1)*sc_t1*g/2)
v0_t2 = ufloat(np.exp(c_t2)*g/2,  np.exp(c_t2)*sc_t2*g/2)
v0_tt1 = ufloat(np.exp(c_tt1)*g/2, np.exp(c_tt1)*sc_tt1*g/2)
v0_tt2 = ufloat(np.exp(c_tt2)*g/2, np.exp(c_tt2)*sc_tt2*g/2)

print(f"v0 tennis run 1 = {v0_t1}")
print(f"v0 tennis run 2 = {v0_t2}")
print(f"v0 table tennis run 1 = {v0_tt1}")
print(f"v0 table tennis run 2 = {v0_tt2}")

#sigma test for comparing predicted and experimental V_0
t_t1 = abs(v0_t1.n  - v0_pred) / v0_t1.s
t_t2 = abs(v0_t2.n  - v0_pred) / v0_t2.s
t_tt1 = abs(v0_tt1.n - v0_pred) / v0_tt1.s
t_tt2 = abs(v0_tt2.n - v0_pred) / v0_tt2.s

print("t_t1 =", t_t1)
print("t_t2 =", t_t2)
print("t_tt1 =", t_tt1)
print("t_tt2 =", t_tt2)


