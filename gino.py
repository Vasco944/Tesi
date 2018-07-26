import csv
import matplotlib.pyplot as plt
import numpy as np

## INIZIALIZZO I PARAMETRI ##

j = 1
i = 1
x = []
M = [] #matrice in cui inserisco il file csv
O = [] 
N = []
E_Matrix = []
GID = 0
GID_step = 1
con_num = 1 #indica il numero della connessione
riga = 0
diverso = 0
flag_while = 0
## CREO LA MATRICE 'M' IN CUI METTERE I VALORI DEL FILE CSV ##

with open("PESI.csv") as pesicsv:
	lettore=csv.reader(pesicsv, delimiter="\t")
	
	for row in lettore:
	
		if(i == 1):			
			M = np.array([[int(row[0]), int(row[1]),float(row[2]), float(row[3])]]) 
			
					
		if(i != 1):
			a = np.array([[int(row[0]), int(row[1]),float(row[2]), float(row[3])]])
			M = np.concatenate((M,a), axis=0)
		i=i+1


print('Matrix Created!')

## ORDINO LA MATRICE IN BASE AI GID_SENDERS ##

M = M[M[:,0].argsort()]

GID_position = np.zeros(10)
GID_position[0] = 0
print(M[:, 0])
for i in range(2, 11):
	
	x=np.nonzero(M[:,0]<=i) # prendo sempre l'ultimo elemento quindi non mi interssa se in x finiscono delle pposizioni che ho gia' selezionato
	GID_position[j]=x[0][len(x[0][:]) -1]

	if(GID_position[j]!= GID_position[j-1]): # evta di avere due o piu' volte lo indici in caso manchi un GID
		j=j+1
	
a=np.nonzero(GID_position > 0)

GID_position = GID_position[:a[0][len(a[0][:])+1] 

	'''

#while (GID <= len(GID_position)-1)
#
#	if (GID == len(GID_position)-1):
#		O = M[GID_position(GID):len(M[:, 0])-1, :]
#
#	if (GID != len(GID_position)-1):else
#		O = M[GID_position(GID):GID_position(GID+GID_step)-1, :]
#	
#	N = np.zeros((len(O), 3))
#	
#	if(flag_while == 0):
#		N[0,0] = con_num
#		N[0,1] = O[0,2]
#		N[0,2] = O[0,3]
#	
#	if(flag_while != 0):
#		if(O[0,0] == pr_sender and O[0, 1] == pr_receiver):
#			N[0,0] = E_Matrix[riga,0]
#			N[0,1] = E_Matrix[riga,1]
#			N[0,2] = E_Matrix[riga,2]
#
#	for riga in range(1, len(O[0:, 0])):
#		for count in reversed(range(0, riga)):
#			if(O[count, 0] == O[riga, 0] and O[count, 1] == O[riga, 1]): # se trovo una connessione uguale a quella in 'riga' entro
#				N[riga, 0] = N[count, 0]
#				N[riga, 1] = O[riga, 2]
#				N[riga, 2] = O[riga, 3]
#				diverso=0
#				count = len(M[0:, 0])-1 #facendo cio' quando trovo l'uguaglianza esco dal ciclo for
#			
#			if(O[count, 0] != O[riga, 0] or O[count, 1]!= O[riga, 1]): #se NON trovo una connessione uguale a quella in 'riga' entro
#				diverso = diverso+1
#	
#			if(diverso == riga):  #se entro vuol dire che in nessuna riga precedente c'e' una connessione simile
#				con_num = con_num+1
#				N[riga, 0] = con_num
#				N[riga, 1] = O[riga, 2]
#				N[riga, 2] = O[riga, 3]
#				diverso=0
#		
#	if(flag_enum == 0):
#		E_Matrix = N
#
#	if(flag_enum != 0):
#		E_Matrix = np.concatenate((E_Matrix, N), axis=0)
#	
#	GID = GID+GID_step
#	flag_while = flag_while + 1	
#	flag_enum = flag_enum + 1
#	pr_sender = O[riga, 0]
#	pr_receiver = O[riga, 1]
#	

	
#print(E_Matrix)
	
	
	'''
#print('Connections Enumerated!')

#print(GID_position)
#print(len(M[:, 0]))
## ORDINO LA MATRICE 'N' ##

