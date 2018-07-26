import os
import matplotlib.pyplot as plt
import numpy as np
import sys
#sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot

''' TEST ANDAMENTO PESI PARTE DESTRA DEL GRAFICO '''

nest.ResetKernel()
nest.set_verbosity('M_WARNING')
maxweight = 20.0
delay = 1.0
num_parr = 800


parrot = nest.Create("parrot_neuron", num_parr)

nest.SetStatus(parrot, {'tau_minus': float(195.6)})
senders_e= parrot[:num_parr/2]
receivers_e = parrot[num_parr/2:num_parr]
senders_i = parrot[num_parr/2: 3*num_parr/4]
receivers_i = parrot[3*num_parr/4:]

nest.CopyModel('stdp_synapse', 'stdp',{'Wmax': 20.0, 'tau_plus': 125.0})

spikes_in = nest.Create('spike_detector', 1)
spikes_out = nest.Create('spike_detector', 1)

stimuli = nest.Create("spike_generator", 3)
stimulus_e = stimuli[0]
nest.SetStatus([stimulus_e], {'spike_times': [5.0, 10003.0]})

''' LTP '''


for i,senders_ei in enumerate(senders_e):
	nest.Connect([stimulus_e], [senders_ei], {'rule': 'all_to_all'}, {'delay' : delay})
	
for i,receivers_ei in enumerate(receivers_e):
	nest.Connect([senders_e[i]], [receivers_ei], {'rule': 'all_to_all'}, {'model':'stdp', 'weight': 5.0, 'delay' : delay})
	delay = delay + 1

nest.Connect(senders_e, spikes_in)
nest.Connect(receivers_e, spikes_out)

nest.Simulate(10506)

Exc = nest.GetConnections(senders_e, receivers_e)
weights = nest.GetStatus(Exc, "weight")
#print(weights)
weights_e = np.zeros(400)
weights_e_perc = np.zeros(100)

for i in range(0, 400):
	a = weights[i] - 5.0
	weights_e[i] = a


plt.plot(weights_e)
plt.axvline(0, color='white')
plt.show()




