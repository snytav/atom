import numpy as np
import matplotlib.pyplot as plt
import sys
import statistics as st


import PyGnuplot as gp
import reader as rd

def displayParticles1D(coordinates, impulses, sort, coordinate, dataPath, color=0) :
	#Colors of the curve
	curvCol = [['red', '#e136ec'], ['blue', '#36b9ec'], ['green', '#86ec36']]
	axis = ['x', 'y', 'z']

	#Initialise pyplot figure
	title = "Sort " + str(sort) + " - Axis " + str(axis[coordinate-1])
	plt.title(title)
	ylabel = "impulse " + str(axis[coordinate - 1])
	plt.ylabel(ylabel)
	xlabel = str(axis[coordinate - 1])
	plt.xlabel(xlabel)

	#Drawing the value of the impulse for each particle
	plt.plot(coordinates, impulses, 'ro', markersize=0.2, label="", color=curvCol[color%len(curvCol)][1])

def displayNodes1D(coordinates, impulses, sort, coordinate, dataPath, color = 0) :
	curvCol = [['red', '#e136ec'], ['blue', '#36b9ec'], ['green', '#86ec36']]
	axis = ['x', 'y', 'z']

	#Initialise pyplot figure
	title = "Sort " + str(sort) + " - Axis " + str(axis[coordinate-1])
	plt.title(title)
	ylabel = "impulse " + str(axis[coordinate - 1])
	plt.ylabel(ylabel)
	xlabel = str(axis[coordinate - 1])
	plt.xlabel(xlabel)

	#size of the gap between 2 nodes
	hx = 1.255/100

	#Array containing the impulse associated to each node of the grid
	nodesImpulse = [0 for i in range(102)]
	#Aray containing the number of particles associated to each node of the grid
	nodesNumber = [0 for i in range(102)] #x-axis
	for i in range(len(impulses)) :
		nodesImpulse[int(round(coordinates[i]/hx))] += impulses[i]
		nodesNumber[int(round(coordinates[i]/hx))] += 1

	#Avoiding divisions by zero
	for i in range(len(nodesNumber)) :
		if (nodesNumber[i] == 0) :
			nodesNumber[i] = 1

	#each node receive the mean impulse among all the particle associated to it
	for i in range(len(nodesImpulse)) :
		nodesImpulse[i] /= nodesNumber[i]

	#Drawing the impulse value for each node of the grid
	plt.plot(np.arange(102), nodesImpulse, 'ro', markersize=1, label="", color=curvCol[color%len(curvCol)][1])


#Generates a gnuplot file to be displayed using the commands :
#gnuplot
#scale = ?     --  (5000000/100/10) with respect to te sort of particle
#plot 'filePath' u 1:2:($3*scale):($4*scale) with vectors
def gnuplotFile(coordinates, impulses, sort, coordinate, dataPath, color = 0) :
	axis = ['x', 'y', 'z']

	#Creating new file
	name = str(sort) + "_" + str(axis[coordinate[0]]) + "-" + str(axis[coordinate[1]]) + "_" + dataPath[-13:-3] + ".txt"
	file = open(name, "w")

	#variables to copy in the file
	x = ""
	y = ""
	vx = ""
	vy = ""

	#gap between 2 nodes of the grid
	hx = 1.255/100
	hy = 1.255/100

	#sum of impulses squarred among the particles 
	px = 0
	py = 0
	pz = 0

	#displaying 1 particle out of 1000 to be able to display vectors
	for i in range(0,len(coordinates[0]), 1000) :
		#summing squarred impulses
		px += impulses[0][i]**2
		py += impulses[1][i]**2
		pz += impulses[2][i]**2

		#gettings values to write
		x = str(coordinates[0][i]/hx)
		y = str(coordinates[1][i]/hy)
		vx = str(impulses[0][i])
		vy = str(impulses[1][i])

		#writting values in the file
		line = x + " " + y + " " + vx + " " + vy + "\n"
		file.write(line)
	
	file.close()

	print("px :", px)
	print("py :", py)
	print("pz :", pz)


def run2D(dataPath, ax) :
	#Reading data
	dataSet = rd.readFile(dataPath)

	axis = [True, False, False]
	sorts = [True, True, True]

	for sort in range(len(sorts)) :

		#Loading x-axis values
		coordinate = [0] #Values of the coordinates of the particles
		coordinates = [dataSet[sort+1][1][0]] #Values of the impulses of the particles
		impulses = [dataSet[sort+1][1][3]] #Axis to display

		#Loading y-axis values
		if (ax == "y") :
			coordinate += [1]
			coordinates += [dataSet[sort+1][1][1]]
			impulses += [dataSet[sort+1][1][4]]
		elif (ax == "z") :
			coordinate += [2]
			coordinates += [dataSet[sort+1][1][2]]
			impulses += [dataSet[sort+1][1][5]]


		# coordinates = [] #Values of the coordinates of the particles
		# impulses = [] #Values of the impulses of the particles
		# coordinate = []#Axis to display

		# for ax in range(len(axis)) :
		# 	if (axis[ax]) :
		# 		coordinate += [ax]
		# 		coordinates += [dataSet[sort+1][1][ax]]
		# 		impulses += [dataSet[sort+1][1][2 + (ax+1)]]

		impulses += [dataSet[sort+1][1][5]] #REMOVE !!
		gnuplotFile(coordinates, impulses, sort, coordinate, dataPath)

def run1D(dataPath, ax, nodes) :
	#Reading data
	dataSet = rd.readFile(dataPath)#readImpulses(dataPath, sorts, axis)

	axis = [False, False, False]
	sorts = [True, True, True]

	if (ax == "x") :
		axis[0] = True
	elif (ax == "y") :
		axis[1] = True
	elif (ax == "z") :
		axis[2] = True
	elif (ax == "all") :
		axis = [True, True, True]

	#display every axis selected
	for ax in range(len(axis)) :
		if (axis[ax]) :
			#display each sorts selected
			for sort in range(len(sorts)) :
				if (sorts[sort]) :
					#Initializing pyplot figure
					f = plt.figure()
					f.suptitle(dataPath[-13:])

					#Getting data to display
					coordinates = dataSet[sort+1][1][ax]
					impulses = dataSet[sort+1][1][2 + (ax+1)]

					if (nodes) :
						displayNodes1D(coordinates, impulses, sort, (ax+1), dataPath)
					else :
						displayParticles1D(coordinates, impulses, sort, (ax+1), dataPath)

	plt.show()


def showHelp() :
	print("1D :")
	print("\tIn order to display impulses of all particles : (choosing an axis)")
	print("\tpython3 displayImpulses.py 1D -p x/y/z/all inputFile\n")
	print("\tIn order to display a mean impulse for each node : (choosing an axis)")
	print("\tpython3 displayImpulses.py 1D -n x/y/z/all inputFile\n")
	print("2D :")
	print("\tIn order to produce a file to display with gnuplot :")
	print("\tpython3 displayImpulses.py 2D y/z inputFile\n")


def main() :
	if (len(sys.argv) == 1) :
		print("To display help, type :\npython3 main.py -h")
	else :
		if (sys.argv[1] == "1D") :
			if (sys.argv[2] == "-p") :
				run1D(sys.argv[4], sys.argv[3], False)
			elif (sys.argv[2] == "-n") :
				run1D(sys.argv[4], sys.argv[3], True)
		elif (sys.argv[1] == "2D") :
			run2D(sys.argv[3], sys.argv[2])
		elif (sys.argv[1] == "-h") :
			showHelp()

main()