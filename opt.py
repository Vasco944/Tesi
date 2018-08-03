import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit


def  fun(X, a, b, c):
    x1 = [i * np.pi*b for i in X]
    x2 = [i * c for i in X]
    return a*np.sin(x1)*np.exp(-1 * np.abs(x2))

def  fun2(x, a, b, c):
    x1 = [i * b for i in X]
    x2 = [i * c for i in X]
    #print(np.abs(x2))
    return a*np.sin(x1)*np.exp(-1 * np.abs(x2))


Y_1= np.array([-10.0, 0, 5.0, -50.0, -22.0, 22.0, 50.0, 0, 0, -10]) #il valore 0 corrispondente a -75 e +75 e' stato aggiunto per evitare un ripple troppo grande anche se non era presente sul grafico dell'articolo pero' sembra essere comunque un valore consono a quanto e' riportato nel medesimo articolo amche in vitru' delle grandi deviazioni standard delle nostre misure
X = np.array([-99.0, -75.0, -53.0, -25.0, -9.0, 9.0, 25.0, 53.0,75.0, 99.0])

y_noise = 5.2 * np.random.normal(size=X.size)
Y = Y_1 + y_noise
x1 = np.array([0.01, 0.01, 0.01])

popt, popv = curve_fit(fun, X, Y, x1)

diff = 10
thr = 0.01
x_old = x1
dt = range(-100, 100)

plt.plot(dt, fun(dt, *popt))
plt.scatter(X, Y_1)
plt.show()
print(popt)
#[  5.40311822e+02   1.08471127e-01   8.58994150e-02]
#[  1.14326848e+03   1.08898527e-01  -1.14653895e-01]
#[  1.06380073e+02   1.58126312e-02   3.51887749e-02]
#[  1.00742688e+02   1.60585489e-02   3.16269745e-02]

#[  1.06555590e+02   1.35240906e-02   2.76061848e-02]
#[  9.71078074e+01   1.39907151e-02   2.47041006e-02]
#[  7.98930184e+01   1.74948618e-02  -2.17183886e-02]
#[  5.89235138e+01   1.97636875e-02   1.11696510e-02]








