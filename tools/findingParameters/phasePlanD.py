import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import statistics
import numpy.ma as ma
import reader as rd
import multiprocessing as mp
import argparse

import time


#Returns the velocity of a particle (following axis) from it's impulses
def velocity(px, py, pz) :
	return ( px*( 1/((px**2 + py**2 + pz**2)**0.5) ) )


def displayPhasePlanDiagram(index, speed, coordinates, col, flag=False) :
	colors = ['b' , 'g' , 'r' ]#, 'c' , 'm' , 'y' , 'k']
	if flag :
		print("index :", len(index))
		print("speed :", len(speed))
	speeds = [speed[index[i]] for i in range(len(index))]
	coor = [coordinates[index[i]] for i in range(len(index))]
	plt.plot(coor, speeds, 'ro', markersize=0.2, label="", color=colors[col%len(colors)])#(col, 0.5, 0.5))


#Converting x-impulses into speeds
def speedFromImp(impulses) :
	speed = []
	for i in range(len(impulses[0])) :
		gamma = (impulses[0][i]**2 + impulses[1][i]**2 + impulses[2][i]**2 )**0.5
		speed += [abs(impulses[0][i]) / gamma] #ABS !!!??

	return speed

def tmp() :
	# Define an output queue
	output = mp.Queue()

	impulses = [impulses[0][:2150], impulses[1][:2150], impulses[2][:2150]]

	#Determining the repartition oftasks betweens processes
	nbCPU = mp.cpu_count()
	nbTasks = len(impulses[0])//nbCPU
	tasks = [0] + [nbTasks*i for i in range(1,nbCPU+1)]
	tasks[-1] = len(impulses[0])

	# Setup a list of processes that we want to run
	imp = []
	for i in range(nbCPU) :
		imp += [[impulses[0][tasks[i]:tasks[i+1]], impulses[1][tasks[i]:tasks[i+1]], impulses[2][tasks[i]:tasks[i+1]]]]
	print("len imp :", len(imp))
	print("len imp[0] :", len(imp[0]))
	print("len imp[0][0] :", len(imp[0][0]))
	
	processes = [mp.Process(target=speedPara, args=(imp[i], i, output)) for i in range(nbCPU)]

	# Run processes
	for p in processes:
	    p.start()

	# Exit the completed processes
	for p in processes:
	    p.join()

	print("done")
	# Get process results from the output queue
	speeds = sortSpeeds([output.get() for p in processes])
	print("block")

	return speeds


def speedPara(impulses, index, output) :
	speed = []
	for i in range(len(impulses[0])) :
		gamma = (impulses[0][i]**2 + impulses[1][i]**2 + impulses[2][i]**2 )**0.5
		speed += [abs(impulses[0][i]) / gamma] #ABS !!!??

	output.put([index,speed])


#Returns the processes results in the right order
def sortSpeeds(speeds) :
	result = []
	
	tmp= 0
	while (tmp<len(speeds)) :
		for i in range(len(speeds)) :
			if (speeds[i][0] == tmp) :
				print("Speed[",i,"] :",speeds[i][1])
				result += speeds[i][1]
				tmp += 1

	print("Result :",len(result))

	return result


#returns the index of particles classified by speed
def init(data, nbBatchs=100) :
	#batchs for 3 sorts of particles
	indexs = []
	speeds = []

	maxSpeed = 0
	minSpeed = 0
	delta = 0

	for sort in range(3) :
		#each batch correspond to the particles with speed between v and v+dv
		batchs = [[] for i in range(nbBatchs)]

		coordinates = data[1+sort][1][:3] #[[x], [y], [z]]
		impulses = data[1+sort][1][3:] #[[x], [y], [z]]

		#Converting x-impulses into speeds
		begSpeed = time.time()
		speed = speedFromImp(impulses)
		endSpeed = time.time()
		print("Converting speed :", endSpeed-begSpeed)

		maxSpeed = max(speed)*1.0001
		minSpeed = min(speed)*0.9999
		delta = maxSpeed/nbBatchs

		begSpeed = time.time()
		for i in range(len(speed)) :
			vi = int(speed[i]/delta)
			batchs[vi] += [i]
		endSpeed = time.time()
		print("Inserting speeds :", endSpeed-begSpeed)

		indexs += [batchs]
		speeds += [speed]

	output = [indexs, speeds]
	return output


#Represents the velocity of particles depending on the time
#All particles are classified in "batchs" from the initialization depending on their velocity
def runPhasePlan(files, nbBatchs = 100) :
	data = rd.readFile(files[0])
	#
	[indexs, speeds] = init(data, nbBatchs)

	for sort in range(3) :
		plt.figure(files[0] + " - sort " + str(sort+1))
		plt.xlabel('x')
		plt.ylabel('Velocity x')
		for batch in range(nbBatchs) :
			displayPhasePlanDiagram(indexs[sort][batch], speeds[sort], data[1+sort][1][0], batch)

	for file in range(1, len(files)) :
		data = rd.readFile(files[file]) #allSorts

		for sort in range(3) :
			plt.figure(files[file] + " - sort " + str(sort+1))
			plt.xlabel('x')
			plt.ylabel('Velocity x')
			speeds = speedFromImp(data[1+sort][1][3:])
			for batch in range(nbBatchs) :
				displayPhasePlanDiagram(indexs[sort][batch], speeds, data[1+sort][1][0], batch)

	plt.show()


def main() :
	parser = argparse.ArgumentParser(description="Classify particles in batch depending on there impulse x and display their evolution file to file")

	parser.add_argument("-n", "--number", type=int, help="Number of batch to make out of impulses/speed")
	parser.add_argument("FILE", type=str, help="List of files to be displayed", nargs="+")

	args = parser.parse_args()

	files = rd.openRep(args.FILE)

	nbBatchs = args.number

	runPhasePlan(files, nbBatchs)

main()