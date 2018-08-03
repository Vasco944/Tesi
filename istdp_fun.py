	


def iSTDP (alpha, step, mu_plus, initweight, maxweight, tau_p, c):
	import os
	import matplotlib.pyplot as plt
	import numpy as np
	import sys
	#sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
	import nest
	import nest.raster_plot
	if c == 0: #questo if permette di installare il modulo solo al primo clid di 'plot' cosi' le volte successive non mi crea problemi
		nest.Install("albertomodule")


	nest.ResetKernel()
        nest.SetKernelStatus({'overwrite_files' : True})
	nest.set_verbosity('M_WARNING')
	delay = 1.0
	num_parr = 2 * alpha



	parrot = nest.Create("parrot_neuron", num_parr)
	
	#nest.SetStatus(parrot, {'tau_minus': float(tau_m)})
	senders_e= parrot[:num_parr/4]
	receivers_e = parrot[num_parr/4:num_parr/2]
	senders_i = parrot[num_parr/2: 3*num_parr/4]
	receivers_i = parrot[3*num_parr/4:]


	nest.CopyModel('istdp_synapse', 'stdp',{'lambda': step, 'mu_plus': mu_plus, 'Wmax': maxweight, 'tau_plus': float(tau_p)})

	spikes_in = nest.Create('spike_detector', 1, {'to_file': True})
	spikes_out = nest.Create('spike_detector', 1)

	stimuli = nest.Create("spike_generator", 3)
	stimulus_e = stimuli[0]
	nest.SetStatus([stimulus_e], {'spike_times': [5.0, 10003.0]})

	''' PARTE DESTRA '''



	for i,senders_ei in enumerate(senders_e):
		nest.Connect([stimulus_e], [senders_ei], {'rule': 'all_to_all'}, {'delay' : delay})
		
	for i,receivers_ei in enumerate(receivers_e):
		nest.Connect([senders_e[i]], [receivers_ei], {'rule': 'all_to_all'}, {'model':'stdp', 'weight': initweight, 'delay' : delay})
		delay = delay + 1

	nest.Connect(parrot, spikes_in)
	



	''' PARTE SINSTRA '''
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
		
	

	nest.Simulate(10506)


	Exc = nest.GetConnections(senders_e, receivers_e)
	weights = nest.GetStatus(Exc, "weight")
	#print(weights)

	weights_e = np.zeros(alpha/2 + 1)
	weights_e_perc = np.zeros(alpha/2)

	for i in range(0, alpha/2):
		a = weights[i] - initweight
		weights_e[i+1] = a
		weights_e_perc[i] = (a/initweight) * 100
	weights_e[0] = weights_e[1]

	b = weights_e[0]	

	Inh = nest.GetConnections(senders_i, receivers_i)
	weights = nest.GetStatus(Inh, "weight")
	

	weights_i = np.zeros(alpha/2)
	weights_i_perc = np.zeros(alpha/2)
	for i in range(0, alpha/2):
		a = weights[i] - initweight
	
		weights_i[(alpha/2 - 1) - i] = a
		weights_i_perc[(alpha/2 - 1)  - i] = (a/initweight) * 100
	
	a = weights_i[(alpha/2 - 1)]
	d = b - a
	print('dx:' + str(b))
	print('sx:' + str(a))
	print('difference dx - sx:' + str(d))
	print()
	W = np.concatenate(( weights_i,weights_e))
	W_perc = np.concatenate((weights_i_perc, weights_e_perc))
	pesi = np.concatenate((W, W_perc))
	
	
	
	return(pesi)



