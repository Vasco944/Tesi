import Tkinter as tk
import numpy as np
import trovacsv
import os
import glob
from Tkinter import *
from tkMessageBox import *

checks = {}
global input5
global input6
global Trial
global Connection

Trial = 0
Connection = 0
def ConSelect(btn):
	global Connection
	Connection = btn 
	

def TrialSelect(graphbtn):
	global Trial
	Trial = graphbtn

def ok2():
	import matplotlib.pyplot as plt
	import math
	import numpy as np
	import tkSimpleDialog
	global top
	global input3
	global input4
	global input5
	global input6
	global flag
	global Matrix
	
	if(flag == 'RR'):
		bt = input3.get()
		et = input4.get()
		bc = input5.get()
		ec = input6.get()
		trial = np.arange(int(bt), int(et) + 1)
		row = 3.0 # aggiungo il +1 alle colonne del subplot per evitare che dia problemi con le distanze cn valori pari ai multipli di row
		d =int(ec)-int(bc)
		col = math.ceil(float(d)/row)
		if(int(bc) > int(ec) or int(bt) > int(et)):
			showerror("Invalid Selection", "End Value Smaller Than Starting Value")
		
		if(int(bc) < int(ec) and int(bt) < int(et)):
			if(int(bc) > len(Matrix[:, 1]) or int(ec) > len(Matrix[:, 1]) or int(bt) > len(Matrix[1, :]) - 1 or int(et) > len(Matrix[1, :]) - 1):
				showerror("Invalid Selection", "Index Out Of Bounds")
			if(int(bc) <= len(Matrix[:, 1]) and int(ec) <= len(Matrix[:, 1]) and int(bt) <= len(Matrix[1, :])  - 1 and int(et) <= len(Matrix[1, :]) - 1):
				fig = plt.figure()
				lims = np.amax(Matrix[int(bc):int(ec) + 1, int(bt):int(et) + 1])
				limi = np.amin(Matrix[int(bc):int(ec) + 1, int(bt):int(et) + 1])	
				for i in range(int(bc), int(ec) + 1):
		    			ax = fig.add_subplot(row,int(col) + 1, i - int(bc) + 1)
		    			ax.plot(trial, Matrix[i - 1, int(bt):int(et) + 1])
					plt.ylim(limi, lims)
		   		 	ax.set_title('Connection Number' + str(i))
				
				plt.show()

	if(flag == 'RS'):
		bt = input3.get()
		et = input4.get()
		bc = input5.get()
		if(int(bt) > int(et)):
			showerror("Invalid Selection", "End Value Smaller Than Starting Value")
		if(int(bt) < int(et)):
			if(int(bt) > len(Matrix[1, :]) - 1 or int(et) > len(Matrix[1, :]) - 1 or int(bc) > len(Matrix[:, 1])):
				showerror("Invalid Selection", "Index Out Of Bounds")
			if(int(bt) <= len(Matrix[1, :]) - 1 and int(et) <= len(Matrix[1, :]) - 1 and int(bc) <= len(Matrix[:, 1])):	
				trial = np.arange(int(bt), int(et) + 1)
				plt.plot(trial, Matrix[int(bc) - 1, int(bt):int(et) + 1])
				plt.title('Connection Number' + str(bc))
				plt.show()

	if(flag == 'AR'):
		bc = input3.get()
		ec = input4.get()
		if(int(bc) > int(ec)):
			showerror("Invalid Selection", "End Value Smaller Than Starting Value")
		if(int(bc) < int(ec)):
			if(int(bc) > len(Matrix[:, 1]) or int(ec) > len(Matrix[:, 1])):
				showerror("Invalid Selection", "Index Out Of Bounds")

			if(int(bc) <= len(Matrix[:, 1])or int(ec) <= len(Matrix[:, 1])):
				lims = np.amax(Matrix[int(bc):int(ec) + 1, 1:])
				limi = np.amin(Matrix[int(bc):int(ec) + 1,1:])
				trial = np.arange(1, len(Matrix[0, :]))
				fig = plt.figure()
				row = 3.0
				d =int(ec)-int(bc)

				col = math.ceil(float(d)/row)
				for i in range(int(bc), int(ec) + 1):
		    			ax = fig.add_subplot(row,int(col) + 1, i - int(bc) + 1)
		    			ax.plot(trial, Matrix[i - 1, 1:])
					plt.ylim(limi, lims)
		   		 	ax.set_title('Connection Number' + str(i))
	
				plt.show()


	if(flag == 'RA'):
		bt = input3.get()
		et = input4.get()
		bins = input5.get()
		maxxv = 0
		if(int(bt) > int(et)):
			showerror("Invalid Selection", "End Value Smaller Than Starting Value")
		if(int(bt) < int(et)):
			if(int(bt) > len(Matrix[1, :]) - 1 or int(et) > len(Matrix[1, :]) - 1):
				showerror("Invalid Selection", "Index Out Of Bounds")
			if(int(bt) <= len(Matrix[1, :]) - 1 and int(et) <= len(Matrix[1, :]) - 1):	
				con = np.arange(1, len(Matrix[:, 1]) + 1)
				row = 3.0
				d =int(et)-int(bt)
				col = math.ceil(float(d)/row)
				lims = np.amax(Matrix[:, int(bt):int(et) +1])
				limi = np.amin(Matrix[:,int(bt):int(et) + 1])
				print('minimun weight value = ' + str(limi))
				for i in range(int(bt), int(et) + 1):
		    			x, y = np.histogram(Matrix[:, i])
					maxx = np.amax(x)
					if(maxx > maxxv):
						maxxv = maxx
				fig = plt.figure()
					
				for i in range(int(bt), int(et) + 1):
		    			ax = fig.add_subplot(row,int(col) + 1, i - int(bt) + 1)
		    			ax.hist(Matrix[:, i], bins = int(bins))
					plt.ylim(0, maxxv)
					plt.xlim(limi - 0.1, lims)
		   		 	ax.set_title('Trial Number' + str(i))
				
				plt.show()

	


	if(flag == 'AS'):
		bc = input3.get()
		if(int(bc) > len(Matrix[:, 1])):
				showerror("Invalid Selection", "Index Out Of Bounds")

		if(int(bc) <= len(Matrix[:, 1])):
			trial = np.arange(1, len(Matrix[0, :]))
			plt.plot(trial, Matrix[int(bc) - 1, 1:])
			plt.title('Connection Number' + str(bc))
			plt.show()

	if(flag == 'SR'):
		bt = input3.get()
		bins = input4.get()
		bc = input5.get()
		ec = input6.get()
		if(int(bc) > int(ec)):
			showerror("Invalid Selection", "End Value Smaller Than Starting Value")
		if(int(bc) < int(ec)):
			if(int(bc) > len(Matrix[:, 1]) or int(ec) > len(Matrix[:, 1]) or int(bt) > len(Matrix[1, :]) - 1):
				showerror("Invalid Selection", "Index Out Of Bounds")
			if(int(bc) <= len(Matrix[:, 1]) and int(ec) <= len(Matrix[:, 1]) and int(bt) <= len(Matrix[1, :]) - 1):
				con = np.arange(int(bc), int(ec) + 1)
				plt.hist(Matrix[int(bc) - 1:int(ec), int(bt)], bins = int(bins))
				plt.title('Connection Number' + str(bc))
				plt.show()

	if(flag == 'SA'):
		bt = input3.get()
		bins = input4.get()
		if(int(bt) > len(Matrix[1, :]) - 1):
			showerror("Invalid Selection", "Index Out Of Bounds")

		if(int(bt) <= len(Matrix[1, :]) - 1):
			con = np.arange(1, len(Matrix[:, 1]) + 1)
			plt.hist(Matrix[:, int(bt)], bins = int(bins))
			plt.title('Trial Number' + str(bt))
			plt.show()
	

def ok():
	import tkSimpleDialog
	global Trial
	global Connection
	global top
	global input3
	global input4
	global input5
	global input6
	global flag
	flag = 0

	if not Trial or not Connection:
		showerror("Plotting Details", "Please Select Plotting Details")
	if Trial and Connection:
		if(Trial == 'Range' and Connection == 'Range'):
			Label (top, text = "Starting Trial").grid (row=34, column = 0)
			input3 = Entry(top)
			input3.grid(row = 34, column = 1)

			Label (top, text = "Endig Trial").grid (row=34, column = 30)
			input4 = Entry(top)
			input4.grid(row = 34, column =32)

			Label (top, text = "Starting Connection").grid (row=35, column = 0)
			input5 = Entry(top)
			input5.grid(row = 35, column = 1)

			Label (top, text = "Ending Connection").grid (row=35, column = 30)
			input6 = Entry(top)
			input6.grid(row = 35, column = 32)

			flag = 'RR'

		if(Trial == 'Range' and Connection == 'Single'):
			Label (top, text = "Starting Trial").grid (row=34, column = 0)
			input3 = Entry(top)
			input3.grid(row = 34, column = 1)

			Label (top, text = "Endig Trial").grid (row=34, column = 30)
			input4 = Entry(top)
			input4.grid(row = 34, column =32)

			Label (top, text = "Connection's Number").grid (row=35, column = 0)
			input5 = Entry(top)
			input5.grid(row = 35, column = 1)

			flag = 'RS'

		if(Trial == 'Range' and Connection == 'All'):
			Label (top, text = "Starting Trial").grid (row=34, column = 0)
			input3 = Entry(top)
			input3.grid(row = 34, column = 1)

			Label (top, text = "Endig Trial").grid (row=34, column = 30)
			input4 = Entry(top)
			input4.grid(row = 34, column =32)

			Label (top, text = "Bins Number").grid (row=35, column = 0)
			input5 = Entry(top)
			input5.grid(row = 35, column = 1)

			flag = 'RA'
			

		if(Trial == 'All' and Connection == 'Range'):
			
			Label (top, text = "Starting Connection").grid (row=34, column = 0)
			input3 = Entry(top)
			input3.grid(row = 34, column = 1)

			Label (top, text = "Endig Connection").grid (row=34, column = 30)
			input4 = Entry(top)
			input4.grid(row = 34, column =32)
		
			flag = 'AR'
			
		if(Trial == 'All' and Connection == 'Single'):
			Label (top, text = "Connection's Number").grid (row=34, column = 0)
			input3 = Entry(top)
			input3.grid(row = 34, column = 1)

			flag = 'AS'

		if(Trial == 'Single' and Connection == 'Range'):
			Label (top, text = "Trial's Number").grid (row=34, column = 0)
			input3 = Entry(top)
			input3.grid(row = 34, column = 1)

			Label (top, text = "Bins Number").grid (row=34, column = 30)
			input4 = Entry(top)
			input4.grid(row = 34, column =32)

			Label (top, text = "Starting Connection").grid (row=35, column = 0)
			input5 = Entry(top)
			input5.grid(row = 35, column = 1)

			Label (top, text = "Ending Connection").grid (row=35, column = 30)
			input6 = Entry(top)
			input6.grid(row = 35, column = 32)

			flag = 'SR'

		if(Trial == 'Single' and Connection == 'All'):
			
			Label (top, text = "Trial's Number").grid (row=34, column = 0)
			input3 = Entry(top)
			input3.grid(row = 34, column = 1)
			
			Label (top, text = "Bins Number").grid (row=34, column = 30)
			input4 = Entry(top)
			input4.grid(row = 34, column =32)

			flag = 'SA'
		if(Trial == 'Single' and Connection == 'Single'):
			showerror("Invalid Selection", "Cannot Plot One Value")

		if(Trial == 'All' and Connection == 'All'):
			showerror("Invalid Selection", "Cannot Plot So Many Graph")
		if flag:
			B = tk.Button(top, text = "Plot", command = ok2)
			B.grid(row = 100, column = 0)
def put_togheter():
	import funzioni_pesi
	import csv
	import tkSimpleDialog
	global input1
	global input2
	global csv_vector
	global top
	global Matrix
	values = [(var.get()) for data, var in checks.items()]
	csv_vector = funzioni_pesi.choosecsv(values, result)
	if not csv_vector:
		showerror("CSV selection", "Please Select A file")
		
	if csv_vector:
		import funzioni_pesi
		global Matrix
		global trial
		time = input1.get()
		trial = input2.get()
		if not time or not trial:
			showerror("Parameters selection", "Please Insert some Values")
		if time and trial:
			Matrix = funzioni_pesi.MatrixCreation(int(trial), int(time), csv_vector)
			top = Toplevel(master)
			top.geometry('{}x{}'.format(400, 50))
			b = Button(top, text="Save as csv", command= saveMatrix)
			b.grid(row = 1, column = 0)
			b1 = Button(top, text="Plot Menu", command= plot)
			b1.grid(row = 1, column = 1 )
			b2 = Button(top, text="Print Matrix", command= printer)
			b2.grid(row = 1, column = 2 )
			b3 = Button(top, text="Cancel", command= cancel)
			b3.grid(row = 1, column = 3 )


def plot():
	import math
	import matplotlib.pyplot as plt
	import tkSimpleDialog
	global trial
	global input3
	global input4
	global top1
	global begin
	global end
	global Trial
	global top
	flag = 0
	n_connection = 0
	top = Toplevel(master)
	top.geometry('{}x{}'.format(1000, 400))
	btnList=['Single', 'Range', 'All']
	btnMenu = tk.Menubutton(top, text='Conncetions')
	contentMenu = tk.Menu(btnMenu)
	btnMenu.config(menu=contentMenu)
	btnMenu.grid(row = 0, column = 0)
	i = 0
	for btn in btnList:
		contentMenu.add_command(label=btn, command = lambda btn=btn: ConSelect(btn))
		btnMenu.grid(row = i, column = 0)
		i = i +1
	
	i = 30
	graph_list=['Single', 'Range', 'All']
	btnMenu = tk.Menubutton(top, text='Trails')
	contentMenu = tk.Menu(btnMenu)
	btnMenu.config(menu=contentMenu)
	btnMenu.grid(row = 30, column = 0)
	B = tk.Button(top, text = "OK", command = ok)
	B.grid(row = 33, column = 0)
	for btn in graph_list:
		contentMenu.add_command(label=btn, command =lambda btn= btn: TrialSelect(btn))
		btnMenu.grid(row = i, column = 0)
		i = i +1
	

def printer():
	np.set_printoptions(threshold = 'nan')
	print(Matrix[:, :])

def cancel():
	top.destroy()

def cancel1():
	top1.destroy()

def saveMatrix():
	import csv		
	myFile = open('example.csv', 'w')
	with myFile:
   		writer = csv.writer(myFile)
    		writer.writerows(Matrix)
	
master = Tk()
master.geometry('{}x{}'.format(300, 250))



Label (master, text = "Trial's Time (ms)").grid (row=0, column = 0, sticky=E)
input1 = Entry(master)
input1.grid(row = 0, column= 1)


Label (master, text = "Number of Trials").grid (row=1, column = 0, sticky=E)
input2 = Entry(master)
input2.grid(row = 1, column = 1)

Label (master, text = "Select csv Files").grid (row=800, column = 0, sticky=E)

result = trovacsv.result
l=len(result)	
for i in range(0, l):		
	var = IntVar()
	Check_Bcsv = Checkbutton(master, text = result[i], variable = var)
	checks[i] = var
	Check_Bcsv.grid(row = i + 805,  sticky = W)


B_csv = tk.Button(master, text = "Find csv Files", command = put_togheter)
B_csv.grid(row = 1000, column = 0)



master.mainloop()
