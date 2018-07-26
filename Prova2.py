import pylab
import sys
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot

g  = 5.0
eta= 2.0
delay= 1.5
tau_m= 20.0
V_th= 20.0
N_E= 8000
N_I= 2000
N_neurons= N_E+N_I
C_E=N_E/10
C_I=N_I/10
J_E=0.1
J_I=-g*J_E
nu_ex=eta*V_th/(J_E*C_E*tau_m)
p_rate=1000.0*nu_ex*C_E

nest.SetKernelStatus({'print_time':True})
nest.SetDefaults('iaf_psc_delta',{'C_m':1.0, 'tau_m':tau_m, 't_ref':2.0, 'E_L': 0.0, 'V_th':V_th, 'V_rest': 10.0})

nodes=nest.Create('iaf_psc_delta', N_neurons)
nodes_E=nodes[:N_E]
nodes_I=nodes[N_E:]
noise=nest.Create('poisson_generator', 1, {'rate':p_rate})
spikes=nest.Create('spike_detector', 2, [{'label':'bruel-py-ex'},{'label':'bruel-py-in'}])
spikes_E=spikes[:1]
spikes_I=spikes[1:]

nest.CopyModel('static_synapse_hom_w', 'excitatory', {'weight':J_E, 'delay':delay})
nest.Connect(nodes_E, nodes, {'rule':'fixed_indegree', 'indegree':C_E}, 'excitatory')
nest.CopyModel('static_synapse_hom_w', 'inhibitory', {'weight':J_I, 'delay':delay})
nest.Connect(nodes_I, nodes, {'rule':'fixed_indegree', 'indegree':C_I}, 'inhibitory')

nest.Connect(noise, nodes, syn_spec='excitatory')

N_rec= 50
nest.Connect(nodes_E[:N_rec], spikes_E)
nest.Connect(nodes_I[:N_rec], spikes_I)


simtime=300
nest.Simulate(simtime)
events=nest.GetStatus(spikes, 'n_events')
rate_ex=events[0]/simtime*1000.0/N_rec
print "Excitatory rate   :%.2f 1/s" % rate_ex

nest.raster_plot.from_device(spikes_E, hist=True)

pylab.show()









