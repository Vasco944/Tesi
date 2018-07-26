def put_togheter(vector):
	global M
	import csv
	import numpy as np
	i = 1
	for pos in range(0, len(vector)):

		with open(vector[pos]) as pesicsv:
			lettore=csv.reader(pesicsv, delimiter="\t")
		
			for row in lettore:
		
				if(i == 1):			
					P = np.array([[int(row[0]), int(row[1]),float(row[2]), float(row[3])]]) 
					
						
				if(i != 1):
					a = np.array([[int(row[0]), int(row[1]),float(row[2]), float(row[3])]])
					P = np.concatenate((P,a), axis=0)
				i=i+1
		
		if(pos == 0):
			M = P
		if(pos != 0):
			M = np.concatenate((M, P), axis = 0)
	
	return(M)

def choosecsv(vector, vector1):
	import numpy as np
	x = np.nonzero(vector)
	check_position = []
	for position in range(0, len(x[0][:])):
		check_position.append(vector1[x[0][position]])
	return(check_position)

def MatrixCreation(n_trial, trial_time, vector):
	import csv
	import matplotlib.pyplot as plt
	import numpy as np
	import math
	import trovacsv
	import funzioni_pesi
	''' INIZIALIZZO I PARAMETRI '''
	global M
	j = 1
	i = 1
	P = []
	x = [] #matrice ausiliaria
	M = [] #matrice in cui inserisco il file csv
	O = [] #matrice ausiliaria
	N = [] #matrice ausiliaria
	P = []
	Aux = [] #matrice ausiliaria
	E_Matrix = [] #matrice finale di pesi e connessioni
	GID = 0
	GID_step = 1
	con_num = 1 #indica il numero della connessione
	riga = 0
	diverso = 0
	flag_while = 0
	row_aux = 0
	prova = 1
	prova_max = n_trial
	t_prova = trial_time
	n_prove = n_trial
	old_max_con = 0
	thr = 500
	PFPC = vector

	''' DEFINISCO LE FUNZIONI tic() E toc() PER MISURARE LA DURATA DI ESECUZIONE DELLO SCRIPT ''' 
	
	def tic():
		import time
		global startTime_for_tictoc
		startTime_for_tictoc = time.time()
	
	def toc():
		import time
		if 'startTime_for_tictoc' in globals ():
			print('Elapsed Time:' + str(time.time() - startTime_for_tictoc) + 's')
		else:
			print('tic() has not been defined')
	
	
	
	''' CREO LA MATRICE 'M' IN CUI METTERE I VALORI DEL FILE csv '''
	
	tic()
	
	
	M = funzioni_pesi.put_togheter(PFPC)	
	
	print('Matrix Created!')
	
	''' ORDINO LA MATRICE IN BASE AI GID_SENDER E SALVO LE POSIZIONI DEI DIVERSI GID_SENDERS IN UNA LISTA'''
	
	M = M[M[:,0].argsort()]
	
	last_gid = M[len(M) - 1, 0]
	first_gid = M[0,0]
	GID_position = np.zeros(last_gid)
	GID_position[0] = 0 #prima posizione e' in 0
	
	for i in range(int(first_gid) + 1, int(last_gid) + 1):
		
		x = np.nonzero(M[:,0]<i) # prendo sempre l'ultimo elemento quindi non mi interssa se in x finiscono delle 	posizioni che ho gia' selezionato
		GID_position[j] = x[0][len(x[0][:]) -1]
	
		if(GID_position[j]!= GID_position[j-1]): # evta di avere due o piu' volte lo indici in caso manchi un GID
			j = j + 1
		
	a = np.nonzero(GID_position > 0)
	GID_position = GID_position[:a[0][len(a[0][:])-1]+1]
	
	''' DIVIDO LA MATRICE M IN SOTTO MATRICI '''	
	
	
	while (GID <= len(GID_position)-1):
		
		
		if (GID == len(GID_position)-1):# se arrivo all'ultimo
			O=M[GID_position[GID] + 1:, :]
			
		if (GID != len(GID_position)-1): #se sono tra il primo e l'ultimo
			O = M[GID_position[GID] + 1:GID_position[GID+GID_step], :]
			
		if (GID != len(GID_position)-1 and flag_while == 0): # se sono al primo
			O = M[GID_position[GID]:GID_position[GID+GID_step], :]
		
		N = np.zeros((len(O), 3)) # inizializzo una matrice ausiliaria
		
	
		if(flag_while == 0): #entra solo al primo giro del ciclo while
			N[0,0] = con_num
			N[0,1] = O[0,2]
			N[0,2] = O[0,3]
		
		if(flag_while != 0): #entro dal secondo giro in poi, sono sicuro che le connessioni saranno diverse da 			prima perche' cambiano i GID_senders
			con_num = con_num + 1		
			N[0,0] = con_num #dato che so che le connessioni sono diverse il privo valore di N sara' una nuova 	connessione quindi aumento il contatore
			N[0,1] = O[0,2]
			N[0,2] = O[0,3]
			
	
		for riga in range(1, len(O[0:, 0])):
			for count in reversed(range(0, riga)):
				if(O[count, 0] == O[riga, 0] and O[count, 1] == O[riga, 1]): # se trovo una connessione 	uguale a quella in 'riga' entro
					N[riga, 0] = N[count, 0]
					N[riga, 1] = O[riga, 2]
					N[riga, 2] = O[riga, 3]
					diverso=0
					break #facendo cio' quando trovo l'uguaglianza esco dal ciclo for
				
				if(O[count, 0] != O[riga, 0] or O[count, 1] != O[riga, 1]): #se NON trovo una connessione 	uguale a quella in 'riga' entro
					diverso = diverso+1
	
				if(diverso == riga):  #se entro vuol dire che in nessuna riga precedente c'e' una 		connessione simile
					con_num = con_num+1
					N[riga, 0] = con_num
					N[riga, 1] = O[riga, 2]
					N[riga, 2] = O[riga, 3]
					diverso=0
					
		N = N[np.lexsort((N[:, 1], N[:, 0]))] #ordino N in base alle connessioni e al tempo in cui cambiano i pesi
		new_max_con = N[len(N) -1, 0]
		Aux = np.zeros((new_max_con - old_max_con, n_prove + 1)) #inizializzo una matrice ausiliaria
		count = 0
		
		#print(N)	
		for riga in range(1, len(N[:, 0])):
					
			flag_stop = 0
	
			if(prova < prova_max):
	
				count = count +1
				
				if(N[riga, 1] > prova * t_prova and N[riga, 1] != N[riga - 1, 1] ): 
					
					
					if(math.floor(N[riga, 1]/t_prova) > prova and N[riga, 0] == N[riga - 1, 0]): #
						
						col = math.floor(N[riga, 1]/t_prova)
						Aux[row_aux, 0] = N[riga - count, 0]
						for i in range(0, int(col) - int(prova) + 1):
							Aux[row_aux, prova + i] = N[riga - 1, 2]
						prova =  col + 1
						
					if(math.floor(N[riga, 1]/t_prova) == prova and N[riga, 0] == N[riga - 1, 0]):
						Aux[row_aux, 0] = N[riga - 1, 0]
						Aux[row_aux, prova] = N[riga - 1, 2]
						prova = prova + 1
	
					if(math.floor(N[riga, 1]/t_prova) == prova and N[riga, 0] != N[riga - 1, 0]):	#se non spara nella prima prova
						
						Aux[row_aux, 0] = N[riga, 0]
						Aux[row_aux, prova] = N[riga, 2]
						prova = prova +1
	
				if(N[riga, 1] == prova * t_prova and N[riga, 1] != N[riga - 1, 1]):
					Aux[row_aux, 0] = N[riga, 0]
					Aux[row_aux, prova] = N[riga, 2]
					prova = prova + 1
					
	
			if(prova < prova_max): #se all'utlima prova non spara
				if(riga != len(N[:, 0]) - 1):	
					if(N[riga + 1, 0] > N[riga, 0]):
						Aux[row_aux, 0] = N[riga, 0]
						col = math.floor(N[riga, 1]/t_prova)
						for i in range(0, prova_max - prova + 1):
							Aux[row_aux, prova + i] = N[riga, 2]
						prova = prova_max + 1
			
				if(riga == len(N[:, 0]) - 1 and math.floor(N[riga, 1]/t_prova) <= prova_max - 2 ): #prove e rapporti N[riga, 1]/t_prova) hanno una differenza di uno, quindi acccetto nek ciclo 						 
					Aux[row_aux, 0] = N[riga, 0]						  
					col = math.floor(N[riga, 1]/t_prova)
					for i in range(0, prova_max - prova + 1):
						Aux[row_aux, prova + i] = N[riga, 2]
					prova = prova_max + 1
				
	
					
			if(prova == prova_max):
			
				if(riga != len(N[:, 0]) - 1):
					num = math.floor(N[riga, 1]/t_prova) 
	
					if(N[riga + 1,1] < N[riga, 1] and num >= prova_max - 1):
						Aux[row_aux, 0] = N[riga, 0]
						Aux[row_aux, prova] = N[riga, 2]
						prova = prova + 1
														
				if(riga == len(N[:, 0]) - 1):
					Aux[row_aux, 0] = N[riga, 0]
					Aux[row_aux, prova] = N[riga, 2]
					prova = prova + 1
			
			
			if(prova >= prova_max + 1):
				
				count = 0
				prova = 1
				flag_stop = 1
				if(riga != len(N) - 1):  #controlli vari per evitare che una connessione dopo aver riempito tutte le sue colonne si 'espanda' alle righe successive
					if(N[riga + 1, 0] == Aux[row_aux, 0]):
						while(N[riga + 1, 0] == Aux[row_aux, 0]):
							riga = riga + 1
							if(riga == len(N) - 1):
														
								break
							
				row_aux = row_aux + 1
				
			if(Aux[len(Aux) - 1, 0] == new_max_con and flag_stop == 1):
				break	
				
				
		
		if(flag_while != 0):
			E_Matrix = np.concatenate((E_Matrix, Aux), axis=0)
			
		if(flag_while == 0):
			E_Matrix = Aux
		
		GID = GID + GID_step
		flag_while = flag_while + 1	
		old_max_con = N[len(N) -1, 0]
		row_aux = 0


	''' STAMPO MATRICE E_Matrix CHE CONTIENE I PESI DI INTERESSE CON IL RELATIVO NUMERO DI CONNESSIONE E IL TEMPO TOTALE DI ESECUZIONE DELLO SCRIPT '''
	
	return(E_Matrix)
	toc()



def insieme():
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

		time = input1.get()
		trial = input2.get()
		if not time or not trial:
			showerror("Parameters selection", "Please Insert some Values")
		if time and trial:
			Matrix = funzioni_pesi.MatrixCreation(int(trial), int(time), csv_vector)
			top = Toplevel(master)
			top.geometry('{}x{}'.format(350, 50))
			b = Button(top, text="Save as csv", command= saveMatrix)
			b.grid(row = 1, column = 0)
			b1 = Button(top, text="Plot Menu", command= cancel)
			b1.grid(row = 1, column = 1 )
			b2 = Button(top, text="Print Matrix", command= printer)
			b2.grid(row = 1, column = 2 )
			b3 = Button(top, text="Cancel", command= cancel)
			b3.grid(row = 1, column = 3 )

def plot(flag, M):
	import matplotlib as plt
	import math
	import numpy as np
	global input3
	global input4
	global input5
	global input6

	if(flag == 'RR'):
		bt = input3.get()
		et = iput4.get()
		bc = input5.get()
		ec = iput6.get()
		trial = np.arange(bt, et + 1)
		fig = plt.figure()
		row = 3
		col = math.ceil(ec/row)
		for i in range(bc, int(ec) + 1):
    			ax = fig.add_subplot(row,col, i - bc + 1)
    			ax.plot(trial, M[i - 1, bt:et])
   		 	ax.set_title('Connection Number' + str(i - 1))















