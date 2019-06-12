# Erica Lei
# CS251 Spring 2017
# project6


import data
import sys
import random
import numpy as np
from scipy import stats
import scipy.cluster.vq as vq
import scipy.spatial.distance as dt

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
	data.get_num_headers()
	selected = data.getNumCol(headers)
	minval = np.min(selected, axis = 0)
	maxval = np.max(selected, axis = 0)
	extent = maxval-minval
	result= (selected-minval)/extent

	return result

# returns a matrix with each entry normalized 
# so that the minimum value (of all the data in this set of columns) 
# is mapped to 0 and its maximum value is mapped to 1.
def normalize_columns_together(headers, data):
	data.get_num_headers()
	selected = data.getNumCol(headers)
	extent = selected.max() - selected.min()

	r = (selected - selected.min())/extent
	return r

# returns the sums of each col
def sumCol(headers,data):
	selected = data.getNumCol(headers)
	return np.sum(selected,axis = 0)

# retuns a number, sum of all ele(ments
def sumTotal(headers,data):
	selected = data.getNumCol(headers)
	return np.sum(selected)

# returns a list of 25 percent of the range of each col
def perc25(headers,data):
	selected = data.getNumCol(headers)
	pc = np.percentile(selected, 25, axis=0)
	return pc
# do a single liner regression
def single_linear_regression(data, ind_var, dep_var):
	selected = data.getNumCol([ind_var,dep_var]).T

	slope, intercept, r_value, p_value, std_err = stats.linregress(selected)

	minind = np.min(selected, axis = 1)[0,0]
	mindep = np.min(selected, axis = 1)[1,0]
	maxind = np.max(selected, axis = 1)[0,0]
	maxdep = np.max(selected, axis = 1)[1,0]
	return (slope, intercept, r_value, p_value, std_err, minind, mindep, maxind, maxdep)

# takes in the data set, a list of headers for the independent variables, and a single header (not in a list) for the dependent variable
def linear_regression(data, ind, dep):
	y=data.getNumCol([dep])
	A=data.getNumCol(ind)
	A = np.hstack((A,A.shape[0]*[[1]])) # The matrix A.T * A is the covariancde matrix of the independent data
	AAinv = np.linalg.inv( np.dot(A.T, A)) #  the covariancde matrix of the independent data 
	x = np.linalg.lstsq( A, y ) # solves the equation y = Ab	
	b = x[0] # the solution that provides the best fit regression
	N = y.shape[0] # rows of y = number of data points 
	C = b.shape[0] # rows of b = number of coefficients
	df_e = N-C # number of degrees of freedom of the error
	df_r = C-1 # number of degrees of freedom of the model fit (if you have C-1 of the values of b you can find the last one)
	# the error of the model prediction
	error =  y - np.dot(A, b)
	# the sum squared error,
	sse = np.dot(error.T, error) / df_e
	# the standard error
	stderr = np.sqrt( np.diagonal( sse[0, 0] * AAinv ) ) # a Cx1 vector.
	# t-statistic
	t= b.T / stderr
	#the probability of the coefficient indicating a random relationship (slope = 0)
	p= 2*(1 - stats.t.cdf(abs(t), df_e)) 
	#the r^2 coefficient indicating the quality of the fit.
	r2 = 1 - error.var() / y.var()
	# Return the values of the m0, m1, fit (b), the sum-squared error, the
	#     R^2 fit quality, the t-statistic, and the probability of a
	#     random relationship.
	return (x[0][0,0],x[0][1,0], b[2,0], sse, r2, t, p)

# EXTENSION -- USED FOR REGRESSION PLANE
def linear_regression_extension(data, ind, dep):
	A=data.getNumCol(ind)
	y=data.getNumCol([dep])
	minind1 = A[:,0].min()
	minind2 = A[:,1].min()
	mindep = np.min(y)
	maxind1 = A[:,0].max()
	maxind2 = A[:,1].max()
	maxdep = np.max(y)

	A = np.hstack((A,A.shape[0]*[[1]])) 
	AAinv = np.linalg.inv( np.dot(A.T, A)) 
	x = np.linalg.lstsq( A, y ) 
	b = x[0] 
	N = y.shape[0]  
	C = b.shape[0] 
	df_e = N-C 
	df_r = C-1 
	error =  y - np.dot(A, b)
	sse = np.dot(error.T, error) / df_e
	stderr = np.sqrt( np.diagonal( sse[0, 0] * AAinv ) ) # a Cx1 vector.
	t= b.T / stderr
	p= 2*(1 - stats.t.cdf(abs(t), df_e)) 
	r2 = 1 - error.var() / y.var()

	# Return the values of the m0, m1, fit (b), minind1, minind2, mindep, maxind2,maxind2, maxdep, r2
	return (b[0,0],b[1,0], b[2,0],minind1, minind2, mindep, maxind2,maxind2, maxdep, r2)

# take in a list of column headers and 
# return a PCAData object with 
# the projected data, eigenvectors, eigenvalues, source data means, and source column headers stored in it.
# This version uses SVD

def pca(d, headers, normalize=True):
	# assign to A the desired data. Use either normalize_columns_separately 
	#   or getNumCol, depending on the value of the normalize argument.	
	if normalize == True:
		A = normalize_columns_separately(headers,d)
	else:
		A = d.getNumCol(headers)
	# assign to m the mean values of the columns of A
	m = A.mean(axis = 0)
	# assign to D the difference matrix A - m
	D = A - m
	# assign to U, S, V the result of running np.svd on D, with full_matrices=False
	U,S,V = np.linalg.svd(D,full_matrices=False)
	# the eigenvalues of cov(A) are the squares of the singular values (S matrix)
	#   divided by the degrees of freedom (N-1). The values are sorted.
	eigvals = np.square(S)/(D.shape[0]-1)

	# project the data onto the eigenvectors. Treat V as a transformation 
	#   matrix and right-multiply it by D transpose. The eigenvectors of A 
	#   are the rows of V. The eigenvectors match the order of the eigenvalues.
	eigvecs = V
	pdata = (V*D.T).T

	# create and return a PCA data object with the headers, projected data, 
	# eigenvectors, eigenvalues, and mean vector.
	pcad = data.PCAData(pdata, eigvecs, eigvals, m, headers)
	return pcad

'''
# This version calculates the eigenvectors of the covariance matrix
def pca(d, headers, normalize=True):
	# assign to A the desired data. Use either normalize_columns_separately 
	#   or getNumCol, depending on the value of the normalize argument.
	A = d.getNumCol(headers)
	if normalize == True:
		A = normalize_columns_separately(headers,d)

	# assign to C the covariance matrix of A, using np.cov with rowvar=False
	C = np.cov(A, rowvar = False)
	# assign to W, V the result of calling np.eig
	W, V = np.linalg.eig(C)
	# sort the eigenvectors V and eigenvalues W to be in descending order. At 
	#   the end of this process, the eigenvectors should be a matrix V with 
	#   each eigenvector as a row of the matrix.
	idx = np.argsort(W)[::-1]
	W = W[idx]
	V = V[:,idx].T
	eigvals = W
	eigvecs = V
	
	# assign to m the mean values of the columns of A
	m = np.matrix(A.mean(axis = 0))
	# assign to D the difference matrix A - m
	D = A-m
	# project the data onto the eigenvectors. Treat V as a transformation 
	#   matrix and right-multiply it by D transpose. 

	pdata =(V*D.T).T
	# create and return a PCA data object with the headers, projected data, 
	# eigenvectors, eigenvalues, and mean vector.
	return data.PCAData(pdata, eigvecs, eigvals, m, headers)
'''

#Takes in a Data object, a set of headers, and the number of clusters to create.
#Computes and returns the codebook, codes, and representation error. Uses Numpy's built-in k-means function.
def kmeans_numpy( d, headers, K, whiten = True):
	A = d.getNumCol(headers)
	W = vq.whiten(A)
	codebook, bookerror = vq.kmeans(W,K)
	codes, error = vq.vq(W,codebook)
	return (codebook, codes, error)

# take in the data, the number of clusters K 
# and return a numpy matrix with K rows, each one repesenting a cluster mean.
def kmeans_init(A,K):
	S = A.shape[0]
	N = A.shape[1] # dimension
	idx = list(range(S))
	random.shuffle(idx)
	new = np.empty((0,N)) # an empty matrix to hold means
	for i in range(K):
		try:
			index = idx[i]
			row = A[index,:]
			new = np.vstack((new,row))
		except IndexError:
			print("K > # data points")
			break

	return new

# Given a data matrix A and a set of means in the codebook
# Returns a matrix of the id of the closest mean to each point
# Returns a matrix of the sum-squared distance between the closest mean and each point
def kmeans_classify(A, codebook, metric=0):
	print("Distance Metric = ", metric)
	N = A.shape[0]
	min_idx = []
	min_ds =[]
	K = codebook.shape[0] #how many means
	# Hint: you can compute the difference between all of the means and data point i using: 
	for i in range(N):
		temp = [] # the list of distances to each mean
		diff = codebook - A[i,:]
		diff2 = np.square(diff)
		for j in range(K):
			sum = np.sum(diff2[j,:])
			d = np.sqrt(sum)
			temp.append(d)
		# for j in range(K): #each method
		# 	if metric == 0:
		# 		dist = dt.euclidean(A[i,:],codebook[j,:])
		# 	elif metric == 1:
		# 		dist = dt.cityblock(A[i,:],codebook[j,:])
		# 	elif metric == 2:
		# 		dist = dt.correlation(A[i,:],codebook[j,:])
		# 	elif metric == 3:
		# 		dist = dt.hamming(A[i,:],codebook[j,:])
		# 	elif metric == 4:
		# 		dist = dt.cosine(A[i,:],codebook[j,:])
		# 	temp.append(dist)
		temp = np.matrix(temp)
		min_d = np.min(temp)
		min_ds.append([min_d])
		min_index = np.argmin(temp)
		min_idx.append([min_index])
	min_idx = np.matrix(min_idx)
	min_ds = np.matrix(min_ds)

	return (min_idx, min_ds)
# Given a data matrix A and a set of K initial means, compute the optimal
# cluster means for the data and an ID and an error for each data point
def kmeans_algorithm(A, means):
	# set up some useful constants
	MIN_CHANGE = 1e-7     # might want to make this an optional argument
	MAX_ITERATIONS = 100  # might want to make this an optional argument
	D = means.shape[1]    # number of dimensions
	K = means.shape[0]    # number of clusters
	N = A.shape[0]        # number of data points

	# iterate no more than MAX_ITERATIONS
	for i in range(MAX_ITERATIONS):
		# calculate the codes by calling kemans_classify
		# codes[j,0] is the id of the closest mean to point j
		codes, errors = kmeans_classify(A, means)

		# initialize newmeans to a zero matrix identical in size to means
		# Meaning: the new means given the cluster ids for each point
		newmeans = np.zeros_like(means)

		# initialize a K x 1 matrix counts to zeros
		# Meaning: counts will store how many points get assigned to each mean
		counts = np.zeros((K,1))
		# for the number of data points
			# add to the closest mean (row codes[j,0] of newmeans) the jth row of A
			# add one to the corresponding count for the closest mean
		for j in range(N):
			newmeans[codes[j,0],:] += A[j,:]
			counts[codes[j,0],:] += 1.0
		# finish calculating the means, taking into account possible zero counts
		#for the number of clusters K
			# if counts is not zero, divide the mean by its count
			# else pick a random data point to be the new cluster mean
		for k in range(K):
			if counts[k,0]>0.0:
				newmeans[k,:] /= counts[k,0]
			else:
				newmeans[k,:] = A[random.randint(0, A.shape[0]),:]
		# test if the change is small enough and exit if it is
		diff = np.sum(np.square(means - newmeans))
		means = newmeans
		if diff < MIN_CHANGE:
			break

	# call kmeans_classify one more time with the final means
	codes, errors = kmeans_classify( A, means )

	# return the means, codes, and errors
	return (means, codes, errors)

# Takes in a Data object, a set of headers, and the number of clusters to create
# Computes and returns the codebook, codes and representation errors. 
def kmeans(d, headers, K, whiten=True ): 
	# assign to A the result getting the data given the headers
	A = d.getNumCol(headers)
	# if whiten is True
	  # assign to W the result of calling vq.whiten on the data
	# else
	  # assign to W the matrix A
	if whiten:
		W = vq.whiten(A)
	else:
		W = A
	# assign to codebook the result of calling kmeans_init with W and K
	codebook = kmeans_init(W,K)
	# assign to codebook, codes, errors, the result of calling kmeans_algorithm with W and codebook        
	codebook, codes, errors = kmeans_algorithm(W, codebook)
	# return the codebook, codes, and representation error
	return codebook, codes, errors


def main(argv):

	if len(argv) < 4:
		print("Usage: python %s <data file> <independent header> <dependent header>")
		exit(-1)

	# read some data
	data_obj = data.Data( argv[1] )
	ind_headers = (argv[2],argv[3])
	dep_header = argv[4]

	# call the linear regression function
	results = linear_regression( data_obj, ind_headers, dep_header)

	# print out the results

	print("m0:  ",results[0])
	print("m1:  ", results[1])
	print("b:  ", results[2])
	print("SSE:  ", (results[3]))
	print("R2:  ", (results[4]) )
	print("t-value:  ", (results[5]) )
	print("p-value:  ", (results[6]) )
	# results = linear_regression_extension( data_obj, ind_headers, dep_header)
	# print(results)
	return


if __name__ == "__main__":
	main(sys.argv)

