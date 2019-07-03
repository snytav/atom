from netCDF4 import Dataset
import numpy as np
import sys
import struct
import numpy.ma as ma
import os

#returns "<ldd...(size)...ddl"
def createFormatInt8(size):
	form = "<l"
	for h in range(0,size):
		form += "d"
	form += "l"
	return form

#Openning repertories from repPath
def openRep(files) :
	for i in range(len(files)) :
		if ((files[i][-3:] != "dat") and (files[i][-2:] != "nc")) : #if it's a repertory
			repoPath = files[i]

			#adding '/' if necessary
			if (files[i][-1] != "/") : 
				repoPath += "/"

			#storing all the paths of the repertory
			tmpFiles = []
			for filePath in os.listdir(files[i]) :
				if ((filePath[-3:] == "dat") or (filePath[-2:] == "nc")) :
					tmpFiles += [repoPath + filePath]

			#including all the files of the repertory
			files = files[:i] + tmpFiles + files[i+1:]
	
	return files


#DISPLAY IMPULSES

def readFile(nameFile) :
	output = []
	if (nameFile[-3:] == "dat") :
		output = readAllFileDAT(nameFile)
	elif (nameFile[-2:] == "nc") :
		output = readAllFileCDF(nameFile)
	else :
		print("Wrong file format !")
	return output


#Determine the write reader to use
#readSort/readAxis = [True/False, True/False, True/False] or []
def readImpulses(nameFile, readSort = [], readAxis = []) :
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


#returns [fields, [props[0], coor_impulses[0]], [props[1], coor_impulses[1]], [props[2], coor_impulses[2]]]
#fields = [E[x][y][z], M[x][y][z], C[x][y][z], E2[x][y][z]]
#[props, coor_impulses] = [[ Ft, nbP, chrg, mass, Ft], [coorx, coory, coorz, impx, impy, impz]] ], ...]
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


#returns [[], [props[0], coor_impulses[0]], [props[1], coor_impulses[1]], [props[2], coor_impulses[2]]]
#[props, coor_impulses] = [[ Ft, nbP, chrg, mass, Ft], [coorx, coory, coorz, impx, impy, impz]] ], ...]
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


#returns [fields, [props[0], coor_impulses[0]], [props[1], coor_impulses[1]], [props[2], coor_impulses[2]]]
#fields = [E[x][y][z], M[x][y][z], C[x][y][z], E2[x][y][z]]
#[props, coor_impulses] = [[ Ft, nbP, chrg, mass, Ft], [coorx, coory, coorz, impx, impy, impz]] ], ...]
def readAllFileDAT(nameFile):

	print("File : \"", nameFile, "\"")
	# print("Reading ...")

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

		# print()
		# print("First Sort of Particules")

		#32bytes
		r = f.read(32)
		#Number For Fortan
		#nb sort0
		#charge sort 1
		#mass sort 0
		#Number for Fortran
		part1 = struct.unpack("<ldddl",r)

		size = int(part1[1])
		# print("Size : ",size)

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

		# print("OK")

		# print()
		# print("Second Sort of Particules")

		r = f.read(32)
		part2 = struct.unpack("<ldddl",r)

		size = int(part2[1])
		# print("Size : ",size)

		tabPart2 = np.zeros((6,size),dtype = 'd')
		form = createFormatInt8(size)

		for x in range(0,6):
			r = f.read(size*8+8)
			struct2 = struct.unpack(form, r)
			tmp = 1
			for i in range(0,size):
				tabPart2[x][i] = struct2[tmp]
				tmp+=1

		# print("OK")
		
		# print()
		# print("Third Sort of Particules")

		r = f.read(32)
		part3 = struct.unpack("<ldddl",r)

		size = int(part3[1])
		# print("Size : ",size)

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
		# print("OK\n")

		#tab = [E[3],M[3],C[3],E2[3]]
		#(part, tabPart) = ((Ft, nbP, chrg, mass, Ft), (parts[coorx, coory, coorz, impx, impy, impz]]), ...)
		return [tab,[part1,tabPart1],[part2,tabPart2],[part3,tabPart3]]


#returns [fields, [props[0], coor_impulses[0]], [props[1], coor_impulses[1]], [props[2], coor_impulses[2]]]
#fields = [E[x][y][z], M[x][y][z], C[x][y][z], E2[x][y][z]]
#[props, coor_impulses] = [[ Ft, nbP, chrg, mass, Ft], [coorx, coory, coorz, impx, impy, impz]] ], ...]
def readPartFileDAT(nameFile, readSort, readAxis):

	print("File : \"", nameFile, "\"")
	# print("Reading ...")

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
			# print("Sort number ", sort+1)
			r = f.read(32)
			parts[sort] = struct.unpack("<ldddl",r)
			size = int(parts[sort][1])
			# print("Size : ",size)
			if (readSort[sort]) :
				tabParts[sort] = np.zeros((6,size),dtype = 'd')
				form = createFormatInt8(size)
				for x in range(0, 6) :
					r = f.read(size*8+8)
					structs[sort] = struct.unpack(form, r)
					tmp = 1
					for i in range(0, size) :
						tabParts[sort][x][i] = structs[sort][tmp]
						tmp+=1 
			else :
				f.read(6*(size*8+8))
				# print("Skip sort")
			# print("OK")

	except IOError:
		print("Error")

	finally:
		f.close()
		# print("OK\n")
		#tab = [E[3],M[3],C[3],E2[3]]
		#(part, tabPart) = ((Ft, nbP, chrg, mass, Ft), (parts[coorx, coory, coorz, impx, impy, impz]]), ...)

		return [tab, [parts[0], tabParts[0]], [parts[1], tabParts[1]], [parts[2], tabParts[2]]]


#READ FIELDS

#Launch a reader depending on the file format
def readFields(nameFile) :
	output = []
	if (nameFile[-3:] == "dat") :
		output = readFieldsDAT(nameFile)
	elif (nameFile[-2:] == "nc") :
		output = readFieldsCDF(nameFile)
	else :
		print("Wrong file format !")
	return output

#Returns All fields values :
#[E[x], E[y], E[z], M[x], M[y], M[z], C[x], C[y], C[z], E2[x], E2[y], E2[z]]
#E[X] = tab[102][6][6]
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

#Returns all field values :
#[E[x], E[y], E[z], M[x], M[y], M[z], C[x], C[y], C[z], E2[x], E2[y], E2[z]]
#E[X] = tab[102][6][6]
def readFieldsDAT(nameFile) :
	print("File : \"", nameFile, "\"")
	# print("Reading ...\n")

	try:
		f = open(nameFile, "rb") #read binary
		fields = np.zeros((12,102,6,6),dtype='d')
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
						fields[x][i][j][k] = v[tmp]
						tmp+=1
	except IOError:
		print("Error")

	finally:
		f.close()
		# print("OK")
		#fields = [E[3],M[3],C[3],E2[3]]

		return fields


#READ ONLY ELECTRIC FIELD

#Launch a reader depending on the file format
def readElec(nameFile) :
	output = []
	if (nameFile[-3:] == "dat") :
		output = readElecDAT(nameFile)
	elif (nameFile[-2:] == "nc") :
		output = readElecCDF(nameFile)
	else :
		print("Wrong file format !")
	return output

#Returns All fields values :
#[E[x], E[y], E[z], M[x], M[y], M[z], C[x], C[y], C[z], E2[x], E2[y], E2[z]]
#E[X] = tab[102][6][6]
def readElecCDF(nameFile) :
	data = Dataset(nameFile, "r", format="NETCDF4")

	fields = []

	axis = ["x", "y", "z"]

	for i in range(3) :
		tmp = "E" + axis[i] 
		fields += [ma.getdata(data.variables[tmp])]

	return fields

#Returns all field values :
#[E[x], E[y], E[z], M[x], M[y], M[z], C[x], C[y], C[z], E2[x], E2[y], E2[z]]
#E[X] = tab[102][6][6]
def readElecDAT(nameFile) :
	print("File : \"", nameFile, "\"")
	# print("Reading ...\n")

	try:
		f = open(nameFile, "rb") #read binary
		fields = np.zeros((3,102,6,6),dtype='d')
		form = createFormatInt8(3672) # "<ld...dl"

		for x in range(0,3):
			#r receive dat string (binary ?)
			r = f.read(29384)
			#v recoit python string
			v = struct.unpack(form, r)
			tmp = 1
			for i in range(0,102):
				for j in range(0,6):
					for k in range(0,6):
						fields[x][i][j][k] = v[tmp]
						tmp+=1
	except IOError:
		print("Error")

	finally:
		f.close()
		# print("OK")
		#fields = [E[3],M[3],C[3],E2[3]]

		return fields