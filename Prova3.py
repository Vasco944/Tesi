import pylab
import sys
import numpy
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


nodes=nest.Create('iaf_psc_delta', N_neurons)
nodes_E=nodes[:N_E]
nodes_I=nodes[N_E:]
noise=nest.Create('poisson_generator', 1, {'rate':p_rate})
spikes=nest.Create('spike_detector', 2, [{'label':'bruel-py-ex'},{'label':'bruel-py-in'}])
spikes_E=spikes[:1]
spikes_I=spikes[1:]

nest.CopyModel('stdp_synapse', 'alpha':1.0)
nest.Connect(nodes_E, nodes, {'rule':'fixed_indegree', 'indegree':C_E},{'model':'excitatory', 'delay':'delay', 'weight':{'distribution':'uniform', 'low':0.5*J_E, 'high':1.5*J_E}})

nest.Connect(nodes_I, nodes, {'rule':'fixed_indegree', 'indegree':C_I},{'model':'inhibitory', 'delay':'delay', 'weight':{'distribution':'uniform', 'low':0.5*J_E, 'high':1.5*J_E}})
nest.CopyModel('static_synapse_hom_w', 'excitatory', {'weight':J_I, 'delay':delay})
nest.Connect(noise, nodes, syn_spec='excitatory')

N_rec= 50
nest.Connect(nodes_E[:N_rec], spikes_E)
nest.Connect(nodes_I[:N_rec], spikes_I)


simtime=300
nest.Simulate(simtime)

msd=1000
n_vp=nest.GetKernelStatus('total_num_virtual_procs')
msdrange1=range(msd, msd+n_vp)
pyrngs=[numpy.random.RandomState(s) for s in msdrange1]
msdrange2= range(msd+n_vp+1, msd+1+2*n_vp)
nest.SetKernelStatus({'grng_seed': msd+n_vp, 'rng_seeds':msdrange2})

node_info=nest.GetStatus(nodes)
local_nodes=[(ni['global_id'], ni['vp']) for ni in node_info if ni['local']]

for gid, vp in local_nodes:
  nest.SetStatus([gid], {'V_m':pyrngs[vp].uniform(-V_th, V_th)})



pylab.figure()
V_E=nest.GetStatus(nodes_E[:N_rec], 'Vm')
pylab.hist(V_E, bins=10)
pylab.figure()
ex_conns=nest.GetConnections(nodes_E[:N_rec], synapse_model='excitatory')

w= nest.GetStatus(ex_conns, 'weight')
pylab.hist(w, bins=100)
N_rec_local_E=sum(nest.GetStatus(nodes_E[:N_rec], 'local'))
rate_ex=events[0]/simtime*1000.0/N_rec_local_E



pylab.show()









