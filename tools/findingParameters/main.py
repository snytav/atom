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
	#format(file)

	arg = sys.argv[1]

	if (arg == "f") :
		file = sys.argv[2]	
		format(file)
	elif (arg == "i") :
		file = sys.argv[2]
		imp.runImpulse(file)
	elif (arg == "e") :
		file = sys.argv[2]
		fld.runElecField(file)
	else :
		print("Wrong arguments\n")
		print("In order to display impulses, type :")
		print("python3 findParams.py i inputFile\n")
		print("In order to display electric field, type :")
		print("python3 findParams.py e inputFile\n")

main()