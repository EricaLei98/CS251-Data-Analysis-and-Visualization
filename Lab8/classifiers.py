# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import analysis as an
import numpy as np

class Classifier:

    def __init__(self, type):
        '''The parent Classifier class stores only a single field: the type of
        the classifier.  A string makes the most sense.

        '''
        self._type = type

    def type(self, newtype = None):
        '''Set or get the type with this function'''
        if newtype != None:
            self._type = newtype
        return self._type

    def confusion_matrix( self, truecats, classcats ):
        '''Takes in two Nx1 matrices of zero-index numeric categories and
        computes the confusion matrix. The rows represent true
        categories, and the columns represent the classifier output.
        To get the number of classes, you can use the np.unique
        function to identify the number of unique categories in the
        truecats matrix.

        '''
        unique1, mapping = np.unique( np.array(truecats.T), return_inverse=True)
        unique2, mapping = np.unique( np.array(classcats.T), return_inverse=True)

        unique1 = unique1.tolist()
        unique2 = unique2.tolist()

        unique1 += unique2
        unique = np.unique(np.array(unique1)).tolist()

        confmatrix = np.matrix(np.zeros((len(unique), len(unique))))

        for i in range(truecats.shape[0]):
            confmatrix[truecats[i,0],classcats[i,0]] += 1

        return confmatrix


    def confusion_matrix_str( self, cmtx ):
        '''Takes in a confusion matrix and returns a string suitable for printing.'''

        s= "Confusion Matirx\n" + "%*s" % (len("Classified As")+18,"Classified As") +"\n"
        s += "Truth"+ "\n"
        s += '%11s' % ("")
        for i in range(cmtx.shape[1]):
            s += "%9dC" %(i,)
        s += "\n"
        for i in range(cmtx.shape[0]):
            s += "%9dT" %(i,)
            for j in range(cmtx.shape[1]):
                s += "%10d" %(cmtx[i,j],)
            s+="\n"
        return s

    def __str__(self):
        '''Converts a classifier object to a string.  Prints out the type.'''

        return str(self._type)


class NaiveBayes(Classifier):
    '''NaiveBayes implements a simple NaiveBayes classifier using a
    Gaussian distribution as the pdf.

    '''

    def __init__(self, data=None, headers=[], categories=None):
        '''Takes in a Matrix of data with N points, a set of F headers, and a
        matrix of categories, one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'Naive Bayes Classifier')
        
        # store the headers used for classification
        self.headers = headers
        # number of classes and number of features
        self.num_classes = 0
        self.num_features = 0
        # original class labels
        self.class_labels = []
        # unique data for the Naive Bayes: means, variances, scales, priors
        self.class_means = np.matrix([])
        self.class_vars = np.matrix([])
        self.class_scales = np.matrix([])
        self.class_priors = np.matrix([])

        # if given data,
            # call the build function
        if data != None:
            self.build(data.get_data(self.headers), categories)

    def build( self, A, categories ):
        '''Builds the classifier give the data points in A and the categories'''
        A = np.matrix(A)
        # figure out how many categories there are and get the mapping (np.unique)
        # unique is array of unique values, mapping is array of IDs
        unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
        self.num_classes = len(unique)
        self.num_features = A.shape[1]
        self.class_labels = unique
        # create the matrices for the means, vars, and scales
        self.class_means  = np.matrix(np.zeros((self.num_classes, self.num_features)))
        self.class_vars   = np.matrix(np.zeros((self.num_classes, self.num_features)))
        self.class_scales = np.matrix(np.zeros((self.num_classes, self.num_features)))
        self.class_priors = np.matrix(np.zeros((self.num_classes, self.num_features)))
       
        # the output matrices will be categories x features

        # compute the means/vars/scales/priors for each class
        for i in range(self.num_classes):
            SA = A[(mapping == i),:]
            self.class_means[i,:]=SA.mean(0)
            self.class_vars[i,:]=np.var(SA, axis=0, ddof=1)
        # the prior for class i will be the number of examples in class i divided by the total number of examples
            self.class_priors[i,0] = SA.size/A.size
        # store any other necessary information: # of classes, # of features, original labels
            self.class_scales[i,:] = 1/(np.sqrt(2 * np.pi * self.class_vars[i,:]))
        return

    def classify( self, A, return_likelihoods=False ):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_likelihoods
        is True, it also returns the probability value for each class, which
        is product of the probability of the data given the class P(Data | Class)
        and the prior P(Class).

        '''
        # error check to see if A has the same number of columns as the class means
        if A.shape[1] != self.class_means.shape[1]:
            print("A does not have the same number of columns as the class means")
            return
        # make a matrix that is N x C to store the probability of each class for each data point
        P = np.matrix(np.zeros((A.shape[0], self.num_classes))) # a matrix of zeros that is N (rows of A) x C (number of classes)

        # Calcuate P(D | C) by looping over the classes -> get a column of P in each loop.
        #  To compute the likelihood, use the formula for the Gaussian
        #  pdf for each feature, then multiply the likelihood for all
        #  the features together. The result should be an N x 1 column
        #  matrix that gets assigned to a column of P
        
        for i in range(self.num_classes):
            P[:,i] = np.prod(np.multiply( self.class_scales[i,:], np.exp(-np.square((A-self.class_means[i,:]))/(2*self.class_vars[i,:]) )),axis = 1)
        # Multiply the likelihood for each class by its corresponding prior
            P[:,i] = np.multiply(P[:,i], self.class_priors[i,0])
        # calculate the most likely class for each data point
        cats =np.argmax(P, axis =1)# take the argmax of P along axis 1
        # use the class ID as a lookup to generate the original labels
        labels = self.class_labels[cats]
        if return_likelihoods:
            return cats, labels, P
        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nNaive Bayes Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Mean  : ' + str(self.class_means[i,:]) + "\n"
            s += 'Var   : ' + str(self.class_vars[i,:]) + "\n"
            s += 'Scales: ' + str(self.class_scales[i,:]) + "\n"

        s += 'Prior: ' + str(self.class_priors)+"\n"
        return s
        
    def write(self, filename):
        '''Writes the Bayes classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the Bayes classifier from the file'''
        # extension
        return

    
class KNN(Classifier):

    def __init__(self, data=None, headers=[], categories=None, K=None):
        '''Take in a Matrix of data with N points, a set of F headers, and a
        matrix of categories, with one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'KNN Classifier')
        self.data = data
        # store the headers used for classification
        self.headers = headers
        # number of classes and number of features
        self.num_classes = 0
        self.num_features = 0
        # original class labels
        self.class_labels =[]
        # unique data for the KNN classifier: list of exemplars (matrices)
        self.exemplars = []
        self.class_means = np.matrix([])
        # if given data,
            # call the build function
        if data!=None:
            self.build(data.get_data(self.headers), categories)

    def build( self, A, categories, K = None ):
        '''Builds the classifier give the data points in A and the categories'''
        A = np.matrix(A)
        # figure out how many categories there are and get the mapping (np.unique)
        unique, mapping = np.unique(np.array(categories.T), return_inverse=True)
        self.num_classes = len(unique)
        self.num_features = A.shape[1]
        self.class_labels = unique

        self.class_means   = np.matrix(np.zeros((self.num_classes, self.num_features)))
        for i in range(self.num_classes):
            self.class_means[i,:] = A[(mapping==i),:].mean(0)

        #for each category i, build the set of exemplars
        for i in range(self.num_classes):
            SA = A[(mapping == i),:]
            # if K is None
            if K == None:
                # append to exemplars a matrix with all of the rows of A where the category/mapping is i
                self.exemplars.append(SA)
            # else
            else:
                # run K-means on the rows of A where the category/mapping is i
                codebook = an.kmeans_init(SA, K)
                codebook, codes, errors = an.kmeans_algorithm(SA, codebook, 0)
                # append the codebook to the exemplars
                self.exemplars.append(codebook)
        # store any other necessary information: # of classes, # of features, original labels

        return

    def classify(self, A, return_distances=False, K=3):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_distances is
        True, it also returns the NxC distance matrix. The distance is 
        calculated using the nearest K neighbors.'''

        # error check to see if A has the same number of columns as the class means
        if A.shape[1] != self.class_means.shape[1]:
            print("A does not have the same number of columns as the class means")
            return

        # make a matrix that is N x C to store the distance to each class for each data point
        D = np.matrix(np.zeros((A.shape[0],self.num_classes))) # a matrix of zeros that is N (rows of A) x C (number of classes)
        
        # for each class i
        for i in range(self.num_classes):
            # make a temporary matrix that is N x M where M is the number of examplars (rows in exemplars[i])
            temp=np.matrix(np.zeros((A.shape[0],self.exemplars[i].shape[0])))
            # calculate the distance from each point in A to each point in exemplar matrix i (for loop)
            for ex in range(self.exemplars[i].shape[0]):
                temp[:,ex]=np.sum(np.square(A - self.exemplars[i][ex,:]),axis=1)
            # sort the distances by row
            temp.sort(axis = 1)
            # sum the first K columns
            sumKcol=np.sum(temp[:,:K], axis=1)
            # this is the distance to the first class
            D[:,i]=sumKcol
        # calculate the most likely class for each data point
        cats = np.argmin(D, axis =1) # take the argmax of D along axis 1

        # use the class ID as a lookup to generate the original labels
        labels = self.class_labels[cats]

        if return_distances:
            return cats, labels, D

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nKNN Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
            s += 'Mean of Exemplars  :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

        s += "\n"
        return s


    def write(self, filename):
        '''Writes the KNN classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the KNN classifier from the file'''
        # extension
        return
    

# test function
def main(argv):
    # test function here
    if len(argv) < 3:
        print( 'Usage: python %s <training data file> <test data file> <optional training categories file> <optional test categories file>' % (argv[0]) )
        print( '    If categories are not provided as separate files, then the last column is assumed to be the category.')
        exit(-1)

    train_file = argv[1]
    test_file = argv[2]
    dtrain = data.Data(train_file)
    dtest = data.Data(test_file)


    if len(argv) >= 5:
        train_headers = dtrain.get_headers()
        test_headers = dtrain.get_headers()
        
        traincat_file = argv[3]
        testcat_file = argv[4]

        traincats = data.Data(traincat_file)
        traincatdata = traincats.get_data(traincats.get_headers())

        testcats = data.Data(testcat_file)
        testcatdata = testcats.get_data(testcats.get_headers())

    else:
        train_headers = dtrain.get_headers()[:-1]
        test_headers = dtrain.get_headers()[:-1]

        traincatdata = dtrain.get_data([dtrain.get_headers()[-1]])
        testcatdata = dtest.get_data([dtest.get_headers()[-1]])

    
    nbc = NaiveBayes(dtrain, train_headers, traincatdata )

    print( 'Naive Bayes Training Set Results' )
    A = dtrain.get_data(train_headers)
    
    newcats, newlabels = nbc.classify( A )

    uniquelabels, correctedtraincats = np.unique( traincatdata.T.tolist()[0], return_inverse = True)
    correctedtraincats = np.matrix([correctedtraincats]).T

    confmtx = nbc.confusion_matrix( correctedtraincats, newcats )
    print( nbc.confusion_matrix_str( confmtx ) )


    print( 'Naive Bayes Test Set Results' )
    A = dtest.get_data(test_headers)
    
    newcats, newlabels = nbc.classify( A )

    uniquelabels, correctedtestcats = np.unique( testcatdata.T.tolist()[0], return_inverse = True)
    correctedtestcats = np.matrix([correctedtestcats]).T

    confmtx = nbc.confusion_matrix( correctedtestcats, newcats )
    print( nbc.confusion_matrix_str( confmtx ) )

    print( '-----------------' )
    print( 'Building KNN Classifier' )
    knnc = KNN( dtrain, train_headers, traincatdata, 10 )

    print( 'KNN Training Set Results' )
    A = dtrain.get_data(train_headers)

    newcats, newlabels = knnc.classify( A )

    confmtx = knnc.confusion_matrix( correctedtraincats, newcats )
    print( knnc.confusion_matrix_str(confmtx) )

    print( 'KNN Test Set Results' )
    A = dtest.get_data(test_headers)

    newcats, newlabels = knnc.classify(A)

    # print the confusion matrix
    confmtx = knnc.confusion_matrix( correctedtestcats, newcats )
    print( knnc.confusion_matrix_str(confmtx) )

    return
    
if __name__ == "__main__":
    main(sys.argv)
