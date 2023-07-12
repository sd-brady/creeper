import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy.stats import linregress
from time import perf_counter

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

xdata = np.linspace(0, 4, 50)
y = func(xdata, 2.5, 1.3, 0.5)
rng = np.random.default_rng()

y_noise = 0.1 * rng.normal(size=xdata.size)
ydata = y + y_noise
plt.plot(xdata, ydata, 'b-', label='data')

t1_start = perf_counter()

popt, pcov = curve_fit(func, xdata, ydata)

t1_end = perf_counter()
print("Elapsed time during the whole program in seconds:",
                                        t1_end-t1_start)
r_value  = linregress(y, func(xdata, *popt))[2]
print(f"true: {r_value**2}")

r_value  = linregress(ydata, func(xdata, *popt))[2]
print(f"noise: {r_value**2}")

plt.plot(xdata, func(xdata, *popt), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

popt, pcov = curve_fit(func, xdata, ydata, p0=[2.5,1.3,0.5],bounds=((0,0,0),(3,3,3)))

r_value  = linregress(y, func(xdata, *popt))[2]
print(f"true: {r_value**2}")

r_value  = linregress(ydata, func(xdata, *popt))[2]
print(f"noise: {r_value**2}")

plt.plot(xdata, func(xdata, *popt), 'g--',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
