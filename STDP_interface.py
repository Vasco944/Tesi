import Tkinter as tk
import numpy as np
import trovacsv
import os
import glob
from Tkinter import *
from tkMessageBox import *

checks = {}

global Model
global stdp

global alpha_min
global alpha_max
global step_min
global step_max
global mu_plus
global mu_minus
global initweight_min
global initweight_max
global maxweight_min
global maxweight_max
global tau_m_min
global tau_m_max
global tau_p_min
global tau_p_max
global deltaTime_e
global deltaTime_i
global c

c = 0

alpha_min = 0.1
alpha_max = 10.0

step_min = 0.1
step_max = 10.0

initweight_min = 0.1
initweight_max = 5.0

maxweight_min = 5.0
maxweight_max = 200.0

tau_m_min = 2.0
tau_m_max = 20.0

tau_p_min = 2.0
tau_p_max = 20.0

Model = 0
stdp = 0


#alpha, step, mu_plus, mu_minus, initweight, maxweight, tau_m, tau_p


def ModSelect(btn):
	global Model
	Model = btn
	
def STDPSelect(btn):
	global stdp
	stdp = btn
		

def choose_parameter():
	import numpy as np
	import estdp_fun
	import tkSimpleDialog
	global alpha
	global step
	global mu_plus
	global mu_minus
	global initweight
	global maxweight
	global tau_m
	global tau_p
	global alpha_min
	global alpha_max
	global step_min
	global step_max
	global mu_plus
	global mu_minus
	global initweight_min
	global initweight_max
	global maxweight_min
	global maxweight_max
	global tau_m_min
	global tau_m_max
	global tau_p_min
	global tau_p_max
	global top
	

	if not Model and stdp:
		showerror("Model Selection", "Please Select A Model")
	if not stdp and Model:
		showerror("STDP Selection", "Please Select STDP")
	if not stdp and not Model:
		showerror("Selection", "Please Select A Model and STDP")

	if Model == 'Guetig' and stdp == 'eSTDP':
		top = Toplevel(master)
		top.geometry('{}x{}'.format(1100, 500))

		alpha = Scale(top, from_= alpha_min, to= alpha_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = 'alpha',  orient=HORIZONTAL)
		alpha.grid(row = 0, column = 1)

		step = Scale(top, from_=step_min, to=step_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "lambda", orient=HORIZONTAL)
		step.grid(row = 1, column = 1)

		mu_plus = Scale(top, from_=0.0, to=1.0,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "mu_plus", orient=HORIZONTAL)
		mu_plus.grid(row = 2, column = 1)

		mu_minus = Scale(top, from_=0.0, to=1.0,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "mu_minus", orient=HORIZONTAL)
		mu_minus.grid(row = 3, column = 1)

		initweight = Scale(top, from_=initweight_min, to=initweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "InitWeight", orient=HORIZONTAL)
		initweight.grid(row = 4, column = 1)
		
		maxweight = Scale(top, from_=maxweight_min, to= maxweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "MaxWeight", orient=HORIZONTAL)
		maxweight.grid(row = 5, column = 1)

		tau_m = Scale(top, from_=tau_m_min, to=tau_m_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_minus", orient=HORIZONTAL)
		tau_m.grid(row = 6, column = 1)

		tau_p = Scale(top, from_=tau_p_min, to=tau_p_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_plus", orient=HORIZONTAL)
		tau_p.grid(row = 7, column = 1)

		Plot = tk.Button(top, text = "Plot", command = plot)
		Plot.grid(row = 8, column = 1)
		
	if Model == 'Additive' and stdp == 'eSTDP':
		top = Toplevel(master)
		top.geometry('{}x{}'.format(1100, 500))

		alpha = Scale(top, from_= alpha_min, to= alpha_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = 'alpha',  orient=HORIZONTAL)
		alpha.grid(row = 0, column = 1)

		step = Scale(top, from_=step_min, to=step_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "lambda", orient=HORIZONTAL)
		step.grid(row = 1, column = 1)

		mu_plus = 0.0

		mu_minus = 0.0

		initweight = Scale(top, from_=initweight_min, to=initweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "InitWeight", orient=HORIZONTAL)
		initweight.grid(row = 2, column = 1)
		
		maxweight = Scale(top, from_=maxweight_min, to= maxweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "MaxWeight", orient=HORIZONTAL)
		maxweight.grid(row = 3, column = 1)

		tau_m = Scale(top, from_=tau_m_min, to=tau_m_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_minus", orient=HORIZONTAL)
		tau_m.grid(row = 4, column = 1)

		tau_p = Scale(top, from_=tau_p_min, to=tau_p_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_plus", orient=HORIZONTAL)
		tau_p.grid(row = 5, column = 1)

		Plot = tk.Button(top, text = "Plot", command = plot)
		Plot.grid(row = 6, column = 1)

	if Model == 'Multiplicative' and stdp == 'eSTDP':
		top = Toplevel(master)
		top.geometry('{}x{}'.format(1100, 500))

		alpha = Scale(top, from_= alpha_min, to= alpha_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = 'alpha',  orient=HORIZONTAL)
		alpha.grid(row = 0, column = 1)

		step = Scale(top, from_=step_min, to=step_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "lambda", orient=HORIZONTAL)
		step.grid(row = 1, column = 1)

		mu_plus = 1.0

		mu_minus = 1.0

		initweight = Scale(top, from_=initweight_min, to=initweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "InitWeight", orient=HORIZONTAL)
		initweight.grid(row = 2, column = 1)
		
		maxweight = Scale(top, from_=maxweight_min, to= maxweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "MaxWeight", orient=HORIZONTAL)
		maxweight.grid(row = 3, column = 1)

		tau_m = Scale(top, from_=tau_m_min, to=tau_m_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_minus", orient=HORIZONTAL)
		tau_m.grid(row = 4, column = 1)

		tau_p = Scale(top, from_=tau_p_min, to=tau_p_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_plus", orient=HORIZONTAL)
		tau_p.grid(row = 5, column = 1)

		Plot = tk.Button(top, text = "Plot", command = plot)
		Plot.grid(row = 6, column = 1)

	if Model == 'van Rossum' and stdp == 'eSTDP':
		top = Toplevel(master)
		top.geometry('{}x{}'.format(1100, 500))

		alpha = Scale(top, from_= alpha_min, to= alpha_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = 'alpha',  orient=HORIZONTAL)
		alpha.grid(row = 0, column = 1)

		step = Scale(top, from_=step_min, to=step_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "lambda", orient=HORIZONTAL)
		step.grid(row = 1, column = 1)

		mu_plus = 0.0

		mu_minus = 1.0

		initweight = Scale(top, from_=initweight_min, to=initweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "InitWeight", orient=HORIZONTAL)
		initweight.grid(row = 2, column = 1)
		
		maxweight = Scale(top, from_=maxweight_min, to= maxweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "MaxWeight", orient=HORIZONTAL)
		maxweight.grid(row = 3, column = 1)

		tau_m = Scale(top, from_=tau_m_min, to=tau_m_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_minus", orient=HORIZONTAL)
		tau_m.grid(row = 4, column = 1)

		tau_p = Scale(top, from_=tau_p_min, to=tau_p_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_plus", orient=HORIZONTAL)
		tau_p.grid(row = 5, column = 1)

		Plot = tk.Button(top, text = "Plot", command = plot)
		Plot.grid(row = 6, column = 1)
	
	if Model and stdp == 'iSTDP':
		top = Toplevel(master)
		top.geometry('{}x{}'.format(1100, 500))

	        alpha = Scale(top, from_= 0.4, to= 0.6,length = 500, resolution = 0.01, label = 'C',  orient=HORIZONTAL)
		alpha.grid(row = 0, column = 1)

		step = Scale(top, from_=step_min, to=step_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "lambda", orient=HORIZONTAL)
		step.grid(row = 1, column = 1)

		mu_plus = 0.0

		mu_minus = 1.0

		initweight = Scale(top, from_=initweight_min, to=initweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "InitWeight", orient=HORIZONTAL)
		initweight.grid(row = 2, column = 1)
		
		maxweight = Scale(top, from_=maxweight_min, to= maxweight_max,length = 500,  tickinterval = 0.01, resolution = 0.1, label = "MaxWeight", orient=HORIZONTAL)
		maxweight.grid(row = 3, column = 1)

		tau_m = Scale(top, from_=tau_m_min, to=tau_m_max,length = 500,  tickinterval = 0.01, resolution = 0.1,  label = "tau_minus", orient=HORIZONTAL)
		tau_m.grid(row = 4, column = 1)

		tau_p = Scale(top, from_=2.0, to=200.0,length = 500,  tickinterval = 0.01, resolution = 1.0,  label = "tau_plus", orient=HORIZONTAL)
		tau_p.grid(row = 5, column = 1)

		Plot = tk.Button(top, text = "Plot", command = plot)
		Plot.grid(row = 6, column = 1)
		

def plot():
	from numpy import arange, sin, pi
	import Tkinter
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
	from matplotlib.figure import Figure
	import estdp_fun
	import istdp_fun
	global c
	if Model == 'Guetig':
		mu_p = mu_plus.get()
		mu_m = mu_minus.get()

	a = alpha.get()
	s = step.get()
	ini = initweight.get()
	maxw = maxweight.get()
	taum = tau_m.get()
	taup = tau_p.get()
	if Model != 'Guetig':
		mu_p = mu_plus
		mu_m = mu_minus
	
	if (stdp == 'eSTDP'):
		pesi = estdp_fun.eSTDP(a, s, mu_p, mu_m, ini, maxw, taum, taup)
		W = pesi[0:200]
		deltaTime= range(-100, 100)

		

	if (stdp == 'iSTDP'):
		pesi = istdp_fun.iSTDP(a, s, mu_p, mu_m, ini, maxw, taum, taup, c)
		c = c + 1
		W = pesi[0:600]
		deltaTime= range(-300, 300)
	f = Figure()
	a = f.add_subplot(111)
	a.plot(deltaTime, W)
	a.axhline(0, color = 'black')
	a.axvline(0, color='black')
	a.set_xlabel('Time Interval (ms)')
	a.set_ylabel('Delta Weights')

	dataPlot = FigureCanvasTkAgg(f, master=top)
	dataPlot.show()
	dataPlot.get_tk_widget().grid(row = 0, column = 2, rowspan = 1000)

	
master = Tk()
master.geometry('{}x{}'.format(300, 250))

btnList=['Additive', 'Multiplicative', 'Guetig', 'van Rossum']
btnMenu = tk.Menubutton(master, text='Model')
contentMenu = tk.Menu(btnMenu)
btnMenu.config(menu=contentMenu)
btnMenu.pack(pady = 10)

for btn in btnList:
	contentMenu.add_command(label=btn, command = lambda btn=btn: ModSelect(btn))
	btnMenu.pack()

graph_list=['eSTDP', 'iSTDP']

btnMenu = tk.Menubutton(master, text='STDP')
contentMenu = tk.Menu(btnMenu)
btnMenu.config(menu=contentMenu)
btnMenu.pack(pady = 10)

for btn in graph_list:
	contentMenu.add_command(label=btn, command =lambda btn= btn: STDPSelect(btn))
	btnMenu.pack()
	
	

ok = tk.Button(master, text = "Ok", command = choose_parameter)
ok.pack(pady = 10)
master.mainloop()

