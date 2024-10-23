import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

dx, dy = 0.015, 0.05
# numpy.arange returns evenly spaced values within a given interval
x = np.arange(-4.0, 4.0, dx)  # Corrected -04.0 to -4.0
y = np.arange(-4.0, 4.0, dy)  # Corrected -04.0 to -4.0
# returns coordinate matrices from coordinate vectors
X, Y = np.meshgrid(x, y)

extent = np.min(x), np.max(x), np.min(y), np.max(y)

Z1 = np.add.outer(range(8), range(8)) % 2

plt.imshow(Z1, cmap="binary_r", interpolation="nearest", extent=extent, alpha=1)

plt.title("Chess Board", fontweight="bold")

plt.show()
