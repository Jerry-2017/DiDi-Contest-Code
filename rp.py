import os
import random
import CART

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
        #print "up overflow %d"%(ovt)
    if val<mean/thred:
        val=mean/thred
        #ovt+=1
        #print "down overflow %d"%(ovt)
    f=int(math.floor(val))
    bound=2.0*f*(f+1)/(2*f+1)
    if val<(bound-f)/2+f:
        val=f*1.0
    return val
def predict(base,name):
    global tr
    fo=open(base+"%s.csv"%(name),"wb")
    Sam_t1=[]
    l1=len(Xt[0])
    for i in Sam_t:
        Sam_t1.append(i+"0")
    for i in xrange(len(Xt)):
        if Mt[i][0] in Sam_t1:
            if len(Xt[i])!=l1:
                print Xt[i]
            pr=tr.predict(Xt[i])
            #print Xt[i]
            #pr=pow(pr,-1.0)
            if (pr<1):
                pr=1
            #pr=steep(pr,Xt[i])
            fo.write("%s,%s,%f\n"%(int(eval(Mt[i][1])),nextt(Mt[i][0][:-1]),pr))
    fo.close()
reload(CART)
random.seed()
aa=random.randint(1,1000)
print aa
for tn in [250]:
    name="0616-rand-rs-rand%d"%aa
    tr=CART.randomforest(tn,500,1000000,0.0,StopVal=0.0005,StopNum=0.00001,precision=500,Samplerate=1,Samplefeature=14)
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

    """for i in xrange(len(X)):
        tp=random.randint(i,len(X)-1)
        _t=X0[i]
        X0[i]=X0[tp]
        X0[tp]=_t
        _t=Y0[i]
        Y0[i]=Y0[tp]
        Y0[tp]=_t"""
    lp=int(len(X0))
    if True:
        #tr.LoadData(X0,Y0,Xt)
        #for i in xrange(tn):
        fn="rs.m"
        #    if os.path.exists(fn):
        tr.loadfromfile(fn)
                
        #    else:
        #        tr.TreeBuilder(i)
        #        tr.savetofile(fn)
    er=0.0
    ct=0
    ct1=0
    print "pr"
    predict("","RegTree-du-N2")
    print "?"
    #X0=X
    #Y0=Y
    """ for i in xrange(lp,len(X)):#
        y=tr.predict(X0[i])
        #y=steep(y,X0[i])
        ct1+=1
        #y=1.0/y
        if y<1:
            y=1
        if Y[i]>0:
            er+=abs(Y0[i]-y)/Y0[i]
            ct+=1
    print "Tree num",tn,"error",er/ct*0.636,er/ct1"""

