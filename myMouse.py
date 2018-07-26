import matplotlib.pyplot as plt
import sys
import numpy as np
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot
import nest.voltage_trace
nest.ResetKernel()

gr = 1000
pc = 100
mli = 200
n_tot = gr + pc + mli

ampTG = 1.5
ampPN = 1.0
freqTG = 5.0
freqPN = 2.0

p_noise = 3000.0

j_e = 1.5
j_i = -0.5
j_noise = 0.2

c_pc = gr/10
c_mli = gr/100
c_i = mli/10
tsim = 500

nodes = nest.Create('iaf_psc_delta', n_tot)

Gr = nodes[:gr]
PC = nodes[gr:gr + pc]
MLI = nodes[gr + pc:n_tot]


voltmeter = nest.Create('voltmeter', 1,{'withgid': True})
sineTG = nest.Create('ac_generator', 1, 
		    {'amplitude': ampTG,
		    'frequency': freqTG})

sinePN = nest.Create('ac_generator', 1, 
		    {'amplitude': ampPN,
		    'frequency': freqPN})
noise = nest.Create('poisson_generator', 1, 
		    {'rate': p_noise})

nest.CopyModel('static_synapse_hom_w', 'excitatory', {'weight':j_e})
nest.CopyModel('static_synapse_hom_w', 'exc_noise', {'weight':j_noise})
nest.CopyModel('static_synapse_hom_w', 'inhibitory', {'weight':j_i})

nest.Connect(noise, Gr, syn_spec = 'exc_noise')
nest.Connect(noise, PC, syn_spec = 'exc_noise')
nest.Connect(noise, MLI, syn_spec = 'exc_noise')

nest.Connect(sineTG, Gr, syn_spec = 'excitatory')
nest.Connect(sinePN, Gr, syn_spec = 'excitatory')

nest.Connect(Gr, PC,{'rule':'fixed_indegree', 'indegree':c_pc},
		    {'model': 'excitatory'})
nest.Connect(Gr, MLI,{'rule':'fixed_indegree', 'indegree':c_mli},
		    {'model': 'excitatory'})
nest.Connect(PC, MLI,{'rule':'fixed_indegree', 'indegree':c_i},
		    {'model': 'inhibitory'})


nest.Connect(voltmeter, PC[20:30])

nest.Simulate(tsim)

plt.figure()
nest.voltage_trace.from_device(voltmeter)
plt.show()















