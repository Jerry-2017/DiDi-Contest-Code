from sklearn.externals import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
import matplotlib.pyplot as plt
import os
import json
import time
import string
import math
model=RandomForestRegressor#GradientBoostingRegressor#RandomForestRegressor##DecisionTreeRegressor#RandomForestRegressor#
def prev(strg):
    sp=strg.split("-")
    if sp[3]=="1":
        sp[2]=str(int(sp[2])-1)
        sp[3]=1440
        if len(sp[2])==1:
            sp[2]="0"+sp[2]
    else:
        sp[3]=str(int(sp[3])-1)
    return "%s-%s-%s-%s"%(sp[0],sp[1],sp[2],sp[3])
def rid(str):
    i1=str.split("-")
    return (int(i1[2])-1)*1440+int(i1[3])-1
def nextt(strg):
    sp=strg.split("-")
    if sp[3]=="1440":
        sp[2]=str(int(sp[2])+1)
        sp[3]=1
        if len(sp[2])==1:
            sp[2]="0"+sp[2]
    else:
        sp[3]=str(int(sp[3])+1)
    return "%s-%s-%s-%s"%(sp[0],sp[1],sp[2],sp[3])    
def kfold():
    """k flod verification"""
    log=open("log.txt","ab")
    fold=5
    le=len(X)
    lme=int(le/fold)-2
    Yp=[None]*len(X)
    for i in xrange(len(X)):
        if Y[i]>=1:
            Yp[i]=1.0/Y[i]
        else:
            Yp[i]=1.0
    for i in xrange(4,10): #depth
        ert=0
        for j in xrange(3,4):
            X1=X[:lme*j+1]
            X1.extend(X[lme*(j+1):])
            Y1=Yp[:lme*j+1]
            Y1.extend(Yp[lme*(j+1):])
            X2=X[lme*j+1:lme*(j+1)]
            Y2=Y[lme*j+1:lme*(j+1)]
            regr = model(min_samples_leaf=int(len(X)*0.0001),n_estimators=i*5)#,n_estimators=24,n_jobs=-1)#max_depth=i)#maxdepth=i
            regr.fit(X1,Y1)
            joblib.dump(regr, "DCTree_D%d_F%d.m"%(i,j))
            er=0
            y=regr.predict(X2)
            ct=0
            for i1 in xrange(len(X2)):
                yp=1.0/y[i1]
                if yp<1:
                    yp=1.0
                if Y2[i1]>0:
                    er+=abs(yp-Y2[i1])/Y2[i1]
                    ct+=1
            er=er/ct*0.616
            print "i=",i,er
            log.write("Exp depth %d fold %d with error %f\n"%(i,j,er))
            log.flush()
            ert+=er
        ert/=fold
        log.write("Exp depth %d average error rate %f\n"%(i,ert))
        log.flush()
    log.close()
def tail():
    global Y0,X0
    X0=[]
    Y0=[]
    log=open("log.txt","ab")
    fold=1000
    le=len(X)
    le0=len(X0)
    lme=int(le/fold)*(fold-10)
    lde=int(le/fold)*(fold-50)
    for pi in xrange(1):
        po=1.0
        X0=[]
        Y0=[]
        for i in xrange(len(X)):
            vecp=X[i]
            yp=Y[i]
            if yp!=0:
                X0.append(vecp)
                Y0.append(1.0/pow(yp,po))#math.log(yp)*po)#
            else:
                X0.append(vecp)
                Y0.append(1.0)
        for per in [4,16]:
            try:
                psi=per*1440
                pei=(per+5)*(1440)
                X1=[]
                Y1=[]
                X2=[]
                Y2=[]
                for i in xrange(le):
                    if timestamp[i]>=psi and timestamp[i]<=pei:
                        X2.append(X[i])
                        Y2.append(Y[i])
                    else:
                        X1.append(X0[i])
                        Y1.append(Y0[i])
                """X1=X0[:lde]
                Y1=Y0[:lde]
                X2=X[lme:]
                Y2=Y[lme:]
                ne=19"""
                for i in [500]: #depth
                    regr = model(min_samples_leaf=int(len(X)*0.0001),max_depth=i,n_estimators=50,n_jobs=24)#,max_depth=8,n_estimators=23)
                    regr.fit(X1,Y1)
                    #joblib.dump(regr, "DCTree_D%d.m"%(i))
                #regr=joblib.load("decisiontreeregr.m")
                    er=0
                    y=regr.predict(X2)
                    ct=0
                    for i1 in xrange(len(X2)):
                        if y[i1]==0:
                            continue
                        y[i1]=1.0/pow(y[i1],po)#math.exp(y[i1]/po)#
                        if y[i1]<1:
                            y[i1]=1
                        if Y2[i1]>0:
                            er+=abs(y[i1]-Y2[i1])/Y2[i1]
                            ct+=1
                    er=er/ct*0.616
                    print er
                    log.write("Exp depth %d with error %f pow %f startstamp %d endstamp %d\n"%(i,er,po,psi,pei))
                    log.flush()
                log.flush()
                thre=1
            except Exception,e:
                print e
    """
    for i in xrange(1,1000,): #depth
        #regr = model(max_depth=i)#n_estimators=ne,max_depth=8)
        #regr.fit(X1,Y1)
        #joblib.dump(regr, "DCTree_D%d.m"%(i))
    #regr=joblib.load("decisiontreeregr.m")
        er=0
        #y=regr.predict(X2)
        ct=0
        for i1 in xrange(len(X2)):
            ypp=thre
            if ypp<1:
                ypp=1
            if Y2[i1]>0:
                er+=(ypp-Y2[i1])*(ypp-Y2[i1])/(Y2[i1]*Y2[i1])
                ct+=1
        er=math.sqrt(er/ct)
        print er
        log.write("Exp all %f with error %f\n"%(thre,er))
        log.flush()
        thre+=0.0001"""
    log.flush()
    log.close()
def train():
     Y0=[]
     for i in xrange(len(X)):
         vecp=X[i]
         yp=Y[i]
         if yp!=0:
             Y0.append(1.0)#math.log(yp)*po)#
         else:
             Y0.append(0.0)
     for i in xrange(1):
         le=len(X)
         regr = model(min_samples_leaf=int(len(X)*0.0001),n_estimators=40)#,n_jobs=-1,max_depth=10,n_estimators=100)#n_estimators=20,
         regr.fit(X,Y0)
         name="rv-GBDT-D3-T40.m"
         joblib.dump(regr, name)
         predict(name)
    
def predict(name):
    regr1=joblib.load(name)
    fo=open("result%s.csv"%(name),"wb")
    regr1=joblib.load(name)
    Sam_t1=[]
    for i in Sam_t:
        Sam_t1.append(i+"0")
    for i in xrange(len(Xt)):
        if Mt[i][0] in Sam_t1:
            pr=regr1.predict([Xt[i],])[0]
            pr=1.0/pr
            if (pr<1):
                pr=1
            fo.write("%d,%s,%f\n"%(int(eval(Mt[i][1])),nextt(Mt[i][0][:-1]),pr))
    fo.close()
    y=regr1.predict(X)
    er=0
    ct=0
    """for i1 in xrange(len(X)):
        y[i1]=1/pow(y[i1],0.6)
        if y[i1]<1:
            y[i1]=1
        if Y[i1]>0:
            er+=(y[i1]-Y[i1])*(y[i1]-Y[i1])/(Y[i1]*Y[i1])
            ct+=1
    er=math.sqrt(er/ct)
    print er"""
print(rid("2016-2-1-1"))
print(rid("2016-2-2-3"))
tail()
#kfold()
#train()
#
#train()
#predict("RDCV-Reduced-D10-06.m")
