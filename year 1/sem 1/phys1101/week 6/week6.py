#data analysis in python lab

from uncertainties import ufloat
from uncertainties.umath import *


#part 2: calculating uncertainties

x = ufloat(10.34,0.04)
y = ufloat(7.66,0.03)
G = 6.67e-11
print((x**2 + y**2)**0.5)
print((4*x)/np.exp(y))
print((G*x)/y)


#part 3: supernova data

import pandas
import matplotlib.pyplot as plt
import numpy as np

data = pandas.read_excel("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 6/RawSupernovaData.xlsx")
data.head()
print(data.head())

# plot the data read in above, and save the plot.
# can change the formatting of the data points.
plt.errorbar(data.Distance, data.Redshift, xerr=data.Uncertainty, fmt="r.") # code to plot data with error bars
plt.xlabel("Distance (Mpc)") #can change the name of the columns you want to plot as needed
plt.ylabel("Redshift (z)")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 6/errplot.png", dpi=300)


#part4: standard deviations

data1 = pandas.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 6/DataC.csv")
data1.head()
print(data1.head())

data2 = pandas.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 6/DataD.csv")
data2.head()
print(data2.head())

# code to compute the mean, median and standard deviation of data1
print("Number of data points = ", len(data1.Strength))
print("Mean = ",np.mean(data1.Strength))
print("Median = ",np.median(data1.Strength))
print("Standard Deviation = ",np.std(data1.Strength))

# code to compute the mean, median and standard deviation of data2
print("Number of data points = ", len(data2.Strength))
print("Mean = ",np.mean(data2.Strength))
print("Median = ",np.median(data2.Strength))
print("Standard Deviation = ",np.std(data2.Strength))

n_C = len(data1.Strength)
n_D = len(data2.Strength)

# code to compute the mean, uncertainty in mean, and difference in mean for data 1 & data2
mean_C = ufloat(np.mean(data1.Strength), np.std(data1.Strength) / n_C**0.5)
mean_D = ufloat(np.mean(data2.Strength), np.std(data2.Strength) / n_D**0.5)
diff = mean_C - mean_D

print("Alloy C mean strength =", mean_C)
print("Alloy D mean strength =", mean_D)
print("Difference (C - D) =", diff)

#conclusion : the difference in mean strengths shows Alloy D is slightly stronger than Alloy C, not weaker. it is observed that the new energy-efficient processs produced a marginally stronger alloy.


#part 5: line fitting
import statsmodels.api as sm

data3 = pandas.read_csv("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 6/linedata.csv")
data3.head()
print(data3.head())

x = data3['x']
y = data3['y']
err_y = data3['yerr']

plt.errorbar(x,y,yerr=err_y, fmt="ko")
plt.show()

x1 = sm.add_constant(x) # tells the package that you want an intercept, not a line through zero.
w = 1.0/(err_y**2) # calculates how much weight to give each point. larger errors mean lower weights
model = sm.WLS(y,x1,weights=w) # generates model
result = model.fit() # generates fit
result.summary() #prints out lots of statitics of the fit

plt.errorbar(x,y, yerr=err_y, fmt="ko") #plots the data points with error bars
bm = result.params[0]  #extracts the intercept (bm) and gradient (am) from the fit results
am = result.params[1]
model = am*x+bm        #calculates the y-values of the best fit line using y=ax+b at each x value
plt.plot(x,model,"-r") #plots the best fit line in red (r), as a solid line
plt.xlabel("x") 
plt.ylabel("y")
plt.savefig("/Users/chhaya/Documents/uniwork-cr/year 1/sem 1/phys1101/week 6/part5plot.png", dpi=300)
plt.show()

#from result.summary(), gradient = 1.99 +/- 0.02, intercept = 0.01 +/- 0.02.