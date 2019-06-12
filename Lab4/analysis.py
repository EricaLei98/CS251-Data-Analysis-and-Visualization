# Erica Lei
# CS251 Spring 2017
# Project 4 Integrating Data and Viewing
# due March 12

import data
import sys
import numpy as np


# returns a list of 2-element lists with min and max for each col
def data_range(headers, data):
	selected = data.getNumCol(headers)
	mins = selected.min(0)
	minlist = [[mins[0,0]],[mins[0,1]]]

	maxs = selected.max(0)
	maxlist = [[maxs[0,0]],[maxs[0,1]]]

	minnmax = np.hstack((minlist, maxlist))
	return minnmax

# returns a list of the mean values for each column
def mean(headers, data):

	return data.getNumCol(headers).mean(0)

# returns a list of the standard deviation for each specified column
def stdev(headers, data):
	selected = data.getNumCol(headers)
	sdlist = []
	for i in range(selected.shape[1]):
		col =  selected[:,i]
		
		sdlist.append(np.std(col))
	return sdlist

# returns a matrix with each column normalized
# so its minimum value is mapped to 0 and 
# its maximum value is mapped to 1.       (x-min)/(max-min)
def normalize_columns_separately(headers, data):
	selected = data.getNumCol(headers)
	minval = np.min(selected, axis = 0)
	maxval = np.max(selected, axis = 1)
	extent = maxval-minval
	result= (selected-minval)/extent

	return result

# returns a matrix with each entry normalized 
# so that the minimum value (of all the data in this set of columns) 
# is mapped to 0 and its maximum value is mapped to 1.
def normalize_columns_together(headers, data):
	selected = data.getNumCol(headers)
	extent = selected.max() - selected.min()
	r = (selected - selected.min())/extent
	return r

# returns the sums of each col
def sumCol(headers,data):
	selected = data.getNumCol(headers)
	return np.sum(selected,axis = 0)

# retuns a number, sum of all elements
def sumTotal(headers,data):
	selected = data.getNumCol(headers)
	return np.sum(selected)

# returns a list of 25 percent of the range of each col
def perc25(headers,data):
	selected = data.getNumCol(headers)
	pc = np.percentile(selected, 25, axis=0)
	return pc

