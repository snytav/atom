from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import statistics
import sys
import struct
import netCDF4
import numpy.ma as ma
import reader as rd
import impulses as imp

def findSinFunction(field) :
	amplitude = max(np.abs(field))
	angularFreq = 1
	phase = 0

	#DETERMINING ANGULAR FREQUENCE
	AmplHistory = [[], []] #[[Positions], [Values]] of the points close to the amplitude
	amplAdmitance = 0.9*amplitude #How close a point should be to be considered as amplitude

	print("field : ", len(field))

	for i in range(len(field)) :
		if (np.abs(field[i]) > amplAdmitance) :
			AmplHistory[0] += [i]
			AmplHistory[1] += [field[i]]

	#print("AmplHistory : ", AmplHistory)

	halfSymbolGap = [(AmplHistory[0][i+1]-AmplHistory[0][i]) for i in range(len(AmplHistory[0]) - 1)]

	print("halfSymbolGap : ", halfSymbolGap)
	print("halfSymbolGap mean : ", statistics.mean(halfSymbolGap))

	cleanGap = []
	m = statistics.mean(halfSymbolGap)
	for i in range(len(halfSymbolGap)) :
		if (halfSymbolGap[i] > m) :
			cleanGap += [halfSymbolGap[i]]

	print("cleanGap : ", cleanGap)
	print("cleanGap mean : ", statistics.mean(cleanGap))

	angularFreq = np.pi/statistics.mean(cleanGap)

	#DETERMINING PHASE

	return (amplitude, angularFreq, phase)


def sinusoidal(x, amplitude, angularFreq, phase) :
	return amplitude*np.sin(angularFreq*x + phase)


#Displays the value of the Electric field following x axis
def displayField(field, y, z) : #field[102][6][6]
	abscissa = np.arange(0, len(field), 1)
	# axis = [] + [field[i][y][z] for i in range(len(field))] #Convert matrix[x][y][z] to list[102]
	axis = [] + field 

	plt.plot(abscissa, axis, markersize=0.2, color='red')

	#Finding the parameters of the sine function that describes the field
	(amplitude, angularFreq, phase) = findSinFunction(axis)

	print("Amplitude", amplitude, "- Angular Frequence", angularFreq, "- Phase", phase)

	#Applying the function to compare with the data
	fSin = sinusoidal(abscissa, amplitude, angularFreq, phase)

	plt.plot(abscissa, fSin, markersize=0.1, color='green')


#Initializes arguments and launch display_impulses function
def runElecField(file) :
	#load data
	# data = rd.readFields(file) #data[12][102][6][6]
	# print("data length : ", len(data))
	# print("data[0] length : ", len(data[0]))
	# print("data[0][0] length : ", len(data[0][0]))

	sort = 0
	axis = 0
	y = 3
	z = 2

	amplitude = 4
	angularFrequence = 5
	phase = 0

	print("real angular frequence : ", aF)
	#field = data[sort*4+axis] #field[102][6][6]
	field = [sinusoidal(i, amplitude, angularFrequence, phase) for i in range(102)]

	displayField(field, y, z)

	plt.xlabel('Position')
	plt.ylabel('Electric Field x')
	plt.show()