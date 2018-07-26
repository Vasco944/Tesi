def put_togheter(vector):
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


def ordina(matrix):
	import numpy as np
	matrix = matrix[matrix[:,0].argsort()]
	return(matrix)

