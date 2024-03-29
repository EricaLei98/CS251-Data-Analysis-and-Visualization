# Erica Lei
# CS251 Spring 2017
# lab5

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
		self.header2col = {}
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
	def get_raw_headers(self):
		return self.headers
	# return a list of numeric headers
	def get_num_headers(self):
		return self.num_headers

	# returns a list of all types
	def get_raw_types(self):
		return self.types
	# returns a list of numeric types
	def get_num_types(self):
		return self.num_types
	#returns the number of columns
	def get_num_dimensions(self):
		return self.rawdata.shape[1]

	#returns the number of "numeric matrix" columns
	def get_numeric_dimensions(self):
		return self.numD.shape[1]

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
	def get_type(self, headers):
		t = 0
		for i in headers:
			v = self.get_value(headers[i],0)
			if self.determine(v) == float:
				t=1
			else:
				t=-1
		if t==1:
			return "numeric"

		else:
			return "string"

	# takes in a list of columns headers,
	# returns a Numpy atrix with the data for all rows 
	# but just the specified columns.
	def getCol(self, headers):
		indexes = []
		for item in headers:
			indexes.append(self.header2col[item])

		return self.rawdata[:,indexes]	

	def getNumCol(self, headers):
		indexes = []
		for item in headers:
			indexes.append(self.num_header2col[item])

		return self.numD[:,indexes]	
	
	#EXTENSION
	def addColumn(self, header, type, data):
		# make sure right points
		if len(data) != self.numD.shape[0]:
			print("new col points do not match")
		else:
			# update header, dict
			self.headers.append(header)
			self.header2col[header] = len(self.headers)+1
			# update types
			self.types.append(type)
			# update rawdata
			d = np.array(data)
			self.rawdata=np.hstack((self.rawdata,d))
			# if appropriate, update numD 
			self.numD = self.get_numeric_data(self.rawdata)


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

if __name__ == "__main__":
	Data.main(sys.argv)