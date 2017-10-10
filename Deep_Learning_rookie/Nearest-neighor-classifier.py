#coding: utf-8
import numpy as np

class NearestNeighbor:
    def __init__(self):
        pass

    def train(self,X,y):
        '''
        X is N X D where each row is an example.
        Y is 1-dimension of size N
        :param X:
        :param y:
        :return:
        '''
        # the nearest neigbor classifier simply remebers all the training data
        self.Xtr = X
        self.ytr = y

    def predict(self,X):
        ''' X is N X D where each row is an example we wish to predict label for'''
        num_test = X.shape[0]
        # lets make sure that the output type matches the input type
        Ypred = np.zeros(num_test,dtype = self.ytr.dtype)

        #loop over all test rows
        for i in xrange(num_test):
            # find the nearest training image to the i'th test image
            # using the L1 distance(sum of absolute value differences)
            distances = np.sum(np.bas(self.Xtr - X[i:]),axis = 1)
            min_index = np.argmin(distances) # get the index with smallest distance
            Ypred[i] = self.ytr[min_index] # predict the label of the nearest example

        return Ypred


    def L_i_vectorized(self,x,y,W):
        scores = W.dot(x)              #向量相乘得到预测出的score
        margins = np.maximum(0,scores - scores[y] + 1)   # y是一个整数，代表correct score
        margins[y] = 0                 #correct score的loss为0
        loss_i = np.sum(margins)       #在所有class上求和
        return loss_i
