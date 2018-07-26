
import pylab
import matplotlib.pyplot as plt
import sys
import numpy as np
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot
import nest.voltage_trace
nest.ResetKernel()
n_e=2000
n_i=1000
n_tot=n_e+n_i

c_e=n_e/10
c_i=n_i/10
j_e=0.2
j_self=0.0000001

w_min_e=0.0
w_max_e=0.001

w_min_i=-w_max_e
w_max_i=-w_min_e

amp_e=1.5
freq_e=4.0
amp_i=1.0
freq_i=2.0

p_rate=8000.0
N_rec=100
tsim=300
threads=8
delay=10.0

#nest.SetKernelStatus({'local_num_threads':threads})

nodes=nest.Create('iaf_psc_delta', n_tot)
nodes_e=nodes[:n_e]			
nodes_i=nodes[n_e:n_tot]


recdict= {"to_memory": False, 
            "to_file":    True,
            "label":     "PESI",
	  
            "senders": nodes_e[:10],
            "targets": nodes_i[:20]
            }
Weights = nest.Create('weight_recorder',params=recdict)

	
voltmeter=nest.Create('voltmeter', 1, {'withgid': True})
noise=nest.Create('poisson_generator', 1, {'rate':p_rate})
sine_e=nest.Create('ac_generator', 1, {'amplitude':amp_e, 'frequency':freq_e})
sine_i=nest.Create('ac_generator', 1, {'amplitude':amp_i, 'frequency':freq_i})

spikes_e=nest.Create('spike_detector', 1)


nest.CopyModel('static_synapse_hom_w', 'excitatory', {'weight':j_e})
nest.CopyModel('static_synapse_hom_w', 'sel_exc', {'weight':j_self})
nest.Connect(sine_e, nodes_e, syn_spec='excitatory')
nest.Connect(sine_i, nodes_i, syn_spec='excitatory')

nest.Connect(noise, nodes_e, syn_spec='excitatory')
nest.Connect(noise, nodes_i, syn_spec='excitatory')

nest.SetDefaults('stdp_synapse_hom', {'weight_recorder' : Weights[0]})
nest.CopyModel('stdp_synapse_hom', 'plastic-synapse',{'alpha':0.01, 'Wmax':0.01})

nest.Connect(nodes_e, nodes_i, {'rule':'fixed_indegree', 'indegree':c_e},{'model':'plastic-synapse', 'weight':{'distribution':'uniform', 'low':w_min_e, 'high':w_max_e}, 'delay': delay})
nest.Connect(nodes_e, nodes_e, syn_spec='sel_exc')
nest.Connect(nodes_i, nodes_e, {'rule':'fixed_indegree', 'indegree':c_i},{'model':'plastic-synapse', 'weight':{'distribution':'uniform', 'low':w_min_i, 'high':w_max_i}, 'delay': delay})
nest.Connect(nodes_i, nodes_i,syn_spec='sel_exc')



nest.Connect(nodes_e[:N_rec], spikes_e)
nest.Connect(voltmeter, nodes_e[90:91])
nest.Simulate(tsim)

#plt.subplot(2,1,1)

nest.raster_plot.from_device(spikes_e, hist=True)

#x1 = np.linspace(0.0, 5.0)
#y2 = np.cos(2 * np.pi * x1)
#plt.subplot(2,1,1)
#plt.plot(x1, y2)

#plt.subplot(2,1,2)
plt.figure()
nest.voltage_trace.from_device(voltmeter)
plt.show()
##PSD




