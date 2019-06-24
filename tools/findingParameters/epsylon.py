import reader as rd
import matplotlib.pyplot as plt
import numpy as np

#field = [Ex, Ey, Ez] with Ex = [102][6][6]
#Return sum((Ex, Ey, Ez)^2)
def epsylon(field) :
	[Ex, Ey, Ez] = field
	sum = 0
	for ix in range(len(Ex)) :
		for iy in range(len(Ex[0])) :
			for iz in range(len(Ex[0][0])) :
				sum += Ex[ix][iy][iz]**2 + Ey[ix][iy][iz]**2 + Ez[ix][iy][iz]**2

	return sum


def displayEpsylon(epsylons) :
	plt.plot(np.arange(len(epsylons)), epsylons, markersize=0.1)


def runEpsylon(files) :
	epsylons = []
	for file in files :
		#load data
		electricField = rd.readElec(file)
		epsylons += [epsylon(electricField)]

	print("Epsylon :", epsylons)

	displayEpsylon(epsylons)

	plt.xlabel('Time')
	plt.ylabel('Epsylon')
	plt.show()