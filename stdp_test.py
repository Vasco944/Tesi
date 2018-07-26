import matplotlib.pyplot as plt
import numpy as np
import estdp_fun

deltaTime = range(-100, 100)
print(len(deltaTime))
#alpha, step, mu_plus, mu_minus, initweight, maxweight, tau_m, tau_p

'''

multiplicative    mu_plus = mu_minus = 1.0  
additive STDP	  mu_plus = mu_minus = 0.0  
Guetig STDP	  mu_plus = mu_minus = [0.0,1.0]  
van Rossum STDP	  mu_plus = 0.0 mu_minus = 1.0 

'''


''' ADDITIVE '''

mu_minus = 1.0 
mu_plus = 1.0 
	
x = 0.1
fig = plt.figure(1)
fig.suptitle('DeltaWeight (Additive)')

fig2 = plt.figure(2)
fig2.suptitle('DeltaWeight in Percentage Of Initial Weight (Additive)')

for i in range(0, 3):
	pesi = estdp_fun.eSTDP(x, 1.0, mu_plus, mu_minus, 1.0, 20, 20.0, 20.0)
	W = pesi[0:200]
	print(len(W))
	W_perc = pesi[200:]
	ax = fig.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W)
	ax.set_title('alpha = ' + str(x))
	ax = fig2.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W_perc)
	ax.set_title('alpha = ' + str(x))
	x = x * 10



x = 0.1

for i in range(3, 6):
	pesi = estdp_fun.eSTDP(1.0, x, mu_plus, mu_minus, 1.0, 20, 20.0, 20.0)
	W = pesi[0:200]
	print(len(W))
	W_perc = pesi[200:]
	ax = fig.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W)
	ax.set_title('lambda = ' + str(x))
	ax = fig2.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W_perc)
	ax.set_title('lambda = ' + str(x))
	x = x * 10

''' MULTIPLICATIVE '''

mu_minus = 1.0 
mu_plus = 1.0 
	
x = 0.1
fig3 = plt.figure(3)
fig3.suptitle('DeltaWeight (Multiplicative)')

fig4 = plt.figure(4)
fig4.suptitle('DeltaWeight in Percentage Of Initial Weight (Multiplicative)')

for i in range(0, 3):
	pesi = estdp_fun.eSTDP(x, 1.0, mu_plus, mu_minus, 5, 20, 20.0, 20.0)
	W = pesi[0:200]
	print(len(W))
	W_perc = pesi[200:]
	ax = fig3.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W)
	ax.set_title('alpha = ' + str(x))
	ax = fig4.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W_perc)
	ax.set_title('alpha = ' + str(x))
	x = x * 10



x = 0.1

for i in range(3, 6):
	pesi = estdp_fun.eSTDP(1.0, x, mu_plus, mu_minus, 5, 20, 20.0, 20.0)
	W = pesi[0:200]
	print(len(W))
	W_perc = pesi[200:]
	ax = fig3.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W)
	ax.set_title('lambda = ' + str(x))
	ax = fig4.add_subplot(2, 3, i + 1)
	ax.plot(deltaTime, W_perc)
	ax.set_title('lambda = ' + str(x))
	x = x * 10



plt.show()
