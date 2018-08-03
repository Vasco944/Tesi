
import matplotlib.pyplot as plt
import numpy as np
import sys
#sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot
nest.Install('albertomodule')#RICORDA CHE PER LA PARTE NEGATIVA DEVI CONSIDERARE CHE ABBIAMO (t_spike + dendritic delay) - t_spike quindi alle differenze tra gli spike time che vedi bisogna sottrarre ancora 1 per la parte negativa
# per la parte positiva le differenze tra gli spike time non necessitano un'ulteriore sottrazione
	
#RICORDA CHE PER LA PARTE NEGATIVA DEVI CONSIDERARE CHE ABBIAMO (t_spike + dendritic delay) - t_spike quindi alle differenze tra gli spike time che vedi bisogna sottrarre ancora 1 per la parte negativa
# per la parte positiva le differenze tra gli spike time non necessitano un'ulteriore sottrazione

nest.ResetKernel()
nest.set_verbosity('M_WARNING')
delay = 1.0
num_parr = 400 #se si vuole iSTDP con grafico piu' ampio va aumentato, tenere sempre valori multipli di 4

initweight = 1.0

STDP = 1 #PER iSTDP SCEGLIERE 1 PER Sgritta2017 SCEGLIERE 0 


A = 58.92
B = 0.0135241
C = 0.0244572

C_istdp = 5.0451
r_LTD_LTP = 0.552
tau_plus = 125.0

parrot = nest.Create("parrot_neuron", num_parr)


senders_e= parrot[:num_parr/4]
receivers_e = parrot[num_parr/4:num_parr/2]
senders_i = parrot[num_parr/2: 3*num_parr/4]
receivers_i = parrot[3*num_parr/4:]
if STDP == 1:
	nest.CopyModel('istdp_synapse', 'stdp',{'lambda': C_istdp, 'mu_plus': r_LTD_LTP, 'Wmax':10.0, 'tau_plus': tau_plus})
if STDP == 0:
	nest.CopyModel('sgritta_synapse', 'stdp', {'alpha': A , 'lambda': B, 'tau_plus': C })
spikes_in = nest.Create('spike_detector', 1)
spikes_out = nest.Create('spike_detector', 1)

stimuli = nest.Create("spike_generator", 3)
stimulus_e = stimuli[0]
nest.SetStatus([stimulus_e], {'spike_times': [5.0, 10003.0]})

''' LTP '''


for i,senders_ei in enumerate(senders_e):
	nest.Connect([stimulus_e], [senders_ei], {'rule': 'all_to_all'}, {'delay' : delay})
	
for i,receivers_ei in enumerate(receivers_e):
	nest.Connect([senders_e[i]], [receivers_ei], {'rule': 'all_to_all'}, {'model':'stdp', 'weight': initweight, 'delay' : delay})
	delay = delay + 1

nest.Connect(senders_e, spikes_in)
nest.Connect(receivers_e, spikes_out)


''' LTD '''
delay = 1.0
stimulus_i = stimuli[1]
stimulus_i_out = stimuli[2]
nest.SetStatus([stimulus_i], {'spike_times': [7.0]})
nest.SetStatus([stimulus_i_out], {'spike_times': [5.0]})

nest.Connect([stimulus_i_out], receivers_i, {'rule': 'all_to_all'}, {'model': 'static_synapse'})

for i,senders_ii in enumerate(senders_i):
	nest.Connect([stimulus_i], [senders_ii], {'rule': 'all_to_all'}, {'model': 'static_synapse', 'delay': delay})
	delay = delay + 1

for i, receivers_ii in enumerate(receivers_i):
	nest.Connect([senders_i[i]], [receivers_ii], {'rule': 'all_to_all'}, {'model': 'stdp', 'weight': initweight, 'delay': 1.0})
		
	

nest.Simulate(10006)




Exc = nest.GetConnections(senders_e, receivers_e)
weights = nest.GetStatus(Exc, "weight")

print(weights[0] +weights[9] + weights[14] + weights[24] - 4) #ricorda che in weights se vuoi il peso all'istante A devi printare weights[A - 1] il - 4 serve a togliere il peso iniziale dei 4 elementi
weights_e = np.zeros(num_parr/4 + 1)
for i in range(0, num_parr/4):
	a = weights[i] - initweight
	weights_e[i+1] = a

if STDP == 1:
	weights_e[0] = weights_e[1] #per iSTDP

if STDP == 0:
	weights_e[0] = 0 #per Sgritta2017
	
Inh = nest.GetConnections(senders_i, receivers_i)
weights = nest.GetStatus(Inh, "weight")

print(weights[23] + weights[18] + weights[13] - 3 ) #ricorda che in weights se vuoi il peso all'istante A devi printare weights[A - 1] il - 3 serve a togliere il peso iniziale dei 3 elementi
weights_i = np.zeros(num_parr/4)

for i in range(0, num_parr/4):
	a = weights[i] - initweight
	weights_i[num_parr/4 -1 - i] = a

dt = range(-num_parr/4, num_parr/4 + 1)

W = np.concatenate(( weights_i,weights_e))
plt.plot(dt, W)
plt.show()




























