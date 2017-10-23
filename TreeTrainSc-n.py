import os
import json
import time
import string
import math

task=""
descriptor=""
base=""
def tasklog():
    global base
    fo=open("./Record/tasklog.txt","ab")
    fo.write("\nTaskName=%s Time=%s\nTaskContent=%s\n"%(task,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),descriptor))
    fo.close()
    if not os.path.exists("./Record/%s"%(task)):
        os.mkdir("./Record/%s"%(task))
    base="./Record/%s/"%(task)
def log(strg):
    fo=open("./Record/tasklog.txt","ab")
    fo.write(strg+"\r\n")
    fo.close()
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
def regular_read():
    global X,Y,mi,mx,avg,timestamp
    avgc=[0]*1000
    avg=[0]*1000
    mx=[0]*1000
    mi=[100000]*1000
    timestamp=[]
    X=[]
    X0=[]
    Y0=[]
    Y=[]
    if not os.path.exists("mxmi.txt"):
        fi=open("dataset.txt","rb")
        for i in fi:
            vec=json.loads(i)
            f=True
            vecp=[]
            cnt=0
            for i in vec:
                cnt+=1
                if cnt<=4:
                    continue
                if i==None:
                    continue
                if i>mx[cnt]:
                    mx[cnt]=i
                if i<mi[cnt]:
                    mi[cnt]=i
        fo=open("mxmi.txt","wb")
        for i in xrange(500):
            fo.write("%f %f\n"%(mx[i],mi[i]))
        fi.close()
        fo.close()
    else:
        fi=open("mxmi.txt","rb")
        cnt=-1
        for i in fi:
            cnt+=1
            j=i.split()
            if len(j)<2:
                continue
            mx[cnt]=string.atof(j[0])
            mi[cnt]=string.atof(j[1])
        fi.close()
    fi=open("dataset.txt","rb")
    for i1 in fi:
        vec=json.loads(i1)
        f=True
        vecp=[]
        cnt=0
        for i in vec:
            cnt+=1
            if (cnt==2):
                sti=i
            if (cnt==3 or cnt>4) and i==None:
                f=False
                break
            if (cnt==4):
                yp=i
            if cnt<=4:
                continue
            avg[cnt]+=i
            avgc[cnt]+=1
            if mx[cnt]-mi[cnt]<1e-4:
                vecp.append(0)#mi[cnt])
            else:
                vecp.append((i-mi[cnt])/(mx[cnt]-mi[cnt]))
        if f: 
            timestamp.append(rid(sti))
            X.append(vecp)
            Y.append(yp)
    fi.close()
    for i in xrange(1000):
        if avgc[i]>0:
            avg[i]=avg[i]/avgc[i]
def test_read():
    fi=open("./test_set_1/dataset.txt","rb")
    global Xt,Mt,mi,mx,Sam_t
    Xt=[]
    Mt=[]
    Y=[]
    for i in fi:
        vec=json.loads(i)
        f=True
        vecp=[]
        tp=[]
        cnt=0
        for i in vec:
            cnt+=1
            if (cnt==2 or cnt==3):
                tp.append(str(i))
            if (cnt==3 or cnt>4) and i==None:
                vecp.append(avg[cnt])
                continue
            if (cnt==3):
                yp=i
            if cnt<=4:
                continue
            if mx[cnt]-mi[cnt]<1e-4:
                vecp.append(0)
            else:
                vecp.append((i-mi[cnt])/(mx[cnt]-mi[cnt]))
        if f:
            Xt.append(vecp)
            Mt.append(tp)
    fi.close()    
    fi=open("preinput.txt","rb")
    Sam_t=[]
    for i in fi:
        i=i.strip()
        i=prev(i)
        Sam_t.append(i)
    fi.close()

def schedule():
    while (True):
        f=raw_input("FileName:")
        if len(f)<=3:
            f="model.py"
        try:
            execfile(f,globals())
        except Exception,e:
            print e
            continue
regular_read()
test_read()
schedule()
