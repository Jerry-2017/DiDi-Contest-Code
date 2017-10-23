import os
from datetime import *
import json
import time
import string 

def norm(strg):
    r=int(time.mktime(time.strptime(strg,"%Y-%m-%d %H:%M:%S")))
    bias=int(time.mktime(time.strptime("2000-01-01 00:00:00","%Y-%m-%d %H:%M:%S")))
    mark=int((int(r-bias)%(86400))/600)
    mark+=1
    ltime=time.localtime(r)
    timeStr=time.strftime("%Y-%m-%d", ltime)
    week=(int(time.strftime("%w",ltime))+6)%7
    timeStr+="-%d"%(mark)
    return timeStr,str(mark),str(week+1)
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
def prev(strg):
    sp=strg.split("-")
    if sp[3]=="1":
        sp[2]=str(int(sp[2])-1)
        sp[3]=144
        if len(sp[2])==1:
            sp[2]="0"+sp[2]
    else:
        sp[3]=str(int(sp[3])-1)
    return "%s-%s-%s-%s"%(sp[0],sp[1],sp[2],sp[3])
def process(di,key,mode=1):
    data={}
    global sfeature,metric,metriccnt,district_id
    if mode==-2:
        sfeature=[]
    cnt=0
    for i in os.listdir(".\\%s\\"%(di)):
        if os.path.isfile(".\\%s\\%s"%(di,i)) and i[0]!='.':
            print ".\\%s\\%s"%(di,i)
            fi=open(".\\%s\\%s"%(di,i),"rb")
            if mode==1:  
                for line in fi: #calculate
                    line=line.strip()
                    cnt+=1
                    #if cnt>15:
                    #    break
                    datatp=[]
                    for j in line.split("\t"):
                        datatp.append(j)
                    #print datatp
                    tm,mark,week=norm(datatp[6])
                    #print tm
                    if not data.has_key(datatp[3]): # 0 order start 1 order accept 2 order to 3 order to accept
                        data[datatp[3]]={}
                    if not data[datatp[3]].has_key(tm):
                        data[datatp[3]][tm]=[0]*4
                    if not data.has_key(datatp[4]):
                        data[datatp[4]]={}
                    if not data[datatp[4]].has_key(tm):
                        data[datatp[4]][tm]=[0]*4
                    data[datatp[3]][tm][0]+=1
                    data[datatp[4]][tm][2]+=1 ##the time relation and space relation dosnt reflect here!!
                    if not datatp[1]=="NULL":
                        data[datatp[3]][tm][1]+=1
                        data[datatp[4]][tm][3]+=1
                    #MDS
                    if district_id.has_key(datatp[3]) and district_id.has_key(datatp[4]):
                        s=int(district_id[datatp[3]])
                        d=int(district_id[datatp[4]])
                        metric[s][d]+=string.atof(str(datatp[5]))
                        metriccnt[s][d]+=1
            elif mode==2:
                for line in fi:
                    line=line.replace("\n","")
                    datatp=[]
                    for j in line.split("\t"):
                        datatp.append(j)
                    data[datatp[0]]=datatp[1]
            elif mode==5:
                for line in fi:
                    line=line.replace("\n","")
                    datatp=[]
                    for j in line.split("\t"):
                        datatp.append(j)
                    data[datatp[1]]=datatp[0]
            elif mode==-2:
                for line in fi:
                    line=line.replace("\n","")
                    datatp=[]
                    for j in line.split("\t"):
                        datatp.append(j)
                    data[datatp[0]]={}
                    for j in datatp[1:]:
                        sp=j.split(":")
                        #print sp[0],sp[1]
                        data[datatp[0]][sp[0]]=sp[1]
                        if sp[0] not in sfeature:
                           # print "add"
                            sfeature.append(sp[0])
            elif mode==3:
                for line in fi:
                    line=line.replace("\n","")
                    datatp=[]
                    for j in line.split("\t"):
                        datatp.append(j)
                    datatp[0],mark,week=norm(datatp[0])
                    data[datatp[0]]=datatp[1:]
                    data[datatp[0]].append(mark)
                    data[datatp[0]].append(week)
            elif mode==4:
                for line in fi:
                    line=line.replace("\n","")
                    datatp=[]
                    for j in line.split("\t"):
                        datatp.append(j)
                    datatp[5]=datatp[5].strip()
                    datatp[5],mark,week=norm(datatp[5])
                    data[datatp[5]+datatp[0]]=datatp
    return data

def builddataset(start,time_peri): ##enhance by adding 2 extra field
    global sfeature,district_id,metric,metriccnt,mds
    poi=process("poi_data",["district_hash","poi_class"],-2)
    district_id=process("cluster_map",["district_hash","district_id"],2)
    district_rid=process("cluster_map",["district_hash","district_id"],5)
    weather=process("weather_data",["time","weather","temperature","pm2.5"],3)
    traffic=process("traffic_data",["district_hash","tj_level","tj_time"],4)
    count=process("order_data",["order_id","driver_id","passenger_id","start","ends","price","time"],1)
    """ disttrict_hash tj_level_1..2..3..4 tj_time order_start_from order_start_accept order_to mark dustrict_id poi_class weather temperature pm2.5 """
    #print sfeature
    fo=open("metric.txt","wb")
    fo.write(json.dumps(metric)+"\n")
    fo.write(json.dumps(metriccnt)+"\n")
    fo.close()
    fo=open("dataset.txt","wb")
    nearest=[0]*1000
    for j in xrange(len(mds)):
        dis=100000.0
        for i in xrange(len(mds)):
            if i!=j:
                ditt=pow(pow(mds[i][0]-mds[j][0],2)+pow(mds[i][1]-mds[j][1],2),0.5)
                if ditt<dis:
                    dis=ditt
                    nrst=i
        nearest[j+1]=nrst
            
    for k1 in district_id:
        if not district_id.has_key(k1):
            continue
        tj_time=start
        ps_tr=[None]*4
        for k2 in xrange(time_peri):
            kk=tj_time+k1
            district_hash=k1
            output=[]
            if traffic.has_key(kk):
                traffic_item=traffic[kk]
                tj_level1=traffic_item[1].split(":")[1]
                tj_level2=traffic_item[2].split(":")[1]
                tj_level3=traffic_item[3].split(":")[1]
                tj_level4=traffic_item[4].split(":")[1]
            else:
                tj_level1=None
                tj_level2=None
                tj_level3=None
                tj_level4=None
            order_start_from=0
            order_start_accept=0
            order_to=0
            order_to_accept=0
            gap=0
            if count.has_key(district_hash) and count[district_hash].has_key(tj_time):
                count[district_hash][tj_time]
                order_start_from=count[district_hash][tj_time][0]
                order_start_accept=count[district_hash][tj_time][1]
                order_to=count[district_hash][tj_time][2]
                order_to_accept=count[district_hash][tj_time][3]
                nt=nextt(tj_time)
                gap=0
                if count[district_hash].has_key(nt):
                    gap=count[district_hash][nt][0]-count[district_hash][nt][1]
            if district_id.has_key(district_hash):
                did=district_id[district_hash]
            else:
                did=None
            if weather.has_key(tj_time):
                weth=weather[tj_time][0]
                tempa=weather[tj_time][1]
                pm2=weather[tj_time][2]
            else:
                weth=None
                tempa=None
                pm2=None
            tm_n=tj_time.split("-")
            
            st1,markp,week=norm("%s-%s-%s 00:01:00"%(tm_n[0],tm_n[1],tm_n[2]))
            markp=tm_n[3]
            out=[district_hash,tj_time,int(did),int(gap),int(did),tj_level1,tj_level2,tj_level3,tj_level4,int(order_start_from),int(order_start_accept),int(order_to),int(order_to_accept),weth,tempa,pm2,int(markp),int(week)]
            for i in xrange(len(out)):
                if i>=2 and out[i]!=None:
                    out[i]=string.atof(str(out[i]))
            if not poi.has_key(district_hash):
                poi[district_hash]={}
            out.append(mds[int(did)-1][0])
            out.append(mds[int(did)-1][1])
            mds_hash=district_rid[str(nearest[int(did)])]
            nrst_gap=0
            if count.has_key(mds_hash) and count[mds_hash].has_key(tj_time):
                nrst_gap=count[mds_hash][tj_time][0]-count[mds_hash][tj_time][1]
            out.append(nrst_gap*1.0)

            for i in sfeature:
                if poi[district_hash].has_key(i):
                    if poi[district_hash][i]==None:
                        j=None
                    else:
                        j=string.atof(poi[district_hash][i])
                else:
                    j=0
                out.append(j)
            if ps_tr[0]!=None:
                out.extend(ps_tr[1][3:15])
                out.extend(ps_tr[0][3:15])
                out.extend([ps_tr[0][9]-ps_tr[0][10],])
                out.extend([ps_tr[1][3]+ps_tr[0][3]+ps_tr[0][9]-ps_tr[0][10],])
                fo.write(json.dumps(out)+"\n")
            tj_time=nextt(tj_time)
            ps_tr[0]=ps_tr[1]
            ps_tr[1]=out
    fo.flush()

metric= [[0.0 for col in range(67)] for row in range(67)]
metriccnt= [[0 for col in range(67)] for row in range(67)]
fs=open("position.txt","rb")
mds=json.loads(fs.read())
fs.close()
print len(mds)
builddataset("2016-01-01-1",144*21)
os.chdir(".\\test_set_1")
builddataset("2016-01-22-1",144*9)
#print count
#print norm("2016-01-15 00:35:11")
