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
def nextt(strg):
    sp=strg.split("-")
    if sp[3]=="144":
        sp[2]=str(int(sp[2])+1)
        sp[3]=1
        if len(sp[2])==1:
            sp[2]="0"+sp[2]
    else:
        sp[3]=str(int(sp[3])+1)
    return "%s-%s-%s-%s"%(sp[0],sp[1],sp[2],sp[3])
def steep(val):
    global ovt
    thred=2.5
    f=int(math.floor(val))
    bound=2.0*f*(f+1)/(2*f+1)
    if val<(bound-f)/2+f:
        val=f*1.0
    return val

def tail():
    bestv=1000
    path="net-layer7-bias0.1"
    global X,Yp,Y,cri
    log=open("log.txt","wb")
    layer=3
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
    beta=0.9
    baset=0.0003
    mtd="sigmoid"
    path="net-layer%d-bias%f-ml%d"%(layer,baset,ml)
    inputs = Input(shape=(n,))
    x = Dense(ml, activation='relu')(inputs)
    for i in xrange(layer-2):
        x=Dense(ml, activation='sigmoid')(x)
        #x=BatchNormalization(ml)(x)
        #x=Dropout(p=0.5)(x)
    predictions = Dense(1, activation=mtd)(x)
    model = Model(input=inputs, output=predictions)
    sgd = Adadelta()#SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    psi=14*144
    pei=21*144
    po=1.0
    mxyp=0.00
    for i in xrange(len(X)):
        yp=Y[i]
        if yp>mxyp:
            mxyp=yp
        if yp>0:#
            Y0.append(yp)#pow(yp,-1.0*po))#math.log(yp)*po)#
        else:
            Y0.append(1.0)
    for i in xrange(le0):
        if timestamp[i]>=psi and timestamp[i]<=pei:
            #if  (timestamp[i]%144+1) in cst:#timestamp[i]-psi in cst:#timestamp[i]>=pei-145 and
            X2.append(X[i])
            Y2.append([Y0[i]*beta/mxyp+baset,])
        elif timestamp[i]<psi:#else:
            X1.append(X[i])
            Y1.append([Y0[i]*beta/mxyp+baset,])
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
        model.fit(matrix(X1), matrix(Y1), nb_epoch=10, batch_size=32)
        score = model.evaluate(X2, Y2, batch_size=16)
        print "score",score
        fm="%s.xml"%(path)
        fm1=open(fm,"wb")
        fm1.write(model.to_json())
        fm1.close()
        try:
                os.remove("%s.w.xml"%path)
        except:
                pass
        model.save_weights("%s.w.xml"%path)
        ct=0
        er=0
        ct1=0
        mean=0
        var=0
        for i in xrange(len(X2)):
            ct1+=1
            yp=(model.predict(matrix([X2[i]])).tolist())[0][0]
            #print yp
            if yp<=baset+1*beta/mxyp:
               yp=1/mxyp*beta
            else:
               yp=yp-baset
            #yp=1.0
            yp1=Y2[i][0]-baset
            if yp1>0:
                er+=abs(yp1-yp)/yp1
                ct+=1
            else:
                print yp1
        mean=er/ct
        var=0
        for i in xrange(len(X2)):
            yp=(model.predict(matrix([X2[i]])).tolist())[0][0]
            #print yp
            if yp<=baset+1*beta/mxyp:
               yp=1/mxyp*beta
            else:
               yp=yp-baset
            #yp=1.0
            yp1=Y2[i][0]-baset
            if yp1>0:
                var+=(abs(yp1-yp)/yp1-mean)*(abs(yp1-yp)/yp1-mean)
        print er/ct1,er/ct*0.636,"mean",math.sqrt(var),mean+math.sqrt(var/ct)
        if mean+math.sqrt(var/ct)<bestv:
            print "accept"
            bestv=mean+math.sqrt(var/ct)
            fm="%s-best.xml"%(path)
            fm1=open(fm,"wb")
            fm1.write(model.to_json())
            fm1.close()
            try:
                    os.remove("%s-best.w.xml"%path)
            except:
                    pass
            model.save_weights("%s-best.w.xml"%path)
            fo=open("result.csv","wb")
            for i in xrange(len(Xt)):
                if Mt[i][0] in Sam_t:
                    yp=(model.predict(matrix([Xt[i]])).tolist())[0][0]
                    #print yp
                    if yp<=baset+1*beta/mxyp:
                       yp=1.0/mxyp*beta
                    else:
                       yp=yp-baset
                    #yp=1.0
                    yp=yp/beta*mxyp
                    yp=steep(yp)
                    fo.write("%s,%s,%f\n"%(int(eval(Mt[i][1])),nextt(Mt[i][0]),yp))
            fo.close()
        open("logn.txt","ab").write("bias:%f beta:%d layer:%d width:% realerror%f displayerror:%f method:%s\n"%(baset,beta,layer,ml,er/ct1,er/ct*0.636,mtd))
    open("status.txt","wb").write("r\n")

tail()
