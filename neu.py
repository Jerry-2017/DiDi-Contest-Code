import os
import json
import time
import string
import math
import random
from numpy import matrix
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import SGD,Adadelta
from keras.models import model_from_json
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Dropout

def tail():
    global X,Yp,Y,cri
    log=open("log.txt","wb")
    layer=5
    le=len(X)
    le0=le
    Y0=[]
    X1=[]
    Y1=[]
    X2=[]
    Y2=[]
    cst=[]
    n=len(X[0])
    ml=10
    
    inputs = Input(shape=(n,))
    x = Dense(ml, activation='relu')(inputs)
    for i in xrange(layer-2):
        x=Dense(ml, activation='relu')(x)
        x=BatchNormalization(ml)(x)
        x=Dropout(p=0.5)(x)
    predictions = Dense(1, activation='softplus')(x)
    model = Model(input=inputs, output=predictions)
    sgd = Adadelta()#SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    
    psi=18*144
    pei=21*144
    po=1.0
    mxyp=0.00
    for i in xrange(len(X)):
        yp=Y[i]
        if yp>mxyp:
            mxyp=yp
        if yp!=0:# 
            Y0.append(yp)#pow(yp,-1.0*po))#math.log(yp)*po)#
        else:
            Y0.append(1.0)
    baset=0.005
    for i in xrange(le0):
        if timestamp[i]>=psi and timestamp[i]<=pei:
            #if  (timestamp[i]%144+1) in cst:#timestamp[i]-psi in cst:#timestamp[i]>=pei-145 and
            X2.append(X[i])
            Y2.append([Y[i]/mxyp+baset,])
        elif timestamp[i]<psi:#else:
            X1.append(X[i])
            Y1.append([Y0[i]/mxyp+baset,])
    print("trainer down")
    e=4
    #if os.path.exists("net.w.xml"):
    #    model=model_from_json(open("net.xml","rb").read())
    #    model.load_weights("net.w.xml")
    model.compile(loss='mape', optimizer=sgd)#mean_squared_error
    cnt=0
    while True:
        fi=open("status.txt","rb")
        if fi.read()[0]!="r":
            break
        fi.close()
        model.fit(matrix(X1), matrix(Y1), nb_epoch=5, batch_size=32)
        #score = model.evaluate(X2, Y2, batch_size=16)
        #print "score",score
        fm="net.xml"
        fm1=open(fm,"wb")
        fm1.write(model.to_json())
        fm1.close()
        try:
                os.remove("net.w.xml")
        except:
                pass
        model.save_weights("net.w.xml")
        ct=0
        er=0
        ct1=0
        for i in xrange(len(X2)):
            ct1+=1
            yp=(model.predict(matrix([X2[i]])).tolist())[0][0]
            #print yp
            if yp<=baset+1/mxyp:
               yp=1/mxyp
            else:
               yp=yp-baset
            #yp=1.0
            yp1=Y2[i][0]-baset
            #if yp<1:
            #    yp=1.0
            if yp1>0:
                er+=abs(yp1-yp)/yp1
                ct+=1
        print er/ct1,er/ct*0.636
        open("log.txt","ab").write("%f,%f"%(er/ct1,er/ct*0.636))
    open("status.txt","wb").write("r\n")
    
tail()
