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
def predict():
    path=""
    base=""
    name="neupr-0.265"
    path="net-layer5-bias0.001500-ml10-best"
    po=1.0
    mxyp=0.00
    beta=0.8
    baset=0.0015
    sgd = Adadelta()
    for i in xrange(len(X)):
        yp=Y[i]
        if yp>mxyp:
            mxyp=yp
    if os.path.exists("%s.w.xml"%path):
        model=model_from_json(open("%s.xml"%path,"rb").read())
        model.load_weights("%s.w.xml"%path)
    #model.compile(loss='mape', optimizer=sgd)#mean_squared_error
    global tr
    fo=open(base+"%s.csv"%(name),"wb")
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
predict()
