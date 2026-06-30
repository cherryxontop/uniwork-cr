import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import statsmodels.api as sm

annetemp = pd.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/csvs/AnneTemp.csv")
print(annetemp.head())
x = annetemp['Minutes'][60:]
y = annetemp['Temperature'][60:]
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (°C)")
plt.errorbar(x,y, fmt="ko")
plt.show()

x1 = sm.add_constant(x)
y = np.log(y)
model = sm.WLS(y,x1)
result = model.fit()
result.summary()

plt.errorbar(x,y, fmt="ko")
bm = result.params[0]
am = result.params[1]
model = am*x+bm
plt.plot(x,model,"-r")
plt.xlabel("minutes")
plt.ylabel("temperature")
plt.show()
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/pngs/annetemp.png", dpi=300)

fredtemp = pd.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/csvs/FredTemp.csv")
x = fredtemp['Minutes'][60:]
y = fredtemp['Temperature'][60:]
plt.errorbar(x,y, fmt="ko")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (°C)")
plt.show()

x2 = sm.add_constant(x)
y = np.log(y)
model = sm.WLS(y,x2)
result = model.fit()
result.summary()

plt.errorbar(x,y, fmt="ko")
bm = result.params[0]
am = result.params[1]
model = am*x+bm
plt.plot(x,model,"-r")
plt.xlabel("minutes")
plt.ylabel("temperature")
plt.show()
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/pngs/fredtemp.png", dpi=300)

irsensor = pd.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/csvs/IRsensor.csv")
plt.errorbar(x,y, fmt = "ko")
plt.show()
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/pngs/irsensor.png", dpi=300)


annecell = pd.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/csvs/Annephone.csv")
x = annecell['Minutes']
y = annecell['T2']
plt.errorbar(x,y, fmt="ko")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (°C)")
plt.show()

x3 = sm.add_constant(x)
y = np.log(y)
model = sm.WLS(y,x3)
result = model.fit()
result.summary()

plt.errorbar(x,y, fmt="ko")
bm = result.params[0]
am = result.params[1]
model = am*x+bm
plt.plot(x,model,"-r")
plt.xlabel("minutes")
plt.ylabel("t2")
plt.show()
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/pngs/annecell.png", dpi=300)

fredcell = pd.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/csvs/Fredphone.csv")
x = fredcell['Minutes']
y = fredcell['T2']
plt.errorbar(x,y, fmt="ko")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (°C)")
plt.show()

x4 = sm.add_constant(x)
y = np.log(y)
model = sm.WLS(y,x4)
result = model.fit()
result.summary()

plt.errorbar(x,y, fmt="ko")
bm = result.params[0]
am = result.params[1]
model = am*x+bm
plt.plot(x,model,"-r")
plt.xlabel("minutes")
plt.ylabel("t2")
plt.show()
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/pngs/fredcell.png", dpi=300)

louisacell = pd.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/csvs/Louisaphone.csv")
louisacell.head()
x = louisacell['Minutes']
y = louisacell['T2']
plt.errorbar(x,y, fmt="ko")
plt.show()

x5 = sm.add_constant(x)
y = np.log(y)
model = sm.WLS(y,x5)
result = model.fit()
result.summary()

plt.errorbar(x,y, fmt="ko")
bm = result.params[0]
am = result.params[1]
model = am*x+bm
plt.plot(x,model,"-r")
plt.xlabel("minutes")
plt.ylabel("t2")
plt.show()
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 7/pngs/louisacell.png", dpi=300)