import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

dt = range(0, 500)

t_p = 125.0
t_m = 200.6

c1 = np.divide(dt, t_p)
c_1 = [i * 2 for i in c1]

c2 = np.divide(dt, t_m)
c_2 = [i * 2 for i in c2]

k = np.exp(  - 1.0 * ( np.absolute(dt) / t_p)) * (1 + np.cos(c_1))  - 5. * np.exp(  - 1.0 * ( np.absolute(dt) / t_m)) * (1 - np.cos(c_2))

g = k 

plt.plot(dt, k)
plt.show()
