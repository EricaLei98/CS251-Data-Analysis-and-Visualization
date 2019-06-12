# Erica Lei
# CS251 Spring 2017
# project6

import numpy as np
import csv
import sys
import time
import analysis

# read csv file
class Data:

	def __init__(self, filename = None):
		# list of all headers
		self.headers = []
		# list of all types
		self.types = []
		# list of lists, each sublist corresponds to a row of the data CSV file.
		self.rows = []
		# dictionary mapping a header to its corresponding column)
		self.header2col = {}
		# numeric types
		self.num_headers = []
		self.num_types = []
		self.num_header2col = {}
		#extension 1
		self.enumDic = {}
		self.enumIdx = 0

		if filename != None:
			self.read(filename)

	def read(self,filename):

		fp = open(filename,'rU')
		csv_reader = csv.reader(fp)

		line = next(csv_reader)
		for header in line:
			h = header.strip()
			# remove white space from before and after the string
			self.headers.append(h)

		for i in range(len(self.headers)):
			self.header2col[self.headers[i]] = i

		line = next(csv_reader)

		for onetype in line:
			o = onetype.strip()
			self.types.append(o)


		for line in csv_reader:
			newList = []
			for x in line:
				# if it is a number
				if self.determine(x) == float:
					newList.append(float(x))

				# if it is a EXTENSION: enumerated types
				elif self.types[line.index(x)]== "enum":
					if x in self.enumDic:
						newList.append(self.enumDic[x])
					else:
						self.enumDic[x] = self.enumIdx
						self.enumIdx += 1
						newList.append(self.enumDic[x])
				# if it is a EXTENSION: date
				elif self.types[line.index(x)]== "date":
					s = time.strptime(x, "%m/%d/%y")
					string = str(s[0])+"."+str(s[1]).zfill(2)+str(s[2]).zfill(2)
					f = float(string)
					newList.append(f)

				# if it is a string
				else:
					newList.append(x.strip())
			self.rows.append(newList)
		self.rawdata = np.matrix(self.rows)
		self.numD = self.get_numeric_data(self.rawdata)
		return self.numD

	# determine the datatypes
	def determine(self, value):
		heuristics = [(float, float)]
		for (type,test) in heuristics:
			try:
				test(value)
				return type
			except ValueError:
				continue
		# All other heuristics failed it is a string
		return str

	# return the numeric matrix 
	def get_numeric_data(self, inputdata):
		num_headers = list(self.headers)
		num_types = list(self.types)
		num_header2col = dict(self.header2col)

		# discard types
		indexes = []
		idx=0
		for onetype in num_types:
			# EXTENSION - enum
			if onetype != "numeric" and onetype != "enum" and onetype != "date":
				indexes.append(idx)
				idx += 1
			else:
				idx += 1

		# discard headers
		indexes.reverse()
		self.numD = inputdata
		for i in indexes:
			num_types.pop(i)

			curHeader = num_headers.pop(i)

			num_header2col.pop(curHeader,None)
		# discard columns
		self.numD = np.delete(self.numD, indexes, 1)
		self.numD = np.float_(self.numD)
		n=0
		for header in num_headers:
			num_header2col[header] = n
			n +=1 
		self.num_headers = num_headers
		self.num_types = num_types
		self.num_header2col = num_header2col

		return self.numD

	#returns a list of all of the headers.
	def get_headers(self, datatype = 0):
		if len(self.headers)==0:
			if datatype == 1:
				for i in range(self.rawdata.shape[1]):
					self.headers.append("eigvec"+str(i).zfill(2))
					self.header2col[self.headers[i]] = i
			elif datatype == 2:
				for i in range(self.rawdata.shape[1]):
					self.headers.append("mean"+str(i).zfill(2))
					self.header2col[self.headers[i]] = i

		return self.headers
	# return a list of numeric headers
	def get_num_headers(self, datatype = 0):
		if len(self.num_headers)==0:
			if datatype == 1: 
				for i in range(self.numD.shape[1]):
					self.num_headers.append("eigvec"+str(i).zfill(2))
					self.num_header2col[self.num_headers[i]] = i
			elif datatype == 2:
				for i in range(self.numD.shape[1]):
					self.num_headers.append("mean"+str(i).zfill(2))
					self.num_header2col[self.num_headers[i]] = i
		return self.num_headers
	# returns a list of all types
	def get_types(self):
		if len(self.types)==0:
			for i in range(len(self.rawdata[0].tolist()[0])):
				if type( self.rawdata[0].tolist()[0][i]) == float:
					self.types.append("numeric")

		return self.types
	# returns a list of numeric types
	def get_num_types(self):
		if len(self.num_types)==0:
			for i in range(len(self.numD[0].tolist()[0])):
				if type( self.numD[0].tolist()[0][i]) == float:
					self.num_types.append("numeric")
		return self.num_types
	#returns the number of columns
	def get_num_dimensions(self):
		return self.numD.shape[1]

	#returns the number of "numeric matrix" columns
	# def get_numeric_dimensions(self):
	# 	return self.numD.shape[1]

	#returns the number of points/rows in the data set
	def get_num_points(self):
		return self.rawdata.shape[0]

	#returns the number of points/rows in the "numeric" data set
	def get_numeric_points(self):
		return self.numD.shape[0]

	# returns the specified row as a NumPy matrix
	def get_row(self, rowIndex):
		return self.rawdata[rowIndex]

	# returns the specified value in the given column
	def get_value(self, header, rowIndex):
		return self.rawdata[rowIndex, self.header2col[header]]

	# returns the specified value in the given column
	def get_numeric_value(self, header, rowIndex):
		return self.numD[rowIndex, self.num_header2col[header]]

	# returns the data type with given header
	def get_type(self, header):

		v = self.get_value(headers[i],0)
		if self.determine(v) == float:
			return "numeric"
		else:
			return "string"

	# takes in a list of columns headers,
	# returns a Numpy atrix with the data for all rows 
	# but just the specified columns.
	#def getCol(self, headers):
	def get_data(self, headers):
		indexes = []

		for item in headers:
			indexes.append(self.header2col[item])

		return self.rawdata[:,indexes]	

	def getNumCol(self, headers):
		indexes = []
		print(self.num_header2col)
		for item in headers:
			indexes.append(self.num_header2col[item])

		return self.numD[:,indexes]	
	
	# add a column
	def addColumn(self, header, typeofdata, data):
		# make sure right points
		if data.shape[0] != self.numD.shape[0]:
			print("new col points do not match")
		else:
			# update header, dict
			self.headers.append(header)
			self.header2col[header] = len(self.headers)-1
			# update types
			self.types.append(typeofdata)
			# update rawdata
			d = np.array(data)
			self.rawdata=np.hstack((self.rawdata,d))
			# if appropriate, update numD 
			self.numD = self.get_numeric_data(self.rawdata)
	# add a row
	def addRow(self,d):
		self.numD = np.vstack((self.numD, d))

	#  write out a selected set of headers to a specified file. 
	def write_to_file(self, filename, headers):
		f = open(filename + ".csv", mode='w')

		# write headers
		for header in headers[:-1]:
			f.write(header + ",")
		f.write(headers[-1] + "\n")

		# write types
		for header in headers[:-1]:
			f.write(self.raw_types[self.header2raw[header]] + ",")
		f.write(self.raw_types[self.header2raw[headers[-1]]] + "\n")

		# write data
		for i in range(len(self.raw_data)):
			for header in headers[:-1]:
				f.write(str(self.raw_data[i][self.header2col[header]]) + ",")
			f.write(str(self.raw_data[i][self.header2raw[headers[-1]]]) + "\n")

	# main test program
	def main(argv):

		# test command line arguments
		if len(argv) < 2:
			print( 'Usage: python %s <csv filename>' % (argv[0]))
			exit(0)

		# create a data object, which reads in the data
		dobj = Data(argv[1])

		# print out information about the dat
		print('Number of rows:    ', dobj.get_num_points() )
		print('Number of columns: ', dobj.get_num_dimensions() )

		# print out the headers
		print("\nHeaders:")
		headers = dobj.get_raw_headers()
		s = headers[0]
		for header in headers[1:]:
			s += "," + header
		print( s )

		# print out the types
		print("\nTypes:")
		types = dobj.get_raw_types()
		s = types[0]
		for type in types[1:]:
			s += ", " + type
		print( s )

		# print out a single row
		print("\nPrinting row index 2:")
		print( dobj.get_row( 2 ) )

		# print out cols
		c = dobj.getCol([dobj.get_raw_headers()[0],dobj.get_raw_headers()[1]] )
		print("\Select the 1st and 2nd col:")
		print( c )

		# print out all of the data
		print("\n All Data:")
		headers = dobj.get_raw_headers()
		for i in range(dobj.get_num_points()):
			s = str( dobj.get_value( headers[0], i ))
			for header in headers[1:]:
				s += str(dobj.get_value( header, i ))
			print(s)

		# EXTENSION
		print("\nAdd a Column")
		dobj.addColumn("new col", "numeric", [[0],[1],[2]])
		print('Number of columns: ', dobj.get_num_dimensions())


		print("--- testing manipulations on the 1st and the 3rd NUMERIC columns:---")
		d = dobj.getCol([dobj.get_num_headers()[0],dobj.get_num_headers()[2]] )
		print(d)
		# test normalized columns
		print("\n Normalize by columns")
		sep_norm = analysis.normalize_columns_separately([dobj.get_num_headers()[0],dobj.get_num_headers()[2]], dobj)
		print(sep_norm)

		# test normalized matrix
		print("\n Normalize the whole matrix")
		tog_norm = analysis.normalize_columns_together([dobj.get_num_headers()[0],dobj.get_num_headers()[2]], dobj)
		print(tog_norm)  


class PCAData(Data):
	def __init__(self, projected_data, eigen_vectors, eigen_values, original_means, original_headers):
		
		Data.__init__(self, filename=None)
		self.rawdata = projected_data
		self.numD = projected_data
		self.eigen_values = eigen_values
		self.eigen_vectors = eigen_vectors
		self.original_means = original_means
		self.original_headers = original_headers

	def get_eigenvalues(self):
		#returns a copy of the eigenvalues as a single-row numpy matrix.
		return self.eigen_values
	def get_eigenvectors(self): 
		#returns a copy of the eigenvectors as a numpy matrix with the eigenvectors as rows.
		return self.eigen_vectors
	def get_original_means(self):
		# returns the means for each column in the original data as a single row numpy matrix.
		return self.original_means
	def get_original_headers(self):
		# returns a copy of the list of the headers from the original data used to generate the projected data.
		return self.original_headers

# a class for clustering
class ClusterData(Data):
	def __init__(self, codebook, codes, errors):
		Data.__init__(self, filename=None) # number of clusters (IDs) and cluster means
		# mean poitns
		self.means = codebook
		self.numD = codebook
		self.rawdata = codebook
		# the category of each point
		self.IDs = codes
		# errors
		self.errors = errors
		# colors for all points
		self.colors = []
		# colors for means
		self.colors_mean = []
		self.colorsmeandic={}
		self.MDL = 0
	# assign color of datapoints
	def add_c(self, colorlist):
		for n in range(self.IDs.shape[0]):
			idx = self.IDs[n,0]
			self.colors.append(colorlist[idx])
			self.colorsmeandic[idx]=colorlist[idx]
	# assign color of only means
	def add_c_means(self):
		for meanidx in range(self.means.shape[0]):
			self.colors_mean.append(self.colorsmeandic[meanidx])
	# accessor methods
	def get_c(self):
		return self.colors
	def get_c_means(self):
		return self.colors_mean
	def get_id(self):
		return self.IDs
	def get_means(self):
		return self.means
	def get_errors(self):
		return self.errors
	def set_quality(self, MDL):
		self.MDL = MDL
	def get_quality(self):
		return self.MDL

if __name__ == "__main__":
	Data.main(sys.argv)