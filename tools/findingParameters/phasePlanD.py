import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import statistics
import numpy.ma as ma
import reader as rd

#Returns the velocity of a particle (following axis) from it's impulses
def velocity(px, py, pz) :
	return ( px*( 1/((px**2 + py**2 + pz**2)**0.5) ) )

def displayPhasePlanDiagram() :
	abscissa = np.arange(0, 102,1)#len(field), 1)
	plt.plot(abscissa, velociy, markersize=0.1, label=label)

def init(data) :
	coorSortAxis = data[1 + sort][1][:3]
	impulsesSortAxis = data[1 + sort][1][3:]

	print("coorSortAxis :", len(coorSortAxis))
	print("coorSortAxis[0] :", len(coorSortAxis[0]))
	print("impulsesSortAxis :", len(impulsesSortAxis))
	print("impulsesSortAxis[0] :", len(impulsesSortAxis[0]))


#Represents the velocity of particles depending on the time
#All particles are classified in "batchs" from the initialization depending on there velocity
def runPhasePlan(files, nbBatchs = 100) :
	dataSet = []
	allSorts = [True, True, True]

	for file in files :
		dataSet += [rd.readFile(file)] #allSorts

	init = init(dataSet[0])

	#displayPhasePlanDiagram()

	plt.xlabel('x')
	plt.ylabel('Velocity x')
	plt.show()