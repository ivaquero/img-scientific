import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb

_, axes = plt.subplots(3, 1, constrained_layout=True)

# The tau curve
x = np.linspace(-20, 20, 1000)
y = np.log((1 / 9) ** x + (8 / 9) ** x) / np.log(3)

axes[0].plot(x, y)
axes[0].set(xlabel="$q$", ylabel=r"$τ(q)$")

# The D_q curve
x1 = np.linspace(-20, 0.99, 100)
x2 = np.linspace(0.99, 20, 100)
Dq1 = np.log((1 / 9) ** x1 + (8 / 9) ** x1) / (np.log(3) * (1 - x1))
Dq2 = np.log((1 / 9) ** x2 + (8 / 9) ** x2) / (np.log(3) * (1 - x2))

axes[1].plot(x1, Dq1, x2, Dq2)
axes[1].set(xlabel="q", ylabel="$D_q$")

# The f(α) curve
p1, p2 = 1 / 9, 8 / 9
k = 500
s = np.arange(500)
x = (s * np.log(p1) + (k - s) * np.log(p2)) / (k * np.log(1 / 3))
f = -(np.log(comb(k, s))) / (k * np.log(1 / 3))

axes[2].plot(x, f)
axes[2].set(xlabel=r"$α$", ylabel=r"$f(α)$")

plt.show()
