
import nest
import matplotlib.pyplot as plt
import numpy as np
nest.Install("albertomodule")

nest.ResetKernel()
nest.SetKernelStatus({'overwrite_files' : True})
nest.set_verbosity('M_WARNING')

#RICORDA CHE PER LA PARTE NEGATIVA DEVI CONSIDERARE CHE ABBIAMO (t_spike + dendritic delay) - t_spike quindi alle differenze tra gli spike time che vedi bisogna sottrarre ancora 1 per la parte negativa
# per la parte positiva le differenze tra gli spike time non necessitano un'ulteriore sottrazione. Inoltre ricorda che qui plotti il peso quindi bisogna sottrarre il peso iniziale per i vari controlli.

parrot = nest.Create("parrot_neuron", 4)

spikes = nest.Create('spike_detector', 1, {'to_file': False})

sender_e = parrot[0:1]
receiver_e = parrot[1:2]

sender_i = parrot[2:3]
receiver_i = parrot[3:]

'''

recdict = {"to_memory": False,
             "to_file":    True,
             "label":     "exc",
             "senders":    sender_e,
             "targets":    receiver_e
               }
w_exc = nest.Create('weight_recorder',params=recdict)

recdict2 = {"to_memory": False,
            "to_file":    True,
            "label":     "inh",
            "senders":    sender_i,
            "targets":    receiver_i
               }
w_inh = nest.Create('weight_recorder',params=recdict2)

'''

A = 58.92
B = 0.0135241
C = 0.0244572

C_istdp = 5.0451
r_LTD_LTP = 0.552
tau_plus = 125.0

STDP = 1 #PER iSTDP SCEGLIERE 1 PER Sgritta2017 SCEGLIERE 0 

if STDP == 1:
	nest.CopyModel('istdp_synapse', 'stdp',{'lambda': C_istdp, 'mu_plus': r_LTD_LTP, 'Wmax':10.0, 'tau_plus': tau_plus})
if STDP == 0:
	nest.CopyModel('sgritta_synapse', 'stdp', {'alpha': A , 'lambda': B, 'tau_plus': C})


#nest.SetDefaults('stdp_i',{ "weight_recorder": w_inh[0]})

nest.Connect(sender_e, receiver_e, {'rule': 'all_to_all'}, {'model':'stdp', 'weight': 1.0, 'delay' : 1.0})
nest.Connect(sender_i, receiver_i, {'rule': 'all_to_all'}, {'model':'stdp', 'weight': 1.0, 'delay' : 1.0})

stimuli = nest.Create("spike_generator", 4)

stimulus_e_in = stimuli[0]
stimulus_e_out = stimuli[1]
stimulus_i_in = stimuli[2]
stimulus_i_out = stimuli[3]

nest.SetStatus([stimulus_e_in], {'spike_times': [5.0, 10003.0]})
nest.SetStatus([stimulus_e_out], {'spike_times': [15.0, 20.0, 30.0]})

nest.SetStatus([stimulus_i_in], {'spike_times': [30.0]})
nest.SetStatus([stimulus_i_out], {'spike_times': [5.0, 10.0, 15.0]})

nest.Connect([stimulus_e_in], sender_e)
nest.Connect([stimulus_e_out], receiver_e)

nest.Connect( [stimulus_i_in], sender_i)
nest.Connect([stimulus_i_out] ,receiver_i)

nest.Connect(parrot, spikes)

nest.Simulate(10506.0)

Exc = nest.GetConnections(sender_e, receiver_e)
weights_e = nest.GetStatus(Exc, "weight")

Inh = nest.GetConnections(sender_i, receiver_i)
weights_i = nest.GetStatus(Inh, "weight")

'''
plt.plot(weights_e)
plt.figure()
plt.plot(weights_i)
plt.show()

'''
print(weights_e) #quando controlli ricorda di sottrarre il peso iniziale. quando fai il paragone con il grafico ricorda che il grafgico mostra il deltaPeso per cui come detto prima alla somma devi togliere il valore di peso iniziale di questo script. stessa cosa vale per i weights_i
print(weights_i)
