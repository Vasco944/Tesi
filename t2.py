
import os
import matplotlib.pyplot as plt
import numpy as np
import sys
#sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot
nest.Install("albertomodule")


nest.ResetKernel()
nest.set_verbosity('M_WARNING')
maxweight = 20.0
delay = 1.0
num_parr = 400

''' TEST ANDAMENTO PESI PARTE SINISTRA DEL GRAFICO '''

parrot = nest.Create("parrot_neuron", num_parr)



senders_i = parrot[:num_parr/4]
receivers_i = parrot[num_parr/4:num_parr/2]


nest.CopyModel('istdp_synapse', 'stdp',{'Wmax': 20.0, 'tau_plus': 125.0})

stimuli = nest.Create("spike_generator", 3)
stimulus_i = stimuli[1]
stimulus_i_out = stimuli[2]
nest.SetStatus([stimulus_i], {'spike_times': [7.0, 10005.0]})
nest.SetStatus([stimulus_i_out], {'spike_times': [6.0]})

nest.Connect([stimulus_i_out], receivers_i, {'rule': 'all_to_all'}, {'model': 'static_synapse'})

for i,senders_ii in enumerate(senders_i):
	nest.Connect([stimulus_i], [senders_ii], {'rule': 'all_to_all'}, {'model': 'static_synapse', 'delay': delay})
	delay = delay + 1

for i, receivers_ii in enumerate(receivers_i):
	nest.Connect([senders_i[i]], [receivers_ii], {'rule': 'all_to_all'}, {'model': 'stdp', 'weight': 5.0, 'delay': delay})

nest.Simulate(10106)

Inh = nest.GetConnections(senders_i, receivers_i)
weights = nest.GetStatus(Inh, "weight")

weights_i = np.zeros(100)

for i in range(0, 100):
	a = weights[i] - 5.0

	weights_i[99 - i] = a
	
	
plt.plot(weights_i)
plt.show()


	

