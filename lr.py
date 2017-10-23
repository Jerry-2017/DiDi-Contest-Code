exit
import pca
import linearregression
reload(pca)
reload(linearregression)
PCA=pca.PCA
LinearRegression=linearregression.LinearRegression
import random
import json
from numpy import matrix


class pca_calc:
    def __init__(self):
        self.Kernel=None
    def train(self,Data,components=1):
        pca=PCA(n_components=components)
        pca.fit(matrix(Data))
        self.setkernel(pca.components_,pca.mean_)
    def setkernel(self,kernel,mean):
        self.Kernel=matrix(kernel).transpose()
        self.mean=mean
    def trans(self,X):
        m1=matrix(X-self.mean)
        return (m1*self.Kernel).tolist()[0]
    def getdata(self):
        pcadata={"kernel":self.Kernel.tolist(),"mean":self.mean.tolist()}
        return pcadata
    def setdata(self,pcadata):
        self.Kernel=matrix(pcadata["kernel"])
        self.mean=matrix(pcadata["mean"])
class linear_calc:
    def __init__(self,maxnode):
        self.maxnode=maxnode
        self.coef=[None]*maxnode
        self.intercept=[None]*maxnode
    def train(self,Node,Data,Mark):
        lin=LinearRegression(fit_intercept=True)
        lin.fit(matrix(Data),matrix(Mark).transpose())
        self.coef[Node]=lin.coef_.tolist()[0]
        self.intercept[Node]=lin.intercept_.tolist()[0][0]
    def predict(self,Node,Data):
        sum=self.intercept[Node]
        for j in xrange(len(self.coef[Node])):
            sum+=self.coef[Node][j]*Data[j]
        return sum
    def getdata(self):
        return {"coef":self.coef,"intercept":self.intercept}
    def setdata(self,data):
        self.coef=data["coef"]
        self.intercept=data["intercept"]
if __name__=="__main__":
    T1=X[:30]
    pcam=pca_calc()
    pcam.train(X,25)
    X1=[]
    for i in xrange(len(T1)):
        X1.append(pcam.trans(T1[i]))
    print "done"
    li=linear_calc(10)
    json.dumps(pcam.getdata())
    print "done"
    print len(X1),len(Y),len(X1[0])
    li.train(1,X1,Y[:30])

