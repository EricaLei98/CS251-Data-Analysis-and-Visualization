# Erica Lei
# CS251 Spring 2017
# Lab exercise 2

import csv 
import numpy

# read csv file
class Data:

	def __init__(self, filename = None):

		if filename != None:
			self.read(filename)

	def read(self, filename):
		# list of all headers
		self.headers = []
		# list of all types
		self.types = []
		# list of lists, each sublist corresponds to a row of the data CSV file.
		self.rows = []
		# dictionary mapping a header to its corresponding column)
		self.header2col = {}

		fp = open(filename,'rU')
		csv_reader = csv.reader(fp)

		line = next(csv_reader)
		for header in line:
			# remove white space from before and after the string
			header.strip()
			self.headers.append(header)

		for i in range(len(self.headers)):
			self.header2col[self.headers[i]] = i

		line = next(csv_reader)
		for onetype in line:
			onetype.strip()
			self.types.append(onetype)
		

		# for line in csv_reader:
			# self.rows.append([float(x) for x in line])
			#equi to
		for line in csv_reader:
			newLis = []
			for x in line:
				readIn = float(x)
				newLis.append(readIn)
			self.rows.append(newLis)

		self.data = numpy.matrix(self.rows)

	#returns a list of all of the headers.
	def get_headers(self):
		return self.headers

	# returns a list of all types
	def get_types(self):
		return self.types

	#returns the number of columns
	def get_num_dimensions(self):
		return self.data.shape[1]

	#returns the number of points/rows in the data set
	def get_num_points(self):
		return self.data.shape[0]

	# returns the specified row as a NumPy matrix
	def get_row(self, rowIndex):
		return self.data[rowIndex]

	# returns the specified value in the give column
	def get_value(self, header, rowIndex):
		return self.data[ rowIndex, self.header2col[header]]


## need:
# Write a __str__ method for your Data class that 
# nicely prints out the data to the command line. 
# You may want to make it sensitive to 
# the number of rows/columns and print only a subset 
# if there are too many dimensions or data ponts.
