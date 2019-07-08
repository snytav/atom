import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import sys

import numpy.ma as ma
import reader as rd
import impulses as imp
import fields as fld
import epsylon as eps
import phasePlanD as ppd
import velocity as vlc


def showHelp() :
	print("In order to display the format of the loaded file :")
	print("python3 main.py -format inputFile\n")
	print("In order to display impulses, type :")
	print("python3 main.py -i inputFile(s) -s 2 3 -a x [-options : sep, m, v, c]\n")
	print("In order to display fields, type :")
	print("python3 main.py -f inputFile -s fieldNumber -yz 2 3\n")
	print("\tTo display electric field :")
	print("\tpython3 main.py -f inputFile -s 0 -yz 2 3\n")
	print("\tThe value for -s can be between 0 & 3, example : ")
	print("\tTo display magnetic field & currant field :")
	print("\tpython3 main.py -f inputFile -s 1 2 -yz 2 3\n")
	print("In order to calculate electric field energy, type :")
	print("python3 main.py -epsylon inputFile(s) \n")
	print("In order display plane phase diagram, type :")
	print("python3 main.py -ppd inputFile(s) -nb 100\n")
	print("In order display 3D velocities, type :")
	print("python3 main.py -v inputFile(s)\n")


#Displays the format of the data returned by 'readFile'
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
			sorts = [False, False, False]
			
			stringAxis = []
			axis = [False, False, False]
			
			#[Separated, ShowMean, ShowVariance, ShowCurve]
			options = [False, False, False, False]
			
			tmp = 2

			#Getting files paths
			while (sys.argv[tmp][0] != "-") :
				files += [sys.argv[tmp]]
				tmp += 1

			#openning repositories
			files = rd.openRep(files)

			#SORTS
			#Getting sorts to treat
			if (sys.argv[tmp] != "-s") :
				print("Wrong arguments ! (sort)")
				showHelp()
				return(-1)
			tmp += 1
			while(sys.argv[tmp][0] != "-") :
				stringSorts += [sys.argv[tmp]]
				tmp += 1

			#Converting sorts
			for s in stringSorts :
				if (s == "1") :
					sorts[0] = True
				elif (s == "2") :
					sorts[1] = True
				elif (s == "3") :
					sorts[2] = True
				else :
					print("Wrong arguments ! (sort value)")
					showHelp()
					return(-1)

			#AXIS
			#Getting axis to treat
			if (sys.argv[tmp] != "-a") :
				print("Wrong arguments ! (axis)")
				showHelp()
				return(-1)
			tmp += 1
			while ((tmp < len(sys.argv)) and (sys.argv[tmp][0] != "-")) :
				stringAxis += [sys.argv[tmp]]
				tmp += 1

			#Determining the axis to display
			for a in stringAxis :
				if (a == "x") :
					axis[0] = True
				elif (a == "y") :
					axis[1] = True
				elif (a == "z") :
					axis[2] = True
				else :
					print("Wrong arguments ! (axis value)")
					showHelp()
					return(-1)

			#Determining options
			while (tmp<len(sys.argv)) :
				if (sys.argv[tmp] == "-sep") :
					options[0] = True
				elif (sys.argv[tmp] == "-m") :
					options[1] = True
				elif (sys.argv[tmp] == "-v") :
					options[1] = True
					options[2] = True
				elif (sys.argv[tmp] == "-c") :
					options[3] = True
				else :
					print("Wrong arguments !")
					print("Options :")
					print("-sep : displays the impulses separetely for each files")
					print("-m : calculates and displays the mean")
					print("-v : calculates and displays the variance")
					print("-c : displays a the gaussian curve that is followed by the impulses")
				tmp += 1

			#Launching the impulse display
			imp.runImpulse(files, sorts, axis, options)

		elif (sys.argv[1] == "-f") : #FIELD
			files = []
			sorts = []
			axis = []

			#Selecting an 'x-line' from the mesh
			y = 0
			z = 0
			
			tmp = 2

			# #Getting files path
			while (sys.argv[tmp][0] != "-") :
				files += [sys.argv[tmp]]
				tmp += 1

			#openning repositories
			files = rd.openRep(files)

			#Getting the sort of field to display (electric, magnetic, currant, halfstep magnetic)
			if (sys.argv[tmp] != "-s") :
				print("Wrong arguments ! (sort)")
				showHelp()
				return(-1)
			tmp += 1
			while(sys.argv[tmp][0] != "-") :
				sorts += [int(sys.argv[tmp])]
				tmp += 1

			#Getting y & z coordinates of the mesh to treat
			if (sys.argv[tmp] != "-yz") :
				print("Wrong arguments ! (y or z)")
				showHelp()
				return(-1)
			tmp += 1
			y = int(sys.argv[tmp])
			tmp += 1
			z = int(sys.argv[tmp])

			print("files :",files)
			print("sorts :",sorts)
			print("y :",y)
			print("z :",z)

			#Launching the field display
			fld.runField(files, sorts, y, z)

		elif (sys.argv[1] == "-epsylon") :
			files = []
			for tmp in range(2, len(sys.argv)) :
				files += [sys.argv[tmp]] 

			#openning repositories
			files = rd.openRep(files)

			eps.runEpsylon(files)

		elif (sys.argv[1] == "-ppd") :#PHASE PLANE DIAGRAMS
			files = []
			nbBatchs = 100
			tmp = 2
			while (tmp<len(sys.argv) and sys.argv[tmp] != "-nb") :
				files += [sys.argv[tmp]] 
				tmp += 1

			#openning repositories
			files = rd.openRep(files)

			if (tmp<len(sys.argv) and sys.argv[tmp] == "-nb") :
				tmp += 1
				nbBatchs = int(sys.argv[tmp])
			elif (tmp<len(sys.argv)) :
				print("Wrong arguments !")
				showHelp()

			ppd.runPhasePlan(files, nbBatchs)

		elif (sys.argv[1] == "-v") :#VELOCITIES
			files = []
			tmp = 2
			while (tmp<len(sys.argv)) :
				files += [sys.argv[tmp]] 
				tmp += 1

			#openning repositories
			files = rd.openRep(files)

			vlc.run3DVelocity(files)	

		elif (sys.argv[1] == "-format") : #DATA FORMAT
			file = sys.argv[2]
			format(file)
		
		elif (sys.argv[1] == "-h") : #HELP
			showHelp()
		
		else :
			print("Wrong arguments !")
			showHelp()

main()