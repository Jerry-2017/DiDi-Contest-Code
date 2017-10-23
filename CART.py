from random import randint
from random import random
from math import log
import math
#import lr
import json
import os
import csplit
pd=0
DebugFile="Debug.txt"
class TreeRegressor:
    def __init__(self,depth=10,maxnode=1024*1024,Validation=0.1,StopVal=0.01,StopNum=0.001,precision=300):
        self.__Test__=False
        self.Depth=depth
        self.Data=[]
        #self.pcam=lr.pca_calc()
        #self.lrm=lr.linear_calc(1)
        self.Node=[None]*maxnode
        self.vCond=[None]*maxnode
        self.iCond=[None]*maxnode
        self.pVal=[None]*maxnode
        self.Validation=Validation
        self.precision=precision
        self._StopNum=StopNum
        self.lNode=0
        self.StopVal=StopVal
        self.PCAComponents=2
    def entropy(self,lnum,rnum):
        _sum=float(lnum+rnum)
        _lp=lnum/_sum
        _rp=rnum/_sum
        _v=0
        if lnum!=0:
            _v-=_lp*log(_lp)
        if rnum!=0:
            _v-=_rp*log(_rp)
        if _v==0:
            _v=0.001
        return _v
    def Error(self,Predict,Real,Base):
        """ Calculate the given property"""
        if Base==0:
            return 0.0
        else:
            return (abs(Predict-Real)/Base)#abs(Predict-Real)/Base#
    def LoadData(self,TData,TMark,TBase,TTest,LR=True):
        nSample=len(TData)
        assert(nSample!=0)
        assert(nSample==len(TMark))
        nFeature=len(TData[0])
        for i in xrange(len(TData)):
            assert(nFeature==len(TData[i]))
        self.TData=[]
        self.TMark=[]
        self.TBase=[]
        self.TTest=TTest
        self.ValidData=[]
        self.ValidMark=[]
        self.ValidBase=[]
        self.Data=range(nSample)
        for i in xrange(nSample):
            _temp=randint(i,nSample-1)
            _temp1=self.Data[_temp]
            self.Data[_temp]=self.Data[i]
            self.Data[i]=_temp1
        bound=int(nSample*(1-self.Validation))
        self.nTrain=bound
        self.nValid=nSample-bound
        for i in xrange(bound):
            self.TData.append(TData[self.Data[i]])
            self.TMark.append(TMark[self.Data[i]])
            self.TBase.append(TBase[self.Data[i]])
        for i in xrange(bound,nSample):
            self.ValidData.append(TData[self.Data[i]])
            self.ValidMark.append(TMark[self.Data[i]])
            self.ValidBase.append(TBase[self.Data[i]])
        self.split=csplit.cpack(self.TData,self.TMark)
        if LR:
            print "LR"
            self.pcam=lr.pca_calc()
            self.pcam.train(TData,self.PCAComponents)
            #nFeature=self.PCAComponents
            #for i in xrange(bound):
            #    self.TData[i]=self.pcam.trans(self.TData[i])
            #for i in xrange(nSample-bound):
            #    self.ValidData[i]=self.pcam.trans(self.ValidData[i])

        if self.__Test__==True:
            print "Data",self.Data
            print "TData",self.TData
            print "TMark",self.TMark
            print "ValidData",self.ValidData
            print "ValidMark",self.ValidMark
        self.nSample=nSample
        self.nTest=len(self.TTest)
        self.nFeature=nFeature
        self.StopNum=int(self._StopNum*self.nTrain)
        print "StopNum",self.StopNum
    def TreeBuilder(self,Node=0,Partion=None,TPartion=None,Depth=1):
        global pd
        print "Build Node",Node
        if Node==0:
            Partion=range(self.nTrain)
            TPartion=range(self.nTest)
        if len(TPartion)==0:
            self.iCond[Node]=-1
            return
        assert(Partion!=None)
        _nTrain=len(Partion)
        _cfeature=-1
        _cthreshold=-1
        _copterr=-1
        _clpartion=[]
        _crpartion=[]
        _tsum=0.0
        _toterr=0.0
        _lnm=0
        _rnm=0
        __lnm=0
        __rnm=0
        __temp=[]
        _ic=-1 #move the inner par outside to make it efficient
        for j in xrange(_nTrain):
            _tsum+=self.TMark[Partion[j]]
        for j in xrange(_nTrain):
            _toterr+=self.Error(_tsum/_nTrain,self.TMark[Partion[j]],self.TBase[Partion[j]])
        if self.__Test__:
            print "Node %d "%Node,"Partion=",Partion," nFeature",self.nFeature
        _cfeature,_cthreshold,_lerr,_rerr,_pp,__lnm,__rnm=self.split.best(Partion)
        _copterr=_lerr+_rerr
        print "Node",Node,"Feature:",_cfeature," Threshold:",_cthreshold," error:",_copterr,"toterr",_toterr,"lnum",__lnm,"rnum",__rnm
        assert(_nTrain!=0)
        self.pVal[Node]=(_tsum)/_nTrain
        if len(TPartion)==0:
            return
        if Depth<self.Depth:
            self.iCond[Node]=_cfeature
            if _cfeature!=-1 and __lnm>self.StopNum and __rnm>self.StopNum and _nTrain>self.StopNum and _toterr!=0 and (_copterr==0 or (_toterr-_copterr)/_copterr>self.StopVal):
                _clpartion=[]
                _crpartion=[]
                for l in xrange(_nTrain):
                    if self.TData[Partion[l]][_cfeature]<=_cthreshold:
                        _clpartion.append(Partion[l])
                    else:
                        _crpartion.append(Partion[l])
                _nTest=len(TPartion)
                _ctlpartion=[]
                _ctrpartion=[]
                for l in xrange(_nTest):
                    if self.TTest[TPartion[l]][_cfeature]<=_cthreshold:
                        _ctlpartion.append(TPartion[l])
                    else:
                        _ctrpartion.append(TPartion[l])
                self.vCond[Node]=_cthreshold
                self.Node[Node]=[self.lNode+1,]
                self.lNode+=1
                self.TreeBuilder(self.lNode,_clpartion,_ctlpartion,Depth+1)
                self.Node[Node].append(self.lNode+1)
                self.lNode+=1
                self.TreeBuilder(self.lNode,_crpartion,_ctrpartion,Depth+1)
            else:
                if _copterr!=0 and self.StopVal>(_toterr-_copterr)/_copterr and _nTrain>1000:
                    dfn=open(DebugFile,"ab")
                    #for i in xrange(len(__temp)):
                        #dfn.write("%d %d %lf %lf %lf\n"%(Node,_cfeature,__temp[i][0],__temp[i][1],self.TMark[__temp[i][0]]))
                    dfn.close()
                self.iCond[Node]=-1
        else:
            self.iCond[Node]=-1
    def releasemem(self):
        self.Data=None
        self.TData=None
        self.TMark=None
        self.ValidData=None
        self.ValidMark=None
        self.TBase=None
        self.ValidBase=None
        self.TotData=None
        self.TTest=None
        self.TotMark=None
        self.split=None
    def postprune(self,Node=0,Partion=None):
        if Node==0:
            Partion=range(self.nValid)
        _lpartion=[]
        _rpartion=[]
        _nValid=len(Partion)
        _cFeature=self.iCond[Node]
        _vThreshold=self.vCond[Node]
        _pVal=self.pVal[Node]
        _lerr=0
        _rerr=0
        _terr=0
        _myflag=False
        #if _nValid==0:
        #    self.iCond[Node]=-1
        #    _myflag=True
        if _cFeature==-1:
            _myflag=True
            for i in xrange(_nValid):
                _cm=self.ValidMark[Partion[i]]
                _cbase=self.ValidBase[Partion[i]]
                _terr+=self.Error(_pVal,_cm,_cbase)
        else:
            for i in xrange(_nValid):
                _cv=self.ValidData[Partion[i]][_cFeature]
                _cm=self.ValidMark[Partion[i]]
                _cbase=self.ValidBase[Partion[i]]
                if _cv<_vThreshold:
                    _lpartion.append(Partion[i])
                    _lerr+=self.Error(_pVal,_cm,_cbase)
                else:
                    _rpartion.append(Partion[i])
                    _rerr+=self.Error(_pVal,_cm,_cbase)
            _terr=_lerr+_rerr
            _lchild=self.Node[Node][0]
            _rchild=self.Node[Node][1]
            _lterr,_lflag=self.postprune(_lchild,_lpartion)
            _rterr,_rflag=self.postprune(_rchild,_rpartion)
            if _lflag and _rflag and _lterr+_rterr>_terr:
                self.iCond[Node]=-1
                _myflag=True
            #print _lterr,_rterr,_terr
        if _myflag:# and self.__Test__:
            print "Postprune",Node
        return _terr,_myflag
    def predict(self,Data):
        #print "predict",len(Data),self.nFeature
        #assert(len(Data)==self.nFeature)
        _cnode=0
        while (self.iCond[_cnode]!=-1):
            _icond=self.iCond[_cnode]
            _vcond=self.vCond[_cnode]
            if (Data[_icond]<=_vcond):
                __cnode=self.Node[_cnode][0]
            else:
                __cnode=self.Node[_cnode][1]
            #if self.iCond[__cnode]==-1:
            #    return self.pVal[_cnode]
            _cnode=__cnode
           #print "node",_cnode,"cond:",_icond,"threshold",_vcond
        if (self.checklr()): #take reverse to make more accurate for small number
            return math.exp(self.lrm.predict(_cnode,self.pcam.trans(Data)))
        else:
            return self.pVal[_cnode]
    def savetofile(self,FileName):
        struct={"Node":self.Node[:self.lNode+1],"vCond":self.vCond[:self.lNode+1],"iCond":self.iCond[:self.lNode+1],"pVal":self.pVal[:self.lNode+1],"Validation":self.Validation,"nFeature":self.nFeature,"lNode":self.lNode}
        if self.checklr():
            struct["pca"]=self.pcam.getdata()
            struct["lr"]=self.lrm.getdata()
            struct["F_LR"]=True
        file=open(FileName,"wb")
        file.write(json.dumps(struct))
        file.close()
    def loadfromfile(self,FileName):
        #struct={"Node":self.Node[:self.lNode+1],"vCond":self.vCond[:self.lNode+1],"iCond":self.iCond[:self.lNode+1],"pVal":self.pVal[:self.lNode+1],"Validation":self.Validation,"nSample":self.nSample,"nFeature":self.nFeature,"lNode":self.lNode}
        file=open(FileName,"rb")
        struct=json.loads(file.read())
        #print struct
        file.close()
        self.Node=struct["Node"]
        self.vCond=struct["vCond"]
        self.iCond=struct["iCond"]
        self.pVal=struct["pVal"]
        self.Validation=struct["Validation"]
        self.nFeature=struct["nFeature"]
        self.lNode=struct["lNode"]
        if struct.has_key("F_LR") and struct["F_LR"]==True:
            self.F_LR=True
            self.pcam.setdata(struct["pca"])
            self.lrm.setdata(struct["lr"])
    def checklr(self):
        if hasattr(self,"F_LR") and self.F_LR==True:
            return True
        else:
            return False
    def LR(self,Partion=None,Node=0):
        if Node==0:
            if self.checklr():
                return
            self.lrm=lr.linear_calc(self.lNode+1)
            Partion=range(len(self.TData))
            self.F_LR=True
        if self.iCond[Node]==-1:
            _X=[]
            _Y=[]
            for i in Partion:
                _X.append(self.pcam.trans(self.TData[i]))
                if self.TMark[i]==0:
                    _Y.append(0.0)
                else:
                    _Y.append(math.log(self.TMark[i]))
            self.lrm.train(Node,_X,_Y)
        else:
            _lpartion=[]
            _rpartion=[]
            _cfeature=self.iCond[Node]
            _threshold=self.vCond[Node]
            _num=len(Partion)
            for i in Partion:
                if self.TData[i][_cfeature]<_threshold:
                    _lpartion.append(i)
                else:
                    _rpartion.append(i)
            self.LR(_lpartion,self.Node[Node][0])
            self.LR(_rpartion,self.Node[Node][1])

class GBDT:
    def __init__(self,Tree=2,depth=10,maxnode=1024*1024,Validation=0.1,StopVal=0.03,StopNum=0.001,precision=300):
        self.Depth=depth
        self.RTree=[None]*Tree
        self.nTree=Tree
        self.Progress=0
        for i in xrange(Tree):
            self.RTree[i]=TreeRegressor(depth,maxnode,Validation,StopVal,StopNum,precision)
    def loadfromfile(self,TreeId,filename):
        assert(self.Progress>=TreeId)
        assert(TreeId<self.nTree)
        self.RTree[TreeId].loadfromfile(filename)
        print "check",self.RTree[TreeId].checklr()
        if TreeId+1>self.Progress:
            self.Progress=TreeId+1
    def savetofile(self,TreeId,filename):
        assert(self.Progress>=TreeId)
        assert(TreeId<self.nTree)
        self.RTree[TreeId].savetofile(filename)
    def LoadData(self,Data,Mark):
        self.Data=Data
        self.Mark=Mark
        self.prdVal=[]
        self.nSample=len(Data)
        for i in xrange(self.nTree):
            self.prdVal.append([None]*self.nSample)
    def TreeBuilder(self,TreeId,LR=False):
        assert(self.Progress>=TreeId)
        assert(TreeId<self.nTree)
        if TreeId+1>self.Progress:
            self.Progress=TreeId+1
        if TreeId==0:
            tMark=self.Mark
        else:
            tMark=[0.0]*self.nSample
            for i in xrange(TreeId):
                _rtree=self.RTree[i]
                for j in xrange(self.nSample):
                    if self.prdVal[i][j]==None:
                        self.prdVal[i][j]=_rtree.predict(self.Data[j])
                    tMark[j]-=self.prdVal[i][j]
            for i in xrange(self.nSample):
                tMark[i]+=self.Mark[i]
        self.RTree[TreeId].LoadData(self.Data,tMark,self.Mark,LR)
        self.RTree[TreeId].TreeBuilder()
        self.RTree[TreeId].postprune()
        if LR:
            self.RTree[TreeId].LR()
        self.RTree[TreeId].releasemem()
    def LR(self):
        TreeId=self.Progress-1
        if TreeId==0:
            tMark=self.Mark
        else:
            tMark=[0.0]*self.nSample
            for i in xrange(TreeId):
                _rtree=self.RTree[i]
                for j in xrange(self.nSample):
                    if self.prdVal[i][j]==None:
                        self.prdVal[i][j]=_rtree.predict(self.Data[j])
                    tMark[j]-=self.prdVal[i][j]
            for i in xrange(self.nSample):
                tMark[i]+=self.Mark[i]
        self.RTree[TreeId].LoadData(self.Data,tMark,self.Mark)
        self.RTree[TreeId].LR()
        print "check",self.RTree[TreeId].checklr()
        self.RTree[TreeId].releasemem()
    def releasemem(self):
        for i in xrange(self.Progress):
            self.RTree[i].releasemem()
    def predict(self,Data):
        _tmark=0.0
        for i in xrange(self.Progress):
            _tmark+=self.RTree[i].predict(Data)
        return _tmark

class randomforest:
    def __init__(self,Tree,depth=3,maxnode=40,Validation=0.1,StopVal=0,StopNum=0,precision=300,Samplerate=1,Samplefeature=7):
        self.Depth=depth
        self.RTree=[None]*Tree
        self.nTree=Tree
        self.Progress=0
        self.Samplerate=Samplerate
        self.SampleFeature=Samplefeature
        self.chFeature=[None]*Tree
        for i in xrange(Tree):
            self.RTree[i]=TreeRegressor(depth,maxnode,0,StopVal,StopNum,precision)
    def LoadData(self,Data,Mark,Test):
        self.Data=Data
        self.Test=Test
        self.nSample=len(Data)
        self.nTest=len(Test)
        self.nFeature=len(Data[0])
        if self.SampleFeature>self.nFeature:
            self.SampleFeature=self.nFeature
        self.Mark=Mark
    def TreeBuilder(self,TreeId):
        self.progress=TreeId
        _SampleNum=int(self.nSample*self.Samplerate)
        _chFeature=range(self.nFeature)
        for i in xrange(self.SampleFeature):
            _sp=randint(i,self.nFeature-1)
            _tp=_chFeature[_sp]
            _chFeature[_sp]=_chFeature[i]
            _chFeature[i]=_tp
        _chFeature=_chFeature[:self.SampleFeature]
        self.chFeature[TreeId]=_chFeature
        _X=[]
        _Y=[]
        for i in xrange(_SampleNum):
            _chosen=randint(0,self.nSample-1)
            _tpdata=[]
            for j in _chFeature:
                _tpdata.append(self.Data[_chosen][j])
            _X.append(_tpdata)
            _Y.append(self.Mark[_chosen])
        _T=[]
        for i in xrange(self.nTest):
            _tpdata=[]
            for j in _chFeature:
                _tpdata.append(self.Test[i][j])
            _T.append(_tpdata)
        self.RTree[TreeId].LoadData(_X,_Y,_Y,_T,False)
        self.RTree[TreeId].TreeBuilder()
        self.RTree[TreeId].releasemem()
    def predict(self,Data):
        #_tmark=0.0
        _tmark=10000000.0
        for i in xrange(self.nTree):
            Data1=[]
            try:
                for j in xrange(self.SampleFeature):
                    Data1.append(Data[self.chFeature[i][j]])
                print "pass",i
                #_tmark+=self.RTree[i].predict(Data1)
                _tmark=min(_tmark,self.RTree[i].predict(Data1))
                #_tmark+=math.pow(self.RTree[i].predict(Data1),1.0/self.nTree)
            except Exception,e:
                print i,e
        #_tmark=_tmark/self.nTree
        return _tmark
    def loadfromfile(self,filename):
        fi=open(filename,"rb")
        dic=json.loads(fi.read())
        fi.close()
        self.nTree=dic["nTree"]
        self.Samplerate=dic["Samplerate"]
        self.SampleFeature=dic["SampleFeature"]
        self.chFeature=dic["chFeature"]
        for i in xrange(self.nTree):
            self.RTree[i].loadfromfile(filename+"-"+str(i))
            print i,"load"
    def savetofile(self,filename):
        fo=open(filename,"wb")
        fo.write(json.dumps({"nTree":self.nTree,"Samplerate":self.Samplerate,"SampleFeature":self.SampleFeature,"chFeature":self.chFeature}))
        fo.close()
        print "nsave"
        for i in xrange(self.nTree):
            if i<=self.progress:
                self.RTree[i].savetofile(filename+"-"+str(i))
if __name__=="__main__":
    nt=3
    """tr=GBDT(nt,100,5000,0.2)"""
    tr=randomforest(Tree=3)
    data=[]
    mark=[]
    name="test"
    for i in xrange(10):
        for k in xrange(80):
            td=[]
            for j in xrange(5):
                td.append(i+random())
            mark.append(i)
            data.append(td)
    tr.LoadData(data,mark)
    for i in xrange(nt):
        tr.TreeBuilder(i)
    tr.savetofile("%s.m"%(name))
    tr.loadfromfile("%s.m"%(name))
    for i in xrange(10):
        td=[]
        for j in xrange(5):
            td.append(i)
        print "predict ",i,tr.predict(td)
