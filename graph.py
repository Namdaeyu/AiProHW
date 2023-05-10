import numpy as np
import math
import matplotlib.pyplot as plt
def main():
    x1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    x2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    y1 = []
    y2 = []
    for k in x1:
        ml = ML()
        fileName = "lin_train.txt"
        ml.setData('train', fileName)
        fileName = "lin_test.txt"
        ml.setData('test', fileName)
        ml.buildModel(k)
        ml.testModel()
        y1.append(ml.report())
    for k in x2:
        ml = ML()
        fileName = "nonlin_train.txt"
        ml.setData('train', fileName)
        fileName = "nonlin_test.txt"
        ml.setData('test', fileName)
        ml.buildModel(k)
        ml.testModel()
        y2.append(ml.report())
    plt.plot(x1, y1)
    plt.plot(x2, y2)
    plt.xlabel('number of k')
    plt.ylabel('value')
    plt.title('')
    plt.legend(['The best value of k for k-NN for linear data', 'The best value of k for k-NN for nonlinear data'])
    plt.show()
class ML:
    def __init__(self):
        self._trainDX = np.array([]) # Feature value matrix (training data)
        self._trainDy = np.array([]) # Target column (training data)
        self._testDX = np.array([])  # Feature value matrix (test data)
        self._testDy = np.array([])  # Target column (test data)
        self._testPy = np.array([])  # Predicted values for test data
        self._rmse= 0          # Root mean squared error
        self._aType = 0        # Type of learning algoritm
        self._w = np.array([]) # Optimal weights for linear regression
        self._k = 0            # k value for k-NN

    def setData(self, dtype, fileName): # set class variables
        XArray, yArray = self.createMatrices(fileName)
        if dtype == 'train':
            self._trainDX = XArray
            self._trainDy = yArray
        elif dtype == 'test':
            self._testDX = XArray
            self._testDy = yArray
            self._testPy = np.zeros(np.size(yArray)) # Initialize to all 0
            
    def createMatrices(self, fileName): # Read data from file and make arrays
        infile = open(fileName, 'r')
        XSet = []
        ySet = []
        for line in infile:
            data = [float(x) for x in line.split(',')]
            features = data[0:-1]
            target = data[-1]
            XSet.append(features)
            ySet.append(target)
        infile.close()
        XArray = np.array(XSet)
        yArray = np.array(ySet)
        return XArray, yArray

    def buildModel(self,k):

        aType = 2
        self._aType = aType
        if aType == 1:
            self._w = self.linearRegression()
        elif aType == 2:
            self._k = k

    def linearRegression(self): # Do linear regression and return optimal w
        X = self._trainDX
        n = np.size(self._trainDy)
        X0 = np.ones([n, 1])
        nX = np.hstack((X0, X)) # Add a column of all 1's as the first column
        y = self._trainDy
        t_nX = np.transpose(nX)
        return np.dot(np.dot(np.linalg.inv(np.dot(t_nX, nX)), t_nX), y)

    def testModel(self):
        n = np.size(self._testDy)
        if self._aType == 1:
            self.testLR(n)
        elif self._aType == 2:
            self.testKNN(n)

    def testLR(self, n): # Test linear regression with the test set
        for i in range(n):
            self._testPy[i] = self.LR(self._testDX[i])

 
    def LR(self, data): # Apply linear regression to a test data
        nData = np.insert(data, 0, 1)
        return np.inner(self._w, nData)
        
    def testKNN(self, n): # Apply k-NN to the test set
        for i in range(n):
            self._testPy[i] = self.kNN(self._testDX[i])

    ### Implement the following and other necessary methods
    def kNN(self, query):
        X = self._trainDX
        y = self._trainDy
        res=[]
        s=0
        for i in range(0,len(X)):
            d=0
            a=(query-X[i])*(query-X[i])
            for j in range(0,len(a)):
                d=d+a[j]
            res.append([math.sqrt(d),y[i]])
        res=sorted(res)
        for k in range(0,self._k):
            s=s+res[k][1]
        avg=s/self._k
        return avg
        
    def report(self):
        self.calcRMSE()
        print()
        print("RMSE: ", round(self._rmse, 2))
        return (round(self._rmse, 2))


    def calcRMSE(self):
        n = np.size(self._testDy) # Number of test data
        totalSe = 0
        for i in range(n):
            se = (self._testDy[i] - self._testPy[i]) ** 2
            totalSe += se
        self._rmse = np.sqrt(totalSe) / n


main()
