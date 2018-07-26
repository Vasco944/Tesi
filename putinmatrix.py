import csv
import matplotlib.pyplot as plt
import numpy as np

i=1
j=1
M=[]
GIDs=[]
GIDr=[]
S=-1
R=0
numeberS=100
numeberR=1000

with open("PESI.csv") as pesicsv:
	lettore=csv.reader(pesicsv, delimiter="\t")
	
	for row in lettore:
	
		if(i==1):			
			M=np.array([[int(row[0]), int(row[1]),float(row[3])]]) #salvo i valori di GIDsenders, GIDreceivers e Peso. 
									       #In quello di ALberto devo salvarmi anche il tempo per fare dei controlli
			
					
		if(i!=1):
			a=np.array([[int(row[0]), int(row[1]),float(row[3])]])
			M=np.concatenate((M,a), axis=0)
		i=i+1

print('Matrix with GID anweights Created!')
senders=M[0:,0]
receivers=M[0:,1]

senders.sort()
receivers.sort()

GIDs=np.zeros(len(senders))

GIDr=np.zeros(len(receivers))

GIDs[0]=senders[0]
GIDr[0]=receivers[0]

for count in range(1, len(GIDs)):
	if(senders[count]>senders[count-1]):
		GIDs[j]=senders[count]
		j=j+1
GID_S=np.delete(GIDs, range(j,len(GIDs)))
j=1
for count in range(1, len(GIDr)):
	if(receivers[count]>receivers[count-1]):
		GIDr[j]=receivers[count]
		j=j+1

GID_R=np.delete(GIDr, range(j,len(GIDr)))

print('GID array created!')
while(S<len(GID_S)):
	S=S+1
	riga=0
	count=0
	flag=0
	R=0
	print(S)
	while(R<len(GID_R)):
		#if(riga<107399):
		#print(R)
		if(M[riga, 0]==GID_S[S] and M[riga, 1]==GID_R[R]):
			W=M[riga, 2] #salvo il valore nel peso in questa variabile
		riga=riga+1
		if(riga==len(M[0:,0])-1):#all' ultima riga il valore in W e' l'ultimo assunto dalla connessione che ipotizzo rimanere uguale fino alla fine
			R=R+1
			riga=0
			if(flag!=0):
				b=np.array([W]) 
				Weights=np.concatenate((Weights, b), axis=0)
			if(flag==0):
				Weights=np.array([W])
				flag=flag+1

print(Weights)
				
			
			
		






























