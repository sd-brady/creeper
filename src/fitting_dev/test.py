import numpy as np
from scipy.optimize import curve_fit

from matplotlib import pyplot as plt

x = np.linspace(0, 10, num=40)

# The coefficients are much bigger.
y = 10.45 * np.sin(5.334 * x) + np.random.normal(size=40)


def test(x, a, b):
    return a * np.sin(b * x)


param, param_cov = curve_fit(test, x, y)

print("Sine function coefficients:")
print(param)
print("Covariance of coefficients:")
print(param_cov)

ans = param[0] * (np.sin(param[1] * x))

plt.plot(x, y, "o", color="red", label="data")
plt.plot(x, ans, "--", color="blue", label="optimized data")
plt.legend()
plt.show()
