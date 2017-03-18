import pylab as plt
import numpy as np

Z = np.random.random((50, 50))
Z = np.zeros((50, 50))  # Test data
plt.imshow(Z, cmap='gray')
plt.show()
