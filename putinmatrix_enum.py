import csv
import matplotlib.pyplot as plt
import numpy as np
import math
import trovacsv
''' INIZIALIZZO I PARAMETRI '''

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
prova_max = 10
t_prova = 500
n_prove = 10
old_max_con = 0
thr = 500
PFPC = trovacsv.result

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


for pos in range(0, len(PFPC)):

	with open(PFPC[pos]) as pesicsv:
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

print('Matrix Created!')

''' ORDINO LA MATRICE IN BASE AI GID_SENDER E SALVO LE POSIZIONI DEI DIVERSI GID_SENDERS IN UNA LISTA'''

M = M[M[:,0].argsort()]

last_gid = M[len(M) - 1, 0]
first_gid = M[0,0]
GID_position = np.zeros(last_gid)
GID_position[0] = 0 #prima posizione e' in 0

for i in range(int(first_gid) + 1, int(last_gid) + 1):
	
	x = np.nonzero(M[:,0]<i) # prendo sempre l'ultimo elemento quindi non mi interssa se in x finiscono delle posizioni che ho gia' selezionato
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
	
	if(flag_while != 0): #entro dal secondo giro in poi, sono sicuro che le connessioni saranno diverse da prima perche' cambiano i GID_senders
		con_num = con_num + 1		
		N[0,0] = con_num #dato che so che le connessioni sono diverse il privo valore di N sara' una nuova connessione quindi aumento il contatore
		N[0,1] = O[0,2]
		N[0,2] = O[0,3]
		

	for riga in range(1, len(O[0:, 0])):
		for count in reversed(range(0, riga)):
			if(O[count, 0] == O[riga, 0] and O[count, 1] == O[riga, 1]): # se trovo una connessione uguale a quella in 'riga' entro
				N[riga, 0] = N[count, 0]
				N[riga, 1] = O[riga, 2]
				N[riga, 2] = O[riga, 3]
				diverso=0
				break #facendo cio' quando trovo l'uguaglianza esco dal ciclo for
			
			if(O[count, 0] != O[riga, 0] or O[count, 1] != O[riga, 1]): #se NON trovo una connessione uguale a quella in 'riga' entro
				diverso = diverso+1

			if(diverso == riga):  #se entro vuol dire che in nessuna riga precedente c'e' una connessione simile
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
			
			if(N[riga, 1] > prova * t_prova and N[riga, 1] != N[riga - 1, 1] ): # > prova * t_prova, quando si usera' un file con piu' prove avra' piu' senso questa divisione di > e == 
				
				
				if(math.floor(N[riga, 1]/t_prova) > prova and N[riga, 0] == N[riga - 1, 0]): #
					#print(N[riga - 1, :])
					#print(N[riga, :])
					col = math.floor(N[riga, 1]/t_prova)
					Aux[row_aux, 0] = N[riga - count, 0]
					Aux[row_aux, prova] = N[riga - 1, 2]
					#Aux[row_aux, col] = N[riga, 2]
					Aux[row_aux, prova + 1] = N[riga - 1, 2]
					prova =  col + 1
					
				if(math.floor(N[riga, 1]/t_prova) == prova and N[riga, 0] == N[riga - 1, 0]):
					Aux[row_aux, 0] = N[riga - 1, 0]
					Aux[row_aux, prova] = N[riga - 1, 2]
					prova = prova + 1

				if(math.floor(N[riga, 1]/t_prova) == prova and N[riga, 0] != N[riga - 1, 0]):	#se non spara nella prima prova
					#print(N[riga - 1, :])
					#print(N[riga, :])
					Aux[row_aux, 0] = N[riga, 0]
					Aux[row_aux, prova] = N[riga, 2]
					prova = prova +1

			if(N[riga, 1] == prova * t_prova and N[riga, 1] != N[riga - 1, 1]):
				Aux[row_aux, 0] = N[riga, 0]
				Aux[row_aux, prova] = N[riga, 2]
				prova = prova + 1
				

		if(prova < prova_max): #se all'utlima prova non spara
			if(riga != len(N[:, 0]) - 1):	
				if(N[riga + 1, 1] < N[riga, 1]):
					#print(N[riga + 1, :])
					#print(N[riga, :])
					Aux[row_aux, 0] = N[riga, 0]
					Aux[row_aux, prova] = N[riga, 2]
					Aux[row_aux, prova + 1] = Aux[row_aux, prova]
					prova = prova_max + 1
			if(riga == len(N[:, 0]) - 1 and math.floor(N[riga, 1]/t_prova) <= prova_max - 2 ):
				Aux[row_aux, 0] = N[riga, 0]
				Aux[row_aux, prova] = N[riga, 2]
				Aux[row_aux, prova + 1] = Aux[row_aux, prova]
				prova = prova_max + 1
	
		if(prova == prova_max):
		
			if(riga != len(N[:, 0]) - 1):
				num = math.floor(N[riga, 1]/t_prova) 

				if(N[riga + 1, 1] < N[riga, 1] and num >= prova_max - 1):
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

np.set_printoptions(threshold = 'nan')
print(E_Matrix[1000:1200, :])


toc()



''' PLOT DI VARIA NATURA E GENERE '''

trials = np.arange(1, 11)

plt.subplot(1, 3, 1)
plt.title('Connection 10')
plt.plot(trials, E_Matrix[10, 1:])
plt.xlabel('Trials')
plt.ylabel('Weight Values')

plt.subplot(1, 3, 2)
plt.title('Connection 160')
plt.plot(trials, E_Matrix[160, 1:])
plt.xlabel('Trials')
plt.ylabel('Weight Values')

plt.subplot(1, 3, 3)
plt.title('Connection 310')
plt.plot(trials, E_Matrix[210, 1:])
plt.xlabel('Trials')
plt.ylabel('Weight Values')

plt.show()

