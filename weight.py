
import pylab
import matplotlib.pyplot as plt
import sys
import numpy
sys.path.append("/home/vasco/Documenti/NEST/lib/x86_64-linux-gnu/python2.7/site-packages")
import nest
import nest.raster_plot
import nest.voltage_trace
nest.ResetKernel()

PRE = nest.Create("iaf_cond_exp", 1)
POST = nest.Create("iaf_cond_exp", 1)

recdict = {"to_memory": False,
           "to_file":    True,
           "label":     "PESI",
           "senders":    PRE,
           "targets":    POST
           }
WeightRec= nest.Create('weight_recorder',params=recdict)

nest.SetDefaults('static_synapse',{ "weight_recorder" : WeightRec[0]})
conn_param = {"model":  'static_synapse',
                           "weight": 1.0,
                           "delay":  1.0}

nest.Connect(PRE,POST,{'rule': 'one_to_one'},conn_param)

Input_generation = nest.Create("poisson_generator", 1)
nest.SetStatus(Input_generation, {'rate' : 10.0})
nest.Connect(Input_generation,PRE,'one_to_one',{'weight': 10000.0})

nest.Simulate(300.0)








