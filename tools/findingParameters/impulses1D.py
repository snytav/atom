import numpy as np
import matplotlib.pyplot as plt
import sys
import statistics as st
import reader as rd
import argparse


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
	plt.figure(title)
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
	plt.figure(title)
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


def run1D(dataPath, axis, nodes, speed) :
	#Reading data
	dataSet = rd.readFile(dataPath)
	sorts = [True, True, True]

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

def main() :
	parser = argparse.ArgumentParser(description="Display 1D representation of the impulses following chosen axis.")

	parser.add_argument("axis", type=str, choices=['x','y','z'], help="Axis to display", nargs="+")
	parser.add_argument("-n", "--nodes", action="store_true", help="Dislpay mean impulses among yz-plan for each node of axis [-a]")
	parser.add_argument("-s", "--speed", action="store_true", help="Dislpay speeds instead of impulses")
	parser.add_argument("file", type=str, help="List of files to be displayed", nargs="+")

	args = parser.parse_args()

	#Parsing axis
	axis = [False, False, False]
	for a in args.axis :
		if (a == 'x') :
			axis[0] = True
		elif (a == 'y') :
			axis[1] = True
		elif (a == 'z') :
			axis[2] = True

	files = rd.openRep(args.file)

	for file in files :
		run1D(file, axis, args.nodes, args.speed)

main()