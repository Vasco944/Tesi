	


def eSTDP (alpha, step, mu_plus, mu_minus, initweight, maxweight, tau_m, tau_p):
	import os
	import matplotlib.pyplot as plt
	import numpy as np
	import sys
	#sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
	import nest
	import nest.raster_plot
	


	nest.ResetKernel()
	nest.set_verbosity('M_WARNING')
	delay = 1.0
	num_parr = 400



	parrot = nest.Create("parrot_neuron", num_parr)
	
	nest.SetStatus(parrot, {'tau_minus': float(tau_m)})
	senders_e= parrot[:num_parr/4]
	receivers_e = parrot[num_parr/4:num_parr/2]
	senders_i = parrot[num_parr/2: 3*num_parr/4]
	receivers_i = parrot[3*num_parr/4:]


	nest.CopyModel('stdp_synapse', 'stdp',{'alpha': alpha, 'lambda': step, 'mu_plus': mu_plus,'mu_minus': mu_minus, 'Wmax': maxweight, 'tau_plus': tau_p})

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
	nest.SetStatus([stimulus_i], {'spike_times': [7.0, 10006.0]})
	nest.SetStatus([stimulus_i_out], {'spike_times': [5.0]})

	nest.Connect([stimulus_i_out], receivers_i, {'rule': 'all_to_all'}, {'model': 'static_synapse'})

	for i,senders_ii in enumerate(senders_i):
		nest.Connect([stimulus_i], [senders_ii], {'rule': 'all_to_all'}, {'model': 'static_synapse', 'delay': delay})
		delay = delay + 1

	for i, receivers_ii in enumerate(receivers_i):
		nest.Connect([senders_i[i]], [receivers_ii], {'rule': 'all_to_all'}, {'model': 'stdp', 'weight': initweight, 'delay': 1.0})
		
	

	nest.Simulate(10006)

	deltaTime = range(-100, 100)


	Exc = nest.GetConnections(senders_e, receivers_e)
	weights = nest.GetStatus(Exc, "weight")
	#print(weights)

	weights_e = np.zeros(100)
	weights_e_perc = np.zeros(100)

	for i in range(0, 100):
		a = weights[i] - initweight
		weights_e[i] = a
		weights_e_perc[i] = (a/initweight) * 100

	
	Inh = nest.GetConnections(senders_i, receivers_i)
	weights = nest.GetStatus(Inh, "weight")
	

	weights_i = np.zeros(100)
	weights_i_perc = np.zeros(100)
	for i in range(0, 100):
		a = weights[i] - initweight
	
		weights_i[99 - i] = a
		weights_i_perc[99 -i] = (a/initweight) * 100

	
	W = np.concatenate(( weights_i,weights_e))
	print(W)
	print()
	print()
	W_perc = np.concatenate((weights_i_perc, weights_e_perc))
	pesi = np.concatenate((W, W_perc))
	

	
	return(pesi)



