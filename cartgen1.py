import CART
import os
from random import randint
#import lr
def steep(val,X):
    global ovt
    thred=2.5
    bias=-1
    for i in xrange(7,len(mx)):
        if (mi[i]==100000):
            bias=i
            break
    x1=X[-1]*(mx[bias-1]-mi[bias-1])+mi[bias-1]
    x2=X[-13]*(mx[bias-13]-mi[bias-13])+mi[bias-13]
    x3=X[-25]*(mx[bias-25]-mi[bias-25])+mi[bias-25]
    mean=(x1+x2+x3)/3.0
    #print x1,x2,x3,val
    if mean<1:
        mean=1
    if val>mean*thred:
        val=mean
        ovt+=1
     #   print "up overflow %d"%(ovt)
    if val<mean/thred:
        val=mean/thred
        #ovt+=1
      #  print "down overflow %d"%(ovt)
    f=int(math.floor(val))
    bound=2.0*f*(f+1)/(2*f+1)
    if val<(bound-f)/2+f:
        val=f*1.0
    return val
def predict(base,name):
    global tr
    fo=open(base+"%s.csv"%(name),"wb")
    for i in xrange(len(Xt)):
        if Mt[i][0] in Sam_t:
            pr=tr.predict(Xt[i])
            #pr=pow(pr,-1.0/po)
            if (pr<1):
                pr=1
            pr=steep(pr,Xt[i])
            fo.write("%s,%s,%f\n"%(int(eval(Mt[i][1])),nextt(Mt[i][0]),pr))
    fo.close()
reload(CART)
#reload(lr)
name="0616-n2-d20-100-v0.1-SN0.0001-SV-0.01-PC100"
tn=2
X0=[None]*len(X)
Y0=[None]*len(X)
for i in xrange(len(X)):
    X0[i]=X[i]
    if Y[i]==0:
        Y0[i]=1
    else:
        Y0[i]=Y[i]
    Y0[i]=Y0[i]#1.0/Y0[i]
ovt=0
for i in xrange(len(X)):
    tp=randint(i,len(X)-1)
    _t=X0[i]
    X0[i]=X0[tp]
    X0[tp]=_t
    _t=Y0[i]
    Y0[i]=Y0[tp]
    Y0[tp]=_t
fold=5
er_tot=0
for i in xrange(fold):
    tr=CART.GBDT(tn,20,140000,StopVal=0.05,StopNum=0.001,precision=100)
    X1=[]
    Y1=[]
    psi=1440*21*i/fold
    pei=1440*21*(i+1)/fold
    part=len(X)/fold
    for i1 in xrange(0,len(X)):
        if timestamp[i1]<psi or timestamp[i1]>pei:
            X1.append(X0[i1])
            Y1.append(Y0[i1])
    for i1 in xrange(0,len(X)):
        if timestamp[i1]>psi and timestamp[i1]<pei:
            X1.append(X0[i1])
            Y1.append(Y0[i1])
    lp=part*(fold-1)
    X11=[]
    Y11=[]
    for i1 in xrange(int(len(X0)*0.2)):
        _ch=randint(0,lp)
        X11.append(X1[_ch])
        Y11.append(Y1[_ch])
    if True:
        tr.LoadData(X11,Y11)
        ff=True
        for i2 in xrange(tn):
            fn="gbdt%s%d_fold%d.m"%(name,i2,i)#
            if i2==0:
                bf=True
            else:
                bf=False
            if os.path.exists(fn) :
                tr.loadfromfile(i2,fn)
                #tr.RTree[i2].F_LR=bf
                print "load"
            else:
                ff=False
                tr.TreeBuilder(i2)
                tr.savetofile(i2,fn)
    er=0.0
    ct=0
    ct1=0
    #    predict("","RegTree-10-N")
    print "?"
    print len(X1),part,fold,part*fold
    for i1 in xrange(lp,len(X1)):
        y=tr.predict(X1[i1])
        #y=steep(y,X0[i])
        ct1+=1
        #y=1.0/y
        if y<1:
            y=1
        if Y1[i1]>0:
            er+=abs(Y1[i1]-y)/Y1[i1]
            ct+=1
    print "error",er/ct*0.636,er/ct1
    fo=open("log.txt","ab")
    fo.write("%s %d %f\n"%(name,i,er/ct*0.616))
    fo.close()
print "error",er_tot/fold
