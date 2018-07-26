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
initweight = 0.1
maxweight = 20.0
delay = 1.0
num_parr = 300
iaf_num = 100
iaf_w = 10000.0

nest.SetDefaults('iaf_psc_alpha', {'t_ref': 300000.0, 'C_m' : 0.20, 'tau_m' : 10.0})

parrot = nest.Create("parrot_neuron", 100)
iaf_in = nest.Create("parrot_neuron", 100)
senders= parrot

nest.CopyModel('stdp_synapse', 'stdp',{'alpha': alpha, 'lambda': step, 'mu_plus': mu_plus,'mu_minus': mu_minus, 'Wmax': maxweight})

spikes = nest.Create('spike_detector', 1)
nest.Connect(senders[0:2], spikes)
stimuli = nest.Create("spike_generator", 2)

stimulus_i = stimuli[1]
stimulus_e = stimuli[0]
nest.SetStatus([stimulus_e], {'spike_times': [7.0, 10005.0]})
nest.SetStatus([stimulus_i], {'spike_times': [5.0]})

nest.Connect([stimulus_i], iaf_in, {'rule': 'all_to_all'}, {'model': 'static_synapse', 'weight': iaf_w})

for i,sendersi in enumerate(senders):
	nest.Connect([stimulus_e], [sendersi], {'rule': 'all_to_all'}, {'model': 'static_synapse', 'delay': delay})
	delay = delay + 1
for i, iaf_ini in enumerate(iaf_in):
	nest.Connect([senders[i]], [iaf_ini], {'rule': 'all_to_all'}, {'model': 'stdp', 'weight': initweight, 'delay': 1.0})

nest.Simulate(10007)

nest.raster_plot.from_device(spikes, hist=False)
Inh = nest.GetConnections(senders, iaf_in)
weights = nest.GetStatus(Inh, "weight")
print(weights)
plt.show()
