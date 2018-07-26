
import sys
import numpy as np
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import matplotlib as plt
import nest
import pylab

stim = nest.Create('poisson_generator', 1, {'rate':9000.0})
nodes = nest.Create('parrot_neuron_ps', 10)
nest.CopyModel('static_synapse_hom_w', 'excitatory', {'weight':0.5})
nest.Connect(stim, nodes, syn_spec='excitatory')

spikes1 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes2 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes3 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes4 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes5 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes6 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes7 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes8 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes9 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})
spikes10 = nest.Create('spike_detector', 1, {"to_memory": True, "to_file":False, "withgid":True, "withtime":  True, "label":"Spike_Detector"})

nest.Connect(nodes[:1], spikes1)
nest.Connect(nodes[1:2], spikes2)
nest.Connect(nodes[2:3], spikes3)
nest.Connect(nodes[3:4], spikes4)
nest.Connect(nodes[4:5], spikes5)
nest.Connect(nodes[5:6], spikes6)
nest.Connect(nodes[6:7], spikes7)
nest.Connect(nodes[7:8], spikes8)
nest.Connect(nodes[8:9], spikes9)
nest.Connect(nodes[9:],spikes10)



nest.Simulate(100)
	
dSD = nest.GetStatus(spikes10,keys="events")[0]
ts = dSD["times"]
t = len(ts)

for i in range(0, int(t)):
	print(i)
print(t)
