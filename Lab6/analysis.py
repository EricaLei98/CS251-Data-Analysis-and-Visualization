# Erica Lei
# CS251 Spring 2017
# project5


import data
import sys
import numpy as np
from scipy import stats

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
	print(headers)
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
def pca_svd(data, headers, normalize=True):
	# assign to A the desired data. Use either normalize_columns_separately 
	#   or get_data, depending on the value of the normalize argument.
	A = data.getNumCol(headers)
	if normalize == True:
		A = self.normalize_columns_separately(headers,data)

	# assign to m the mean values of the columns of A
	m = np.matrix( A.mean( axis=0 ) )
	# assign to D the difference matrix A - m
	D = A.copy()
	for r in range(A.shape[0]):
		D[r] = D[r] - mu
	# assign to U, S, V the result of running np.svd on D, with full_matrices=False
	(U,S,V) = np.svd(D,full_matrices=False)
	# the eigenvalues of cov(A) are the squares of the singular values (S matrix)
	#   divided by the degrees of freedom (N-1). The values are sorted.
	

	# project the data onto the eigenvectors. Treat V as a transformation 
	#   matrix and right-multiply it by D transpose. The eigenvectors of A 
	#   are the rows of V. The eigenvectors match the order of the eigenvalues.

	# create and return a PCA data object with the headers, projected data, 
	# eigenvectors, eigenvalues, and mean vector.

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

