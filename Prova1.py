import pylab
import sys
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.voltage_trace
neuron = nest.Create('iaf_psc_alpha')
sine = nest.Create('ac_generator',1, {'amplitude':100.0, 'frequency':2.0})

noise= nest.Create('poisson_generator', 2, [{'rate':70000.0},{'rate':20000.0}])

voltmeter=nest.Create('voltmeter', 1, {'withgid': True})

nest.Connect(sine, neuron)
nest.Connect(voltmeter, neuron)
nest.Connect(noise[:1], neuron, syn_spec={'weight':1.0, 'delay': 1.0})
nest.Connect(noise[1:], neuron, syn_spec={'weight':-1.0, 'delay': 1.0})
nest.Simulate(1000.0)
nest.voltage_trace.from_device(voltmeter)
pylab.show()
