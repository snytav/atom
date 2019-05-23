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
import impulses as imp
import fields as fld

#Displays the format of the data from readFile
def format(file):
	data = rd.readFile(file)

	fields = ["Electric Field", "Magnetic Fields", "Current", "HalfStep Electric Field"]
	axis = ["x", "y", "z"]

	print("data length : ", len(data))

	#Fields
	print("\tFields : ", len(data[0]), "\t(data[0])")
	for i in range(4) :
		print("\t\t",fields[i],": \t(data[0][",i*3,":",(i+1)*3,"])")
		for j in range(3) :
			print("\t\t\t", axis[j], "axis : ", len(data[0][(i*3)+j]),"*", len(data[0][(i*3)+j][j]), "* 6")

	#Particles
	for i in range(1, len(data)) :
		print("\tSort",i," : ", len(data[i]), "\t(data[", i, "])")
		print("\t\tFortran Number, Particles Number, Mass, Charge :", len(data[i][0]), "\t(data[",i,"][0]")
		print("\t\tCoordinates :")
		for j in range(3) :
			print("\t\t\tAxis",axis[j],": ", len(data[i][1][j]), "\t(data[",i,"][1][",j,"])")
		print("\t\tImpulses :")
		for j in range(3) :
			print("\t\t\tAxis",axis[j],": ", len(data[i][1][3+j]), "\t(data[",i,"][1][",3+j,"])")


def main() :
	if (len(sys.argv) == 1) :
		print("To display help, type :\npython3 main.py -h")
	else :
		if (sys.argv[1] == "-i") : #IMPULSES
			files = []
			stringSorts = []
			stringAxis = []
			sorts = [False, False, False]
			axis = [False, False, False]
			tmp = 2

			#Getting files path
			while (sys.argv[tmp][0] != "-") :
				files += [sys.argv[tmp]]
				tmp += 1

			#Getting sorts to treat
			if (sys.argv[tmp] != "-s") :
				print("Wrong arguments ! (sort)")
				return(-1)
			tmp += 1
			while(sys.argv[tmp][0] != "-") :
				stringSorts += [sys.argv[tmp]]
				tmp += 1

			#Getting axis to treat
			if (sys.argv[tmp] != "-a") :
				print("Wrong arguments ! (axis)")
				return(-1)
			tmp += 1
			while (tmp < len(sys.argv)) :
				stringAxis += [sys.argv[tmp]]
				tmp += 1

			#Converting arguments
			for s in stringSorts :
				if (s == "1") :
					sorts[0] = True
				elif (s == "2") :
					sorts[1] = True
				elif (s == "3") :
					sorts[2] = True
				else :
					print("Wrong arguments ! (sort value)")
					return(-1)

			for a in stringAxis :
				if (a == "x") :
					axis[0] = True
				elif (a == "y") :
					axis[1] = True
				elif (a == "z") :
					axis[2] = True
				else :
					print("Wrong arguments ! (axis value)")
					return(-1)

			#Launching the impulse display
			imp.runImpulse(files, sorts, axis)

		elif (sys.argv[1] == "-e") : #ELECTRIC FIELD
			files = []
			stringAxis = []
			axis = []
			y = 0
			z = 0
			tmp = 2

			#Getting files path
			while (sys.argv[tmp][0] != "-") :
				files += [sys.argv[tmp]]
				tmp += 1

			#Getting the coordinates of the field to display
			if (sys.argv[tmp] != "-a") :
				print("Wrong arguments ! (axis)")
				return(-1)
			tmp += 1
			while(sys.argv[tmp][0] != "-") :
				stringAxis += [sys.argv[tmp]]
				tmp += 1

			#Getting y & z coordinates of the mesh to treat
			if (sys.argv[tmp] != "-yz") :
				print("Wrong arguments ! (y or z)")
				return(-1)
			tmp += 1
			y = int(sys.argv[tmp])
			tmp += 1
			z = int(sys.argv[tmp])

			#Converting the parameters
			for a in stringAxis :
				if (a == "x") :
					axis+= [0]
				elif (a == "y") :
					axis+= [1]
				elif (a == "z") :
					axis+= [2]
				else :
					print("Wrong arguments ! (axis value)")
					return(-1)

			print("files",files)
			print("axis",axis)
			print("y",y)
			print("z",z)

			#Launching the electric field display
			fld.runElecField(files, axis, y, z)

		elif (sys.argv[1] == "-epsylon") :
			files = []
			for i in range(2, len(sys.argv)) :
				files += [sys.argv[i]]
			fld.runEpsylon(files)
		elif (sys.argv[1] == "-format") : #DATA FORMAT
			file = sys.argv[2]
			format(file)
		elif (sys.argv[1] == "-h") : #HELP
			print("In order to display the format of the loaded file :")
			print("python3 main.py -format inputFile\n")
			print("In order to display impulses, type :")
			print("python3 main.py -i inputFile(s) -s 2 3 -a x\n")
			print("In order to display electric field, type :")
			print("python3 main.py -e inputFile -a x -yz 2 3\n")
			print("In order to calculate electric field energy, type :")
			print("python3 main.py -epsylon inputFile(s) \n")
		else :
			print("Wrong arguments !")

main() 