import sympy as sp

x, y = sp.symbols('x y')

g = (x**2) * y

delg_dx = sp.diff(g, x)
print("delg/dx =", delg_dx)

delg_dy = sp.diff(g, y)
print("delg/dy =", delg_dy)

# computing total
x, y = sp.symbols('x y')
g = (x**2) * y

g_total = g.subs(y, x**2)

dg_dx_total = sp.diff(g_total, x)

print("dg/dx =", dg_dx_total)


#3 variables
x, y, z = sp.symbols('x y z')
g = (x**2) * y * (z**3)

delg_dx = sp.diff(g, z)
print("delg/dx =", delg_dx)

delg_dy = sp.diff(g, y)
print("delg/dy =", delg_dy)

delg_dz = sp.diff(g, z)
print("delg/dx =", delg_dz)
