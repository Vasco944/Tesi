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

def ok2():
	import math
	import tkSimpleDialog
	import matplotlib.pyplot as plt
	global input3
	global input4
	global input5
	global input6
	global Trial
	global top1
	begin = input3.get()
	end = input4.get()
	top1.destroy()
	for item in range(int(begin), int(end) + 1):
		plt.subplot(3, math.ceil((int(end) - int(begin))/3), item)
		plt.plot(Trial, Matrix[int(begin) - 1:int(end) - 1, Trial[0]:Trial[len(Trial) - 1]])
		plt.title('Connection' + str(Matrix[item, 0]))
		plt.show()


def ok():
	global input3
	global input4
	global input5
	global input6
	global top1
	global Trial
	import math
	import tkSimpleDialog
	import matplotlib.pyplot as plt

	begin = input3.get()
	end = input4.get()
	top1.destroy()
	Trial = np.zeros(2)
	Trial[0] = begin
	Trial[1] = end
	f = int(end) - int(begin) + 1
	Trial = np.arange(1, f)	
	n_connection = tkSimpleDialog.askstring("How many Connections Do You Want to Plot?", "Single/All/Range/Specific")#specific serve se ne voglio plottare tante diverse

	if (n_connection == 'range' or n_connection == 'Range'):
		top1 = Toplevel(master)
		Label (top1, text = "Beginning").grid (row=0, column = 0, sticky=E)
		input5 = Entry(top1)
		input5.grid(row = 0, column = 1)
		Label (top1, text = "End").grid (row=1, column = 0, sticky=E)
		input6 = Entry(top1)
		input6.grid(row = 1, column = 1)
		b5 = Button(top1, text="OK", command= ok2)
		b5.grid(row = 2, column = 0)
		b6 = Button(top1, text="Cancel", command= cancel1)
		b6.grid(row = 2, column = 1)

	if (n_connection == 'single' or n_connection == 'Single'):
		connection = tkSimpleDialog.askinteger("Which Connection Do You Want to Plot?", "Select Trial")
		
		plt.plot(Matrix[connection - 1, Trial[0]:Trial[len(Trial) - 1]])
		plt.title('Connection' + str(connection))
		plt.show()

	if (n_connection == 'all' or n_connection == 'All'):	
		for item in range(0, len(Matrix) - 1):
			plt.subplot(10, math.ceil((end - begin)/10), item)
			plt.plot(Trial, Matrix[0:, Trial[0]:Trial[len(Trial) - 1]])
			plt.title('Connection' + str(Matrix[item, 0]))
def put_togheter():
	import funzioni_pesi
	import csv
	import tkSimpleDialog
	global input1
	global input2
	global csv_vector
	global top

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
	global trial
	global input3
	global input4
	global top1
	global begin
	global end
	global Trial
	flag = 0
	n_connection = 0
	import tkSimpleDialog
	n_trial = tkSimpleDialog.askstring("How many Trial Do You Want to Plot?", "Single/All/Range")
	if (n_trial == 'range' or n_trial == 'Range'):
		
		top1 = Toplevel(master)
		Label (top1, text = "Beginning").grid (row=0, column = 0, sticky=E)
		input3 = Entry(top1)
		input3.grid(row = 0, column = 1)
		Label (top1, text = "End").grid (row=1, column = 0, sticky=E)
		input4 = Entry(top1)
		input4.grid(row = 1, column = 1)
		b4 = Button(top1, text="OK", command= ok)
		b4.grid(row = 2, column = 0)
		b5 = Button(top1, text="Cancel", command= cancel1)
		b5.grid(row = 2, column = 1)
		

	if (n_trial == 'single' or n_trial == 'Single'):
		Trial = tkSimpleDialog.askint("Which Trial Do You Want to Plot?", "Select Trial")
		n_connection = tkSimpleDialog.askstring("How many Connections Do You Want to Plot?", "Single/All/Range/Specific")
		if (n_connection == 'range' or n_connection == 'Range'):
			top1 = Toplevel(master)
			Label (top1, text = "Beginning").grid (row=0, column = 0, sticky=E)
			input3 = Entry(top1)
			input3.grid(row = 0, column = 1)
			Label (top1, text = "End").grid (row=1, column = 0, sticky=E)
			input4 = Entry(top1)
			input4.grid(row = 1, column = 1)
			b5 = Button(top1, text="OK", command= ok)
			b5.grid(row = 2, column = 0)
			b6 = Button(top1, text="Cancel", command= cancel1)
			b6.grid(row = 2, column = 1)
		for item in range(begin, end + 1):
			plt.subplot(3, math.ceil((end - begin)/3), item)
			plt.plot(Trial, Matrix[begin - 1:end - 1, Trial[0]:Trial[len(Trial) - 1]])
			plt.title('Connection' + str(Matrix[item, 0]))

		if (n_connection == 'single' or n_connection == 'Single'):
			connection = tkSimpleDialog.askint("Which Connection Do You Want to Plot?", "Select Trial")
		
			plt.plot(Matrix[connection - 1, Trial[0]:Trial[len(Trial) - 1]])
			plt.title('Connection' + str(connection))

		if (n_connection == 'all' or n_connection == 'All'):	
			for item in range(0, len(Matrix) - 1):
				plt.subplot(10, math.ceil((end - begin)/10), item)
				plt.plot(Trial, Matrix[0:, Trial[0]:Trial[len(Trial) - 1]])
				plt.title('Connection' + str(Matrix[item, 0]))


	if (n_trial == 'all' or n_trial == 'All'):
		Trial = np.arange(1, len(Matrix[0, :]))
		
 		n_connection = tkSimpleDialog.askstring("How many Connections Do You Want to Plot?", "Single/All/Range/Specific")
		if (n_connection == 'range' or n_connection == 'Range'):
			top1 = Toplevel(master)
			Label (top1, text = "Beginning").grid (row=0, column = 0, sticky=E)
			input3 = Entry(top1)
			input3.grid(row = 0, column = 1)
			Label (top1, text = "End").grid (row=1, column = 0, sticky=E)
			input4 = Entry(top1)
			input4.grid(row = 1, column = 1)
			b5 = Button(top1, text="OK", command= ok)
			b5.grid(row = 2, column = 0)
			b6 = Button(top1, text="Cancel", command= cancel1)
			b6.grid(row = 2, column = 1)
			for item in range(begin, end + 1):
				plt.subplot(3, math.ceil((end - begin)/3), item)
				plt.plot(Trial, Matrix[begin - 1:end - 1, Trial[0]:Trial[len(Trial) - 1]])
				plt.title('Connection' + str(Matrix[item, 0]))

		if (n_connection == 'single' or n_connection == 'Single'):
			connection = tkSimpleDialog.askinteger("Which Connection Do You Want to Plot?", "Select Trial")
		
			plt.plot(Trial, Matrix[connection - 1, 1:])
			plt.title('Connection' + str(connection))
			plt.show()
		if (n_connection == 'all' or n_connection == 'All'):	
			for item in range(0, len(Matrix) - 1):
				plt.subplot(10, math.ceil((end - begin)/10), item)
				plt.plot(Trial, Matrix[0:, Trial[0]:Trial[len(Trial) - 1]])
				plt.title('Connection' + str(Matrix[item, 0])) 		



def printer():
	print(Matrix)

def cancel():
	top.destroy()

def cancel1():
	top1.destroy()

def saveMatrix():
	import csv		
	myFile = open('example', 'w')
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
