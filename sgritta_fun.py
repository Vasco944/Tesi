	


def Sgritta (alpha, step, initweight, maxweight, tau_p, c):
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
	num_parr = 400



	parrot = nest.Create("parrot_neuron", num_parr)
	
	#nest.SetStatus(parrot, {'tau_minus': float(tau_m)})
	senders_e= parrot[:num_parr/4]
	receivers_e = parrot[num_parr/4:num_parr/2]
	senders_i = parrot[num_parr/2: 3*num_parr/4]
	receivers_i = parrot[3*num_parr/4:]
	#init = nest.Create("parrot_neuron", 2)
	#senders_e_init= init[0:1]
	#receivers_e_init = init[1:2]

	nest.CopyModel('sgritta_synapse', 'stdp',{'alpha': alpha, 'lambda': step, 'Wmax': maxweight, 'tau_plus': float(tau_p)})

	spikes_in = nest.Create('spike_detector', 1, {'to_file': True})
	spikes_out = nest.Create('spike_detector', 1)

	stimuli = nest.Create("spike_generator", 3)
	stimulus_e = stimuli[0]
	nest.SetStatus([stimulus_e], {'spike_times': [5.0, 10003.0]})

	''' PARTE DESTRA '''

	#delay = 0.1
	#nest.Connect(senders_e_init, receivers_e_init, {'rule': 'all_to_all'}, {'model':'stdp', 'weight': initweight, 'delay' : delay})	
	delay = 1
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

	#ini = nest.GetConnections(senders_e_init, receivers_e_init)
	#w_in = nest.GetStatus(ini, "weight")
	
	weights_e = np.zeros(101)
	m_e = max(weights_e)
	weights_e_perc = np.zeros(100)

	for i in range(0, 100):
		a = weights[i] - initweight
		weights_e[i+1] = a
		weights_e_perc[i] = (a/initweight) * 100

	
	m_e = max(weights_e)
	Inh = nest.GetConnections(senders_i, receivers_i)
	weights = nest.GetStatus(Inh, "weight")
	

	weights_i = np.zeros(100)
	m_i = min(weights_i)
	weights_i_perc = np.zeros(100)
	for i in range(0, 100):
		a = weights[i] - initweight	
		weights_i[(100 - 1) - i] = a
		weights_i_perc[(100 - 1)  - i] = (a/initweight) * 100
	
	m_i = min(weights_i)
	W = np.concatenate(( weights_i,weights_e))
	W_perc = np.concatenate((weights_i_perc, weights_e_perc))
	maxx = 0
	minn = 0
	pesi = np.concatenate((W, W_perc))
	for i, m_ei in enumerate(weights_e):		
		if m_ei == m_e:
			maxx = i
			
			
	for i, m_ii in enumerate(weights_i):
		if m_ii == m_i:
			minn = i
	
	deltaTime= range(-100, 100)
	print('DeltaTime of Maximum Value is :' + str(deltaTime[maxx + 99]))  #questa aggiunta serve perche' troviamo gli indici di max e min ma poi e' come se gli array fossero shiftati a partire da -100, questo non e' un problema per l'indice del minimo in quanto e' giusto che i valori di weightsi siamo shiftati partendo da -99 (perche' riguardano i deltaT negativi) mentre e' un problema per i valori di weightse percio' e' necessario andare ad aggiungere 99 (in quanto riguardano i valori di deltaT positivi)  


	print('DeltaTime of Minimum Value is :' + str(deltaTime[minn]))  
	
		
	return(pesi)



