import numpy as np
import matplotlib.pyplot as plt

# Forma direta 1
# Wn = Xn + 1.5*Z-1*Xn
# Yn = Wn - 0.1*Z-1*Yn

w=np.zeros(100)
y=np.zeros(100)
x=np.ones(100)
x[0] = 0

for i in range(1,100):
  w[i] = x[i] + 1.5*x[i-1]
  y[i] = w[i] - 0.1*y[i-1]

plt.plot(y[1::])
plt.show()