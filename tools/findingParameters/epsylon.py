import os
import multiprocessing as mp
import string
import reader as rd
import sys
import matplotlib.pyplot as plt
import numpy as np
import reader as rd
import argparse


#Returns the epsylon of the files input associated to the id of the process to get the order
def epsylon(files, pid, output) :
	epsylons = [] #contain the epsylon for each file

	for file in files :

		#load data
		electricField = rd.readElec(file)
		[Ex, Ey, Ez] = electricField		

		sum = 0 #initializing value of field
		#Adding the electric value of each node
		for ix in range(len(Ex)) :
			for iy in range(len(Ex[0])) :
				for iz in range(len(Ex[0][0])) :
					sum += Ex[ix][iy][iz]**2 + Ey[ix][iy][iz]**2 + Ez[ix][iy][iz]**2
		epsylons += [sum]

	output.put([pid, epsylons])


def displayEpsylon(epsylons) :
	plt.figure("Epsylon")
	plt.xlabel('Time')
	plt.ylabel('Epsylon')
	plt.plot(np.arange(len(epsylons)), epsylons, markersize=0.1)
	plt.show()


#Returns the processes results in the right order
def sortEps(epsylons) :
	result = []
	
	tmp= 0
	while (tmp<len(epsylons)) :
		for i in range(len(epsylons)) :
			if (epsylons[i][0] == tmp) :
				result += epsylons[i][1]
				tmp += 1

	return result


def runEpsylon(files) :
	for file in files :
		print(file)

	# Define an output queue
	output = mp.Queue()

	#Determining the repartition oftasks betweens processes
	nbCPU = mp.cpu_count()
	nbTasks = len(files)//nbCPU
	tasks = [0] + [nbTasks*i for i in range(1,nbCPU+1)]
	tasks[-1] = len(files)

	# Setup a list of processes that we want to run
	processes = [mp.Process(target=epsylon, args=(files[tasks[i]: tasks[i+1]], i, output)) for i in range(nbCPU)]

	# Run processes
	for p in processes:
	    p.start()

	# Exit the completed processes
	for p in processes:
	    p.join()

	# Get process results from the output queue
	epsylons = sortEps([output.get() for p in processes])

	displayEpsylon(epsylons)


def main() :
	parser = argparse.ArgumentParser(description="Calculate the energy \'epsilon\' of the electric field and displays the result on a graph.")

	parser.add_argument("FILE", type=str, help="List of files to be treated", nargs="+")

	args = parser.parse_args()

	files = rd.openRep(args.FILE)

	runEpsylon(files)


main()