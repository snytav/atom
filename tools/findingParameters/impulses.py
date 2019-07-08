import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import statistics
import numpy.ma as ma
import os
import multiprocessing as mp
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


#Send the variance to the output
def partMean(impulses, output) :
	var = statistics.mean(impulses) #compute variance
	output.put(var)


#Send the variance to the output
def partVariance(impulses, output) :
	var = statistics.variance(impulses) #compute variance
	output.put(var)


#Return the combination of all the variances
def groupVar(variances, tasks) :
	var = 0

	for i in range(len(variances)) :
		var += variances[i]*(tasks[i+1]-tasks[i])

	return (var/(tasks[-1]))

#Displays the number of particles in each impulses-category of width delta
def displayImpulse(impulses, velocity, categories, sort, coordinate, options) :
	[showMean, showVariance, showCurve] = options

	axis = ['x', 'y', 'z']

	if (showMean) :
		#determine yAxis max which corresponds to the impulse category containing the more particles
		amplitude = max(categories) - min(categories)

		# Define an output queue
		output = mp.Queue()

		#Determining the repartition oftasks betweens processes
		nbCPU = mp.cpu_count()
		nbTasks = len(impulses)//nbCPU
		tasks = [0] + [nbTasks*i for i in range(1,nbCPU+1)]
		tasks[-1] = len(impulses)

		# Setup a list of processes that we want to run
		processes = [mp.Process(target=partMean, args=(impulses[tasks[i]: tasks[i+1]], output)) for i in range(nbCPU)]

		# Run processes
		for p in processes:
		    p.start()

		# Exit the completed processes
		for p in processes:
		    p.join()

		# Get process results from the output queue
		mean = statistics.mean([output.get() for p in processes])
		print("Mean for Sort " + str(sort+1) + " - " + axis[coordinate-1] + " axis : " + str(mean)) #print mean

		#Displays Mean
		plt.axvline(x = mean, markersize=0.1, color="green")
		plt.text(x = mean, y=0.75*amplitude, s="m:"+str(mean), verticalalignment='center', color="green")

	if (showVariance) :
		# Define an output queue
		output = mp.Queue()

		#Determining the repartition oftasks betweens processes
		nbCPU = mp.cpu_count()
		nbTasks = len(impulses)//nbCPU
		tasks = [0] + [nbTasks*i for i in range(1,nbCPU+1)]
		tasks[-1] = len(impulses)

		# Setup a list of processes that we want to run
		processes = [mp.Process(target=partVariance, args=(impulses[tasks[i]: tasks[i+1]], output)) for i in range(nbCPU)]

		# Run processes
		for p in processes:
		    p.start()

		# Exit the completed processes
		for p in processes:
		    p.join()

		# Get process results from the output queue
		variance = groupVar([output.get() for p in processes], tasks)
		
		print("Variance for Sort " + str(sort+1) + " - " + axis[coordinate-1] + " axis : " + str(variance)) #print variance 
		
		#Displays Variance
		plt.text(x = mean, y=0.7*amplitude, s="v:"+str(variance), verticalalignment='center', color="green")

	if (showCurve) :
		#Display the function followed by the impulses
		fImpulses = norm(velocity, amplitude, mean, variance)
		label = "sort " + str(sort+1) + " - axis " + str(coordinate+1) 
		plt.plot(velocity, fImpulses, markersize=0.1, label=label, color="green")
		#plt.legend()

	#Display the Impulses classified by categories
	plt.plot(velocity, categories, 'ro', markersize=0.2)
	

#Calculates all that is needed to display the impulses
def prepareDisplay(files, sort, ax, options, delta=0.0001) :
	axis = ["x", "y", "z"]
	sep = options[0]
	for file in files :
		#load data
		impulses = rd.readImpulse(file, sort, ax)

		#Getting bounds of Impulses
		minim = min(impulses)
		maxim = max(impulses)

		#Number of impulse categories
		#Represents the number of dots on the xAxis
		size = int((maxim - minim)//delta) + 1 

		#Array representing the categories of impulses (X axis)
		velocity = np.arange(minim, maxim, delta)

		#Array containing the number of particles in each categories
		categories = categorize(impulses, size, minim, delta)

		if sep :
			name = file + " : sort " + str(sort+1) + " - axis " + axis[ax] 
			plt.figure(name)

		displayImpulse(impulses, velocity, categories, sort, ax, options[1:])


#displays the impulses in the right order
#depending on the sort, the axis and the file
def orderTasks(filesPaths, sorts, axis, options) :
	axisName = ["x", "y", "z"]

	for sort in range(len(sorts)) :
		if (sorts[sort]) :

			for ax in range(len(axis)) :
				if (axis[ax]) :
					if (not options[0]) :
						name = "Sort " + str(sort+1) + " - Axis " + axisName[ax]
						plt.figure(name)

					prepareDisplay(filesPaths, sort, ax, options)
	plt.show()