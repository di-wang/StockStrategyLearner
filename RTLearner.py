"""
A simple wrapper for RT
"""

import numpy as np
import random as rd



 ## Authoor:Di Wang
# gt username: dwang383
import numpy as np
import pandas as pd
class RTLearner:
    def __init__(self,leaf_size,verbose =False):
        self.leaf_size = leaf_size


    def author(self):
        return 'dwang383'

    def addEvidence(self,Xtrain,Ytrain):
        self.dt = self.buildtree(Xtrain,Ytrain)
        # print self.dt

    def query(self,Xtest):
        output = Xtest.copy()
        output[output.columns.values[0] +'_holding'] = output.apply(self.singlequery,axis = 1)
        output.ix[-1,output.columns.values[0] +'_holding'] = 0

        return output[[output.columns.values[0] +'_holding']]

    def singlequery(self,sigXtest):
        i = 0
        while (True):
            if sigXtest[self.dt[i][0]] <= self.dt[i][1] :
                i += self.dt[i][2]
            else:
                i += self.dt[i][3]
            if self.dt[i][0] == 'leaf':
                return self.dt[i][1]


    def getrandomweights(self,Xtrain,Ytrain):
        cors = []
        for i in range(Xtrain.shape[1]):
            cors.append(np.random.uniform())
        return cors

    def getsplitfeature(self,Xtrain,Ytrain):
        corlist = map(abs,self.getrandomweights(Xtrain,Ytrain))
        return corlist.index(np.nanmax(corlist))

    def issameY(self,Ytrain):
        temp = Ytrain.mean()
        for i in Ytrain:
            if i != temp:
                return False
        return True

    def smallerthanmed(self,Xtrain,bestf):
        med = np.median(Xtrain.ix[:,bestf])
        for i in Xtrain.ix[:,bestf]:
            if i > med:
                return False
        return True
    def find_mode(self, Ytrain):
        count = {}
        for i in Ytrain:
            if i in count:
                count[i]+= 1
            else:
                count[i] = 1
        return max(count, key=count.get)

    def buildtree(self,Xtrain,Ytrain):

        if Xtrain.shape[0] <= self.leaf_size:
            return [['leaf',self.find_mode(Ytrain),'','']]
        if self.issameY(Ytrain):
            return [['leaf',self.find_mode(Ytrain),'','']]
        else:
            bestf = self.getsplitfeature(Xtrain,Ytrain)
            SplitVal = np.median(Xtrain.ix[:,bestf]) if (not self.smallerthanmed(Xtrain,bestf)) else np.mean(Xtrain.ix[:,bestf])
	    if (len(Xtrain) == len(Xtrain.ix[Xtrain.ix[:,bestf] <= SplitVal])|(len(Xtrain) == 0)):
		return [['leaf',self.find_mode(Ytrain),'','']]
            lefttree = self.buildtree(Xtrain.ix[Xtrain.ix[:,bestf]<=SplitVal],Ytrain[Xtrain.ix[:,bestf]<=SplitVal])
            righttree = self.buildtree(Xtrain.ix[Xtrain.ix[:,bestf]>SplitVal],Ytrain[Xtrain.ix[:,bestf]>SplitVal])
            root = [bestf,SplitVal,1,len(lefttree)+1]
            return ([root]+lefttree+righttree)



    def author(self):
        return 'dwang383'  # replace tb34 with your Georgia Tech username

    def addEvidence1(self, X, Y):
        """
                @summary: Add training data to learner
                @param dataX: X values of data to add
                @param dataY: the Y training values
                """

        # slap on 1s column so linear regression finds a constant term
        # newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        # newdataX[:, 0:dataX.shape[1]] = dataX

        # build and save the model

        # self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
        # **********set a trivial dataset and build the tree and print
        def built_tree(dataX, dataY):
            leaf = -1  # negative flag that never be changed during building tree process
            if dataX.shape[0] <= self.leaf_size:
                self.model = np.asarray([[leaf, np.mean(dataY), np.nan, np.nan]])
                return self.model
            elif len(set(dataY)) == 1:
                self.model = np.asarray([[leaf, np.mean(dataY), np.nan, np.nan]])
                return self.model
            else:
                #***************** here is main different, random select the feature for spliting
                i = rd.randint(0, dataX.shape[1]-1)
                #***************** here is main different, random select the feature for spliting



                SplitVal = np.mean(dataX[:, i])
                leftTree = built_tree(dataX[dataX[:, i] <= SplitVal], dataY[dataX[:, i] <= SplitVal])
                rightTree = built_tree(dataX[dataX[:, i] > SplitVal], dataY[dataX[:, i] > SplitVal])
                root = [i, SplitVal, 1, len(leftTree) + 1]
                self.model = np.vstack((root, leftTree, rightTree))
                # print "this is  the tree", build_tree(data)
                # print "this is  the tree"
                return self.model

        return built_tree(X, Y)

    def query1(self, points):
        """
                @summary: Estimate a set of test points given the model we built.
                @param points: should be a numpy array with each row corresponding to a specific query.
                @returns the estimated values according to the saved model.
                """
        current = 0
        size = points.shape[0]  # scan all rows and traveres the model to find its end node
        predict = np.empty([size])

        # loop thru all point and predict
        while current < size:
            index = 0
            while ~np.isnan(self.model[index, 3]):
                # check if it falls on end leaf node, if not, jump the row noted in index 3 and index 4, left or right tree
                val = self.model[index, 1]
                if points[current, int(self.model[index, 0])] <= val:
                    index = index + 1
                else:
                    index = index + int(self.model[index, 3])
            predict[current] = self.model[index, 1]
            current = current + 1
        return predict


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

