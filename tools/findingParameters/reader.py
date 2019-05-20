from netCDF4 import Dataset
import numpy as np
import sys
import struct
import numpy.ma as ma

#return "<ld...(size)...dl"
def createFormatInt8(size):
	form = "<l"
	for h in range(0,size):
		form += "d"
	form += "l"
	return form

def readFile(nameFile, readSort = [], readAxis = []) :
	output = []
	if (nameFile[-3:] == "dat") :
		if (readSort == []) :
			output = readAllFileDAT(nameFile)
		else :
			output = readPartFileDAT(nameFile, readSort, readAxis)
	elif (nameFile[-2:] == "nc") :
		if (readSort == []) :
			output = readAllFileCDF(nameFile)
		else :
			output = readPartFileCDF(nameFile, readSort, readAxis)
	else :
		print("Wrong file format !")
	return output

#tab = [E[3],M[3],C[3],E2[3]]
#(part, tabPart) = ((Ft, nbP, chrg, mass, Ft), (coord_impulses[coord[3], impulse[3]]), ...)
def readAllFileCDF(nameFile) :
	data = Dataset(nameFile, "r", format="NETCDF4")

	fields = []

	fieldsName = ["E", "M", "J", "Q"]
	axis = ["x", "y", "z"]

	for i in range(4) :
		for j in range(3) :
			tmp = fieldsName[i] + axis[j] 
			fields += [ma.getdata(data.variables[tmp])]

	num = ["0", "1", "2"]
	
	tmpExtraNumber = ""
	tmpNbPart = ""
	tmpCharge = ""
	tmpMass = ""
	
	tmpCoor = ""
	tmpImp = ""

	props = [[1,2,3,4], [1,2,3,4], [1,2,3,4]]
	coor_impulses = [[[] for j in range(6)] for i in range(3)]

	for sort in range(3) :
		tmpExtraNumber = "Extra_number_" + num[sort]
		tmpNbPart = "Nb_particles_" + num[sort]
		tmpCharge = "Charge_" + num[sort]
		tmpMass = "Mass_" + num[sort]

		props[sort] = [data.variables[tmpExtraNumber], data.variables[tmpNbPart], data.variables[tmpCharge], data.variables[tmpMass]]

		for ax in range(3) :
			tmpCoor = "Coordinates_" + axis[ax] + num[sort]
			coor_impulses[sort][ax] = ma.getdata(data.variables[tmpCoor][:])

			tmpImp = "Impulses_" + axis[ax] + num[sort]
			coor_impulses[sort][3+ax] = ma.getdata(data.variables[tmpImp][:])

	return [fields, [props[0], coor_impulses[0]], [props[1], coor_impulses[1]], [props[2], coor_impulses[2]]]

#tab = [E[3],M[3],C[3],E2[3]]
#(props, coor_impulses) = ((Ft, nbP, chrg, mass, Ft), (coor_impulses[coord[3], impulse[3]]), ...)
def readPartFileCDF(nameFile, readSort, readAxis) :
	data = Dataset(nameFile, "r", format="NETCDF4")

	axis = ["x", "y", "z"]
	num = ["0", "1", "2"]
	
	tmpExtraNumber = ""
	tmpNbPart = ""
	tmpCharge = ""
	tmpMass = ""
	
	tmpCoor = ""
	tmpImp = ""

	props = [[1,2,3,4], [1,2,3,4], [1,2,3,4]]
	coor_impulses = [[[] for j in range(6)] for i in range(3)]
	for sort in range(len(readSort)) :
		if (readSort[sort]) :
			tmpExtraNumber = "Extra_number_" + num[sort]
			tmpNbPart = "Nb_particles_" + num[sort]
			tmpCharge = "Charge_" + num[sort]
			tmpMass = "Mass_" + num[sort]
			
			props[sort] = [data.variables[tmpExtraNumber], data.variables[tmpNbPart], data.variables[tmpCharge], data.variables[tmpMass]]
			
			for ax in range(len(readAxis)) :
				if (readAxis[ax]) :
					# tmpCoor = "Coordinates_" + axis[ax] + num[sort]
					# coor_impulses[sort][ax] = ma.getdata(data.variables[tmpCoor][:])

					tmpImp = "Impulses_" + axis[ax] + num[sort]
					coor_impulses[sort][3+ax] = ma.getdata(data.variables[tmpImp][:])

	return [[], [props[0], coor_impulses[0]], [props[1], coor_impulses[1]], [props[2], coor_impulses[2]]]


#Read a dat file
#Returns (tab,(part1,tabPart1),(part2,tabPart2),(part3,tabPart3))
#tab 
def readAllFileDAT(nameFile):

	print("File : \"", nameFile, "\"")
	print("Reading ...\n")

	try:
		f = open(nameFile, "rb") #read binary
		tab = np.zeros((12,102,6,6),dtype='d')
		form = createFormatInt8(3672) # "<ld...dl"

		for x in range(0,12):
			#r receive dat string (binary ?)
			r = f.read(29384)
			#v recoit python string
			v = struct.unpack(form, r)
			tmp = 1
			for i in range(0,102):
				for j in range(0,6):
					for k in range(0,6):
						tab[x][i][j][k] = v[tmp]
						tmp+=1

		print()
		print("First Sort of Particules")

		#32bytes
		r = f.read(32)
		#Number For Fortan
		#nb sort0
		#charge sort 1
		#mass sort 0
		#Number for Fortran
		part1 = struct.unpack("<ldddl",r)

		size = int(part1[1])
		print("Size : ",size)

		#Coordinate/Impulses
		tabPart1 = np.zeros((6,size),dtype = 'd')
		form = createFormatInt8(size)

		for x in range(0,6):
			r = f.read(size*8+8)
			struct1 = struct.unpack(form, r)
			tmp = 1
			for i in range(0,size):
				tabPart1[x][i] = struct1[tmp]
				tmp+=1

		print("OK")

		print()
		print("Second Sort of Particules")

		r = f.read(32)
		part2 = struct.unpack("<ldddl",r)

		size = int(part2[1])
		print("Size : ",size)

		tabPart2 = np.zeros((6,size),dtype = 'd')
		form = createFormatInt8(size)

		for x in range(0,6):
			r = f.read(size*8+8)
			struct2 = struct.unpack(form, r)
			tmp = 1
			for i in range(0,size):
				tabPart2[x][i] = struct2[tmp]
				tmp+=1

		print("OK")
		
		print()
		print("Third Sort of Particules")

		r = f.read(32)
		part3 = struct.unpack("<ldddl",r)

		size = int(part3[1])
		print("Size : ",size)

		tabPart3 = np.zeros((6,size),dtype = 'd')
		form = createFormatInt8(size)

		for x in range(0,6):
			r = f.read(size*8+8)
			struct3 = struct.unpack(form, r)
			tmp = 1
			for i in range(0,size):
				tabPart3[x][i] = struct3[tmp]
				tmp+=1

	except IOError:
		print("Error")

	finally:
		f.close()
		print("OK")

		#tab = [E[3],M[3],C[3],E2[3]]
		#(part, tabPart) = ((Ft, nbP, chrg, mass, Ft), (parts[coord[3], impulse[3]]), ...)
		return [tab,[part1,tabPart1],[part2,tabPart2],[part3,tabPart3]]

#Read a dat file
#Returns (tab,(part1,tabPart1),(part2,tabPart2),(part3,tabPart3))
#tab 
def readPartFileDAT(nameFile, readSort, readAxis):

	print("File : \"", nameFile, "\"")
	print("Reading ...\n")

	try:
		f = open(nameFile, "rb") #read binary
		tab = np.zeros((12,102,6,6),dtype='d')
		form = createFormatInt8(3672) # "<ld...dl"

		for x in range(0,12):
			#r receive dat string (binary ?)
			r = f.read(29384)
			#v recoit python string
			v = struct.unpack(form, r)
			tmp = 1
			for i in range(0,102):
				for j in range(0,6):
					for k in range(0,6):
						tab[x][i][j][k] = v[tmp]
						tmp+=1

		parts = [[], [], []]
		tabParts = [[], [], []]
		structs = [[], [], []]
		for sort in range(len(readSort)) :
			print()
			print("Sort number ", sort+1)
			r = f.read(32)
			parts[sort] = struct.unpack("<ldddl",r)
			size = int(parts[sort][1])
			print("Size : ",size)
			tabParts[sort] = np.zeros((6,size),dtype = 'd')
			form = createFormatInt8(size)
			for x in range(0, 6) :
				r = f.read(size*8+8)
				structs[sort] = struct.unpack(form, r)
				tmp = 1
				for i in range(0, size) :
					tabParts[sort][x][i] = structs[sort][tmp]
					tmp+=1 
			print("OK")

	except IOError:
		print("Error")

	finally:
		f.close()
		print("OK")
		#tab = [E[3],M[3],C[3],E2[3]]
		#(part, tabPart) = ((Ft, nbP, chrg, mass, Ft), (parts[coord[3], impulse[3]]), ...)

		return [tab, [parts[0], tabParts[0]], [parts[1], tabParts[1]], [parts[2], tabParts[2]]]

def readFields(nameFile) :
	output = []
	if (nameFile[-3:] == "dat") :
		output = readFieldsDAT(nameFile)
	elif (nameFile[-2:] == "nc") :
		output = readFieldsCDF(nameFile)
	else :
		print("Wrong file format !")
	return output

def readFieldsCDF(nameFile) :
	data = Dataset(nameFile, "r", format="NETCDF4")

	fields = []

	fieldsName = ["E", "M", "J", "Q"]
	axis = ["x", "y", "z"]

	for i in range(4) :
		for j in range(3) :
			tmp = fieldsName[i] + axis[j] 
			fields += [ma.getdata(data.variables[tmp])]

	return fields

def readFieldsDAT(nameFile) :
	print("File : \"", nameFile, "\"")
	print("Reading ...\n")

	try:
		f = open(nameFile, "rb") #read binary
		tab = np.zeros((12,102,6,6),dtype='d')
		form = createFormatInt8(3672) # "<ld...dl"

		for x in range(0,12):
			#r receive dat string (binary ?)
			r = f.read(29384)
			#v recoit python string
			v = struct.unpack(form, r)
			tmp = 1
			for i in range(0,102):
				for j in range(0,6):
					for k in range(0,6):
						tab[x][i][j][k] = v[tmp]
						tmp+=1
	except IOError:
		print("Error")

	finally:
		f.close()
		print("OK")
		#tab = [E[3],M[3],C[3],E2[3]]

		return tab