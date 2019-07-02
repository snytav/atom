import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import statistics
import numpy.ma as ma
import reader as rd
import impulses as imp

def findSinFunction(field) :
	#DETERMINIG AMPLITUDE
	amplitude = max(np.abs(field))


	#DETERMINIG ANGULAR FREQUENCY
	# computing fourier transform
	fourier = np.fft.fft(field)

	# computing frequencies fourier transform
	freq = np.fft.fftfreq(len(field))

	#Getting real part of Fourrier transformed field
	realFourrier = np.real(fourier)

	#Searching for the fundamental frequency
	tmpAF = max(realFourrier)
	frequence = 0
	for i in range(len(realFourrier)) :
		if (realFourrier[i] > 0.9*tmpAF) :
			if (freq[i] > 0) :
				frequence = freq[i]

	angularFrequence = frequence*2*np.pi


	#DETERMINING PHASE
	phase = 0

	return (amplitude, angularFrequence, phase)


def sinusoidal(x, amplitude, angularFreq, phase) :
	return amplitude*np.sin(angularFreq*x + phase)


#Displays the value of the Electric field following x axis
def displayField(field, y, z) : #field[102][6][6]
	abscissa = np.arange(0, len(field), 1)
	axis = [] + [field[i][y][z] for i in range(len(field))] #Convert matrix[x][y][z] to list[102]

	plt.plot(abscissa, axis, markersize=0.2, color='red')

	#Finding the parameters of the sine function that describes the field
	(amplitude, angularFreq, phase) = findSinFunction(axis)

	print("Amplitude", amplitude, "- Angular Frequence", angularFreq, "- Phase", phase)

	#Applying the function to compare with the data
	fSin = sinusoidal(abscissa, amplitude, angularFreq, phase)

	plt.plot(abscissa, fSin, markersize=0.1, color='green')


#Initializes arguments and launch display_impulses function
def runField(files, sorts=[0], y=3, z=2) :
	#sort = [0/1/2/3] <=> Electric, Magnetic, Currant or HalfStep Electric
	fields = ["Electric", "Magnetic", "Currant", "HalfStep Magnetic"]

	for file in files :

		#load data
		data = rd.readFields(file) #data[12][102][6][6]
		figures = []
		for sort in sorts :
			figures += [plt.figure()]
			plt.xlabel('Position')
			yLab = fields[sort] + " Field x"
			plt.ylabel(yLab)
			field = data[sort*4] #field[102][6][6]
			displayField(field, y, z)

	plt.show()