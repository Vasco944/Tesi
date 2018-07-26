
import pylab
import matplotlib.pyplot as plt
import sys
import numpy
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot
import nest.voltage_trace
nest.ResetKernel()
n_e=2000
n_i=1000
n_tot=n_e+n_i
n_parr=1000
n_rep=1000

c_e=n_e/10
c_i=n_i/10
j_e=1.5
j_i=-j_e

w_min_e=0.5
w_max_e=1.5

w_min_i=-w_max_e
w_max_i=-w_min_e

amp_e=150.0
freq_e=4.0
amp_i=100.0
freq_i=2.0

p_rate=8000.0
N_rec=100
tsim=300
threads=8

nest.SetKernelStatus(['local_num_threds': threds])
nodes=nest.Create('iaf_psc_delta', n_tot+n_rep)
nodes_e=nodes[:n_e]			
nodes_i=nodes[n_e:n_tot]
nodes_rep=nodes[n_tot:n_tot+n_rep]
nodes_par=nest.Create('parrot_neuron_ps', n_parr)
		

voltmeter=nest.Create('voltmeter', 1, {'withgid': True})
noise=nest.Create('poisson_generator', 1, {'rate':p_rate})
sine_e=nest.Create('ac_generator', 1, {'amplitude':amp_e, 'frequency':freq_e})
sine_i=nest.Create('ac_generator', 1, {'amplitude':amp_i, 'frequency':freq_i})

spikes_e=nest.Create('spike_detector', 1)


nest.CopyModel('static_synapse_hom_w', 'excitatory', {'weight':j_e})
nest.CopyModel('static_synapse_hom_w', 'inhibitory', {'weight':j_i})
nest.Connect(sine_e, nodes_e, syn_spec='excitatory')
nest.Connect(sine_i, nodes_i, syn_spec='excitatory')

nest.Connect(noise, nodes_e, syn_spec='excitatory')
nest.Connect(noise, nodes_i, syn_spec='excitatory')
nest.Connect(noise, nodes_par, syn_spec='excitatory')
nest.Connect(noise, nodes_rep, syn_spec='excitatory')

nest.CopyModel('stdp_synapse_hom', 'plastic-synapse')

nest.Connect(nodes_e, nodes_i, {'rule':'fixed_indegree', 'indegree':c_e},{'model':'plastic-synapse', 'weight':{'distribution':'uniform', 'low':w_min_e, 'high':w_max_e}, 'Wmax':3})
nest.Connect(nodes_e, nodes_e)
nest.Connect(nodes_i, nodes_e, {'rule':'fixed_indegree', 'indegree':c_i},{'model':'plastic-synapse', 'weight':{'distribution':'uniform', 'low':w_min_i, 'high':w_max_i}, 'Wmax':3})
nest.Connect(nodes_i, nodes_i)
nest.Connect(nodes_e[:1000], nodes_par)
nest.Connect(nodes_par, nodes_rep)


nest.Connect(nodes_rep[:N_rec], spikes_e)
nest.Connect(voltmeter, nodes_rep[500:501])
nest.Simulate(tsim)


nest.raster_plot.from_device(spikes_e, hist=True)

pylab.figure()
nest.voltage_trace.from_device(voltmeter)

pylab.show()









