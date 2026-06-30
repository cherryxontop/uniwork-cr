from uncertainties import ufloat
from uncertainties.umath import *
import math
import numpy as np


r1 = ufloat(5.56, 5.56*0.012)
r2 = ufloat(3.23, 3.23*0.012)
rt = r1+r2
print(rt)

Tmeas = ufloat(5.56, 5.56*0.012)
Ttheory = ufloat(3.23, 3.23*0.012)
sigma = (Tmeas.n-Ttheory.n)/(Tmeas+Ttheory).s
print(sigma)

#calculating fc
R = ufloat(4260, 4260*0.012)
C = ufloat(0.1e-6, 0.1e-6*0.01)
fctheory = 1/(2* np.pi* R * C)
print(fctheory)

fc_calc = 1/(2*np.pi*R*C)
fc_meas = ufloat(320, 50)

print(f"fc calc = {fc_calc}")
print(f"fc meas = {fc_meas}")

sigma = (fc_calc.n - fc_meas.n) / np.sqrt(fc_calc.s**2 + fc_meas.s**2)
print(f"sigma = {sigma:.4f}")

if abs(sigma) < 3:
    print("sigma < 3, values corroborate each other")
else:
    print("sigma >= 3, values don't agree")