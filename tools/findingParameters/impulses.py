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

#Normal Law
def norm(x, amplitude, mean, variance) :
	return (amplitude*np.exp(-(x-mean)**2/(2*variance)))


#Returns an array classifying particles by growing categories of impulse
#example : categories[n] counts the number of particles with an impulse in [minim+n*delta, minim+(n+1)*delta]
def categorize(impulses, size, minim, delta) :
	categories = [0 for i in range(size)]
	for x in impulses : 
		categories[int((x - minim)//delta)] += 1
	return categories


#displays the impulses by categories of width delta
#particle sorts : 1, 2 or 3
#coordinate : x=1, y=2, z=3
def display_impulses(impulses, sort, coordinate, showMean=False, showVariance=False, showCurve=False, delta=0.0001) :
	#Getting bounds of Impulses
	minim = min(impulses)
	maxim = max(impulses)

	#Number of impulse categories
	#Represents the number of dots on the xAxis
	size = int((maxim - minim)//delta) + 1 

	#Arrays containing the categories of impulses for X axis
	velocity = np.arange(minim, maxim, delta)

	#Values for Y axis
	categories = categorize(impulses, size, minim, delta)

	#determine yAxis max which corresponds to the impulse category containing the more particles
	amplitude = max(categories) - min(categories)

	#Colors of the curve
	curvCol = [['red', '#e136ec'], ['blue', '#36b9ec'], ['green', '#86ec36']]
	axis = ['x', 'y', 'z']

	#Show Mean
	mean = statistics.mean(impulses) #compute the mean
	print("Mean for Sort " + str(sort) + " - " + axis[coordinate-1] + " axis : " + str(mean)) #print the mean

	#displays the mean
	if (showMean) :
		plt.axvline(x = mean, color=curvCol[sort-1][0], markersize=0.1)
		plt.text(x = mean, y=0.75*amplitude, s="m:"+str(mean), verticalalignment='center', color=curvCol[sort-1][0])

	#Show Variance
	variance = statistics.variance(impulses) #compute variance
	print("Variance for Sort " + str(sort) + " - " + axis[coordinate-1] + " axis : " + str(variance)) #print 
	if (showVariance) :
		plt.text(x = mean, y=0.7*amplitude, s="v:"+str(variance), verticalalignment='center', color=curvCol[sort-1][0])

	#Display the Impulses classified by categories
	plt.plot(velocity, categories, 'ro', markersize=0.2, color=curvCol[sort-1][0])

	#Display the function followed by the impulses
	if (showCurve) :
		fImpulses = norm(velocity, amplitude, mean, variance)
		plt.plot(velocity, fImpulses, markersize=0.1, color=curvCol[sort-1][1])


#Initializes arguments and launch display_impulses function
def runImpulse(dataPath, sorts= [False, True, True], axis= [True, False, False]) :

	#Display curves separetely or compare them 
	separatedFiles = False
	#Display axis separetely
	separatedAxis = True

	dataSet = []

	if (separatedAxis) :
		#load all dataSets
		for dp in range(len(dataPath)) :
			dataSet += [rd.readFile(dataPath[dp], sorts, axis)]
			#dataSet += [rd.readAllFile(dataPath[dp])]

			#display each axis selected
			for ax in range(len(axis)) :
				if (axis[ax]) :
					plt.figure("Sort - Axis")

					#display each sorts selected
					for sort in range(len(sorts)) :
						if (sorts[sort]) :

							#display from all files
							for ds in range(len(dataSet)) :
								impulsesSortAxis = dataSet[ds][sort+1][1][2 + (ax+1)]
								display_impulses(impulsesSortAxis, sort+1, (ax+1), showCurve=True)
	else :
		for dp in dataPath :
			#load data
			dataSet = rd.readFile(dp)

			if (separatedFiles) :
				plt.figure("Sort - Axis")

			#display each sort selected
			for sort in range(len(sorts)) :
				if (sorts[sort]) :

					#display each axis selected
					for ax in range(len(axis)) :
						if (axis[ax]) :
							#values on the 'ax+1' axis of impulses for sort 'sort+1'
							impulsesSortAxis = dataSet[sort+1][1][2 + (ax+1)]
							display_impulses(impulsesSortAxis, sort+1, (ax+1))

	plt.xlabel('Impulse')
	plt.ylabel('Number of Particles')
	plt.show()