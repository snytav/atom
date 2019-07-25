import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import statistics as st
from mayavi.mlab import *
from mayavi import mlab
import reader as rd


def impulseToSpeed(impulses) :
	speed = [[], [], []]
	for i in range(len(impulses[0])) :
		gamma = (impulses[0][i]**2 + impulses[1][i]**2 + impulses[2][i]**2 )**0.5
		speed[0] += [impulses[0][i] / gamma]   #!!!! ABS ??
		speed[1] += [impulses[1][i] / gamma]   #!!!! ABS ??
		speed[2] += [impulses[2][i] / gamma]   #!!!! ABS ??
	return speed


#Display the impulse of each particles for each sorts
def displayParticles1D(coordinates, impulses, sort, coordinate, dataPath) :
	axis = ['x', 'y', 'z']

	#Initialise pyplot figure
	title = "Sort " + str(sort) + " - Axis " + str(axis[coordinate-1])
	plt.title(title)
	ylabel = "impulse " + str(axis[coordinate - 1])
	plt.ylabel(ylabel)
	xlabel = str(axis[coordinate - 1])
	plt.xlabel(xlabel)

	#Drawing the value of the impulse for each particle
	plt.plot(coordinates, impulses, 'ro', markersize=0.2)


#Calculates & Displays the impulse of each node following one axis for each sorts
def displayNodes1D(coordinates, impulses, sort, coordinate, dataPath) :
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

	#CALCULATING THE IMPULSE OF EACH NODE
	#Array containing the impulse associated to each node of the grid
	nodesImpulse = [0 for i in range(102)]
	#Aray containing the number of particles associated to each node of the grid
	nodesNumber = [0 for i in range(102)] #x-axis
	for i in range(len(impulses)) :
		index = int(round(coordinates[i]/hx))
		nodesImpulse[index] += impulses[i]
		nodesNumber[index] += 1

	#each node receive the mean impulse among all the particle associated to it
	for i in range(len(nodesImpulse)) :
		#Avoiding divisions by zero
		if (nodesNumber[i] == 0) :
			nodesNumber[i] = 1
		nodesImpulse[i] /= nodesNumber[i]

	#Drawing the impulse value for each node of the grid
	plt.plot(np.arange(102), nodesImpulse, 'ro', markersize=1)


def run1D(dataPath, ax, nodes, speed) :
	#Reading data
	dataSet = rd.readFile(dataPath)

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

					if (speed) :
						impulses = dataSet[sort+1][1][3:]
						impulses = impulsesToSpeed(impulses)[ax]
					else :
						impulses = dataSet[sort+1][1][2 + (ax+1)]

					if (nodes) :
						displayNodes1D(coordinates, impulses, sort, (ax+1), dataPath)
					else :
						displayParticles1D(coordinates, impulses, sort, (ax+1), dataPath)

	plt.show()


#Generates a gnuplot file to be displayed using the commands :
#gnuplot
#scale = ?     --  (5000000/100/10) with respect to te sort of particle
#plot 'filePath' u 1:2:($3*scale):($4*scale) with vectors
def gnuplotFile(coordinates, impulses, sort, coordinate, dataPath) :
	axis = ['x', 'y', 'z']

	#Creating new file
	name = str(sort) + "_" + str(axis[coordinate[0]]) + "-" + str(axis[coordinate[1]]) + "_" + dataPath[-13:-3] + ".txt"
	file = open(name, "w")

	#variables to copy in the file
	x = ""
	y = ""
	vx = ""
	vy = ""

	# Gap between 2 nodes of the grid
	h = 1.255/100

	# Sum of impulses squarred among the particles 
	px = 0
	py = 0
	#pz = 0

	# Displaying 1 particle out of 1000 to be able to display vectors
	for i in range(0,len(coordinates[0]), 1000) :
		# Summing squarred impulses
		px += impulses[0][i]**2
		py += impulses[1][i]**2
		#pz += impulses[2][i]**2

		# Gettings values to write
		x = str(coordinates[0][i]/h)
		y = str(coordinates[1][i]/h)
		vx = str(impulses[0][i])
		vy = str(impulses[1][i])

		# Writting values in the file
		line = x + " " + y + " " + vx + " " + vy + "\n"
		file.write(line)
	
	file.close()

	print("Sort", sort, ":")
	print("px :", px)
	print("py :", py)
	#print("pz :", pz, "\n")


def run2D(dataPath, ax, speed) :
	sorts = [True, True, True]

	for sort in range(len(sorts)) :

		#Loading x-axis values
		coordinate = [0] #Values of the coordinates of the particles
		[coordinates, impulses] = rd.readCoorImp(dataPath, sort)

		if (speed) :
			impulses = impulseToSpeed(impulses)

		#Loading y-axis values
		if (ax == "y") :
			coordinate += [1]
			tmp = rd.readCoorImp(dataPath, 1)
			coordinates += [tmp[0]]
			impulses += [tmp[1]]

		elif (ax == "z") :
			coordinate += [2]
			tmp = rd.readCoorImp(dataPath, 2)
			coordinates += [tmp[0]]
			impulses += [tmp[1]]

		gnuplotFile(coordinates, impulses, sort, coordinate, dataPath)


# Displays the impulses of the particles with matplotlib
def displayParticles3D(coordinates, impulses, sort, scl=1) :
	h = 1.255/100 #Gap between nodes
	step = 1000 #Display one particle out of 'step'

	# Determining the scale to apply depending on the sort
	scales = [2, 0.75, 2]
	scale = scl*abs(scales[sort]/max(max(impulses[0]), max(impulses[1]), max(impulses[2])))

	# Setting the coordinates and impulses to display
	x = [coordinates[0][i]/h for i in range(0, len(coordinates[0]), step)]
	y = [coordinates[1][i]/h for i in range(0, len(coordinates[1]), step)]
	z = [coordinates[2][i]/h for i in range(0, len(coordinates[2]), step)]
	u = [impulses[0][i]*scale for i in range(0, len(impulses[0]), step)]
	v = [impulses[1][i]*scale for i in range(0, len(impulses[1]), step)]
	w = [impulses[2][i]*scale for i in range(0, len(impulses[2]), step)]

	# Coloring the arrows for each particles
	col = []

	cmax = [max(u), max(v), max(w)]
	cmin = [min(u), min(v), min(w)]

	for i in range(len(u)) :
		# Normalizing
		partColor = [abs((u[i]-cmin[0])/(cmax[0]-cmin[0])), abs((v[i]-cmin[1])/(cmax[1]-cmin[1])), abs((w[i]-cmin[2])/(cmax[2]-cmin[2]))]

		# Finding the most important coordinate
		maxVal = partColor[0]
		maxIndex = 0
		for j in range(1, len(partColor)) :
			if (maxVal<partColor[j]) :
				maxVal = partColor[j]
				maxIndex = i

		# Decrease the importance of other coordinates
		partColor[(maxIndex+1)%3] /= 10
		partColor[(maxIndex+2)%3] /= 10

		# Applying the color
		col = col + [(partColor[0], partColor[1], partColor[2])]

	# Coloring the arrow's head
	for i in range(len(u)) :
		col = col + [col[i], col[i]]

	# Initializing matplotlib figure
	fig = plt.figure("Sort " + str(sort+1))
	ax = fig.add_subplot(111, projection='3d')

	ax.set_xlabel('X axis')
	ax.set_ylabel('Y axis')
	ax.set_zlabel('Z axis')

	ax.set_xlim([0, 102])
	ax.set_ylim([0, 6])
	ax.set_zlim([0, 6])

	ax.tick_params(axis='x', colors='red')
	ax.tick_params(axis='y', colors='green')
	ax.tick_params(axis='z', colors='blue')

	ax.xaxis.label.set_color('red')
	ax.yaxis.label.set_color('green')
	ax.zaxis.label.set_color('blue')

	ax.text2D(0.05, 0.95, "scale : "+str(scale), transform=ax.transAxes)

	# Drawing the particles
	q = ax.quiver(x, y, z, u, v, w, colors = col)


# Displays the impulses of the nodes with mayavi
def displayNodes3D(impulses, sort, scale) :

	# Meshgrid for the positions
	x, y, z = np.meshgrid(np.arange(0, 102, 1),
                      np.arange(0, 6, 1),
                      np.arange(0, 6, 1))

	# Impulses grids
	u = impulses[0]
	v = impulses[1]
	w = impulses[2]

	quiver3d(x, y, z, u, v, w, line_width=2, scale_factor=scale)
	mlab.show()


# Loads the coordinates and impulses for matplotlib display
def runParticles3D(path, sorts, scale, speed=False) :
	for sort in range(len(sorts)) :
		if (sorts[sort]) :
			[coordinates, impulses] = rd.readCoorImp(path, sort)

			if (speed) :
				impulses = impulseToSpeed(impulses)

			displayParticles3D(coordinates, impulses, sort, scale)


# Loads the impulses for mayavi display
def runNodes3D(path, sorts, scl = 1, speed=False) :
	size = (102, 6, 6, 3)
	h = 1.255/100

	for sort in range(len(sorts)) :
		if (sorts[sort]) :
			[coordinates, impulses] = rd.readCoorImp(path, sort)

			if (speed) :
				impulses = impulseToSpeed(impulses)

			# Hold the sum of the impulses of all the particles around each node
			grid = [[[[0 for ax in range(size[3])] for z in range(size[2])] for y in range(size[1])] for x in range(size[0])]
			# Count number of particles associated to each node
			gridCount = [[[0 for z in range(size[2])] for y in range(size[1])] for x in range(size[0])]

			# Each particle is associated to it's closest node
			for i in range(len(coordinates[0])) :
				x = int(round(coordinates[0][i]/h))
				y = int(round(coordinates[1][i]/h))
				z = int(round(coordinates[2][i]/h))
				gridCount[x][y][z] += 1 #The node has one more particle
				for j in range(3) :
					grid[x][y][z][j] += impulses[j][i] #the 3 impulses are added

			# Looking for the right scale to apply depending on the sort of particles
			scales = [4, 5, 1]
			scale = scl*abs(scales[sort]/max(max(impulses[0]), max(impulses[1]), max(impulses[2])))

			# Meshgrid to be red by Mayavi
			nodesImpulses = np.meshgrid(np.empty([102]),
	                      np.empty([6]),
	                      np.empty([6]))

			for x in range(size[0]) :
				for y in range(size[1]) :
					for z in range(size[2]) :
						# Avoid 0 divisions
						if (gridCount[x][y][z] == 0) :
							gridCount[x][y][z] = 1

						for ax in range(size[3]) :
							# Each node receives the mean impulse of the particles associated
							nodesImpulses[ax][y][x][z] = (grid[x][y][z][ax]*scale)/gridCount[x][y][z]

			displayNodes3D(nodesImpulses, sort, scl)
 


def showHelp() :
	print("1D :")
	print("\tIn order to display impulses of all particles : (choosing an axis)")
	print("\tpython3 displayImpulses.py 1D -p x/y/z/all inputFile\n")
	print("\tIn order to display a mean impulse for each node : (choosing an axis)")
	print("\tpython3 displayImpulses.py 1D -n x/y/z/all inputFile\n")
	print("2D :")
	print("\tIn order to produce a file to display with gnuplot :")
	print("\tpython3 displayImpulses.py 2D y/z inputFile\n")
	print("3D :")
	print("\tIn order to display impulses of particles in 3D for some sorts :")
	print("\tpython3 displayImpulses.py 3D inputFile 1/2/3 -p\n")
	print("\tIn order to display average impulses of nodes in 3D for some sorts :")
	print("\tpython3 displayImpulses.py 3D inputFile 1/2/3 -n\n")
	print("\tIn order to precise the scale :")
	print("\tpython3 displayImpulses.py 3D inputFile 1/2/3 -scale 10 -n/-p\n")
	print("\nIn order to display the speed instead of impulses, add -s at the end\n")


def main() :
	if (len(sys.argv) == 1) :
		print("To display help, type :\npython3 main.py -h")
	else :
		# Displaying speed instead of impulses
		speed = False
		if (sys.argv[1] == "1D") :
			if ((len(sys.argv) == 3) and (sys.argv[2] == "-s")) :
				speed = True
				
			if (sys.argv[2] == "-p") :
				run1D(sys.argv[4], sys.argv[3], False, speed)
			elif (sys.argv[2] == "-n") :
				run1D(sys.argv[4], sys.argv[3], True, speed)

		elif (sys.argv[1] == "2D") :
			if ((len(sys.argv) == 3) and (sys.argv[2] == "-s")) :
				speed = True

			run2D(sys.argv[3], sys.argv[2], speed)

		elif (sys.argv[1] == "3D") :
			path = sys.argv[2]

			sorts = [False, False, False]
			tmp = 3
			while (sys.argv[tmp][0] != "-") :
				if (sys.argv[tmp] == '1') :
					sorts[0] = True
				elif (sys.argv[tmp] == '2') :
					sorts[1] = True
				elif (sys.argv[tmp] == '3') :
					sorts[2] = True
				else :
					print(sys.argv[tmp])
					print("Sorts are 1, 2 or 3")
					showHelp()
				tmp += 1

			scale = 1
			if ((tmp<len(sys.argv)) and (sys.argv[tmp] == "-scale")) :
				tmp += 1
				scale = float(sys.argv[tmp])
				tmp += 1
			
			if ((tmp<len(sys.argv)) and (sys.argv[tmp+1] == "-s")) :
				speed = True
			
			if (sys.argv[tmp] == "-p") :
				runParticles3D(path, sorts, scale, speed)
			elif (sys.argv[tmp] == "-n") :
				runNodes3D(path, sorts, scale, speed)
			plt.show()


		elif (sys.argv[1] == "-h") :
			showHelp()

main()