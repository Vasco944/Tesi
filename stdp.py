import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot

nest.ResetKernel()

alpha = 1.0
step = 1.0
mu_plus = 1.0
mu_minus = 1.0
initweight = 5.0
maxweight = 20.0
delay = 1.0
num_parr = 400



parrot = nest.Create("parrot_neuron", num_parr)

senders_e= parrot[:num_parr/4]
receivers_e = parrot[num_parr/4:num_parr/2]
senders_i = parrot[num_parr/2: 3*num_parr/4]
receivers_i = parrot[3*num_parr/4:]


nest.CopyModel('stdp_synapse_hom', 'stdp',{'alpha': alpha, 'lambda': step, 'mu_plus': mu_plus,'mu_minus': mu_minus, 'Wmax': maxweight})

spikes_in = nest.Create('spike_detector', 1)
spikes_out = nest.Create('spike_detector', 1)

stimuli = nest.Create("spike_generator", 3)
stimulus_e = stimuli[0]
nest.SetStatus([stimulus_e], {'spike_times': [5.0, 10003.0]})

''' LTP '''



for i,senders_ei in enumerate(senders_e):
	nest.Connect([stimulus_e], [senders_ei], {'rule': 'all_to_all'}, {'delay' : delay})
	delay = delay + 1

for i,receivers_ei in enumerate(receivers_e):
	nest.Connect([senders_e[i]], [receivers_ei], {'rule': 'all_to_all'}, {'model':'stdp', 'weight': initweight, 'delay' : 1})
	delay = delay + 1

nest.Connect(senders_e, spikes_in)
nest.Connect(receivers_e, spikes_out)



''' LTD '''
delay = 1.0
stimulus_i = stimuli[1]
stimulus_i_out = stimuli[2]
nest.SetStatus([stimulus_i], {'spike_times': [7.0, 10005.0]})
nest.SetStatus([stimulus_i_out], {'spike_times': [5.0]})

nest.Connect([stimulus_i_out], receivers_i, {'rule': 'all_to_all'}, {'model': 'static_synapse'})

for i,senders_ii in enumerate(senders_i):
	nest.Connect([stimulus_i], [senders_ii], {'rule': 'all_to_all'}, {'model': 'static_synapse', 'delay': delay})
	delay = delay + 1
for i, receivers_ii in enumerate(receivers_i):
	nest.Connect([senders_i[i]], [receivers_ii], {'rule': 'all_to_all'}, {'model': 'stdp', 'weight': initweight, 'delay': 1.0})


nest.Simulate(10006)

deltaTime = range(-100, 100)

#nest.raster_plot.from_device(spikes_in, hist=False)

#nest.raster_plot.from_device(spikes_out, hist=False)

#plt.figure()

Exc = nest.GetConnections(senders_e, receivers_e)
weights = nest.GetStatus(Exc, "weight")
#print(weights)

weights_e = np.zeros(100)
weights_e_perc = np.zeros(100)

for i in range(0, 100):
	a = weights[i] - initweight
	weights_e[i] = a
	weights_e_perc[i] = (a/initweight) * 100

#plt.plot(weights_e)

Inh = nest.GetConnections(senders_i, receivers_i)
weights = nest.GetStatus(Inh, "weight")
#print(weights)

weights_i = np.zeros(100)
weights_i_perc = np.zeros(100)
for i in range(0, 100):
	a = weights[i] - initweight
	
	weights_i[99 - i] = a
	weights_i_perc[99 -i] = (a/initweight) * 100

#plt.figure()
#plt.plot(weights_i)
W = np.concatenate(( weights_i,weights_e))
W_perc = np.concatenate((weights_i_perc, weights_e_perc))
#print(weights_i)
#plt.figure()
plt.title('DeltaWeight')
plt.plot(deltaTime, W)

plt.figure()
plt.title('DeltaWeight Percentage')
plt.plot(deltaTime, W_perc)

plt.show()




