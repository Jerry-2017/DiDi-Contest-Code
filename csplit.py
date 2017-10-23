from cffi import FFI
import random
class cpack:
    def __init__(self,Data,Mark):
        self.ffi=FFI()
        self.ffi.cdef("""
            typedef struct ret{
                int feature;
                double split;
                double lerr,rerr,toterr;
                int lnum,rnum;
            }rt;
            rt bsplit(int nsample,int nfeature,double **Data,double * Mark,int *partion,double error);
        """)
        assert(len(Data[0])<60)
        print "init"
        self.nFeature=len(Data[0])
        self.nSample=len(Data)
        self.Data=self.ffi.new("double*[]",self.nSample)
        self.ds=[None]*len(Data)
        for i in xrange(len(Data)):
            self.ds[i]=self.ffi.new("double[]",len(Data[0]))
            self.Data[i]=self.ds[i]
        self.Mark=self.ffi.new("double[]",len(Mark))
        self.call=self.ffi.verify("""
            typedef struct ret{
                int feature;
                double split;
                double lerr,rerr,toterr;
                int lnum,rnum;
            }rt;
            double dabs(double a)
            {
                if (a>0) return a;
                else return -a;
            }
            rt bsplit(int nsample,int nfeature,double **Data,double* Mark,int *partion,double error)
            {
                int i,j;
                struct ret a;
                int cfeature=-1;
                double thresh=-1;
                double opt=error,_lerr,_rerr;
                int _lnum,_rnum;
                if (opt!=0)
                    for (i=0;i<nfeature;i++)
                    {
                        double mv=1000000.0,mv1,lsum,rsum,lm,rm,lerr,rerr;
                        int lnum,rnum;
                        for (j=0;j<nsample;j++)
                            if (Data[partion[j]][i]<mv)
                                mv=Data[partion[j]][i];
                        do
                        {
                            mv1=10000000.0;
                            lsum=0;rsum=0;
                            lnum=0;rnum=0;
                            for (j=0;j<nsample;j++)
                                if (Data[partion[j]][i]<=mv)
                                {
                                    lsum+=Mark[partion[j]];
                                    lnum+=1;
                                }
                                else
                                {
                                    rsum+=Mark[partion[j]];
                                    rnum+=1;
                                }
                            if (lnum==0 || rnum==0)
                                break;
                            lm=lsum/lnum;
                            rm=rsum/rnum;
                            lerr=0;
                            rerr=0;
                            for (j=0;j<nsample;j++)
                            {
                                if (Data[partion[j]][i]>mv && Data[partion[j]][i]<mv1)
                                    mv1=Data[partion[j]][i];
                                if (Mark[partion[j]]!=0)
                                {
                                    if (Data[partion[j]][i]<=mv )
                                        lerr+=dabs(Mark[partion[j]]-lm)/Mark[partion[j]];
                                    else 
                                       rerr+=dabs(Mark[partion[j]]-rm)/Mark[partion[j]];
                                }
                            }
                            if (lerr+rerr<opt)
                            {
                                opt=lerr+rerr;
                                cfeature=i;
                                thresh=mv;
                                _lerr=lerr;
                                _rerr=rerr;
                                _lnum=lnum;
                                _rnum=rnum;
                            }
                            mv=mv1;
                        }while (mv!=10000000.0);
                }
                a.feature=cfeature;
                a.split=thresh;
                a.lerr=_lerr;
                a.rerr=_rerr;
                a.lnum=_lnum;
                a.rnum=_rnum;
                a.toterr=opt;
                return a;
            }
        """)
        for i in xrange(len(Data)):
            for j in xrange(len(Data[0])):
                self.Data[i][j]=Data[i][j]
            self.Mark[i]=Mark[i]
    def best(self,partion):
        partion1=self.ffi.new("int[]",len(partion))
        for i in xrange(len(partion)):
            partion1[i]=partion[i]
        m=self.call.bsplit(len(partion),self.nFeature,self.Data,self.Mark,partion1,100000000.0)
        #print m.toterr,m.lnum,m.rnum
        return m.feature,m.split,m.lerr,m.rerr,m.toterr,m.lnum,m.rnum
if __name__=="__main__":
    data=[]
    mark=[]
    name="test"
    for i in xrange(10):
        for k in xrange(80):
            td=[]
            for j in xrange(5):
                if j==2:
                    td.append(i+random.random())
                else:
                    td.append(2+random.random())
            mark.append(i)
            data.append(td)
    tt=cpack(data,mark)
    k=range(800)
    a1,a2=tt.best(k)
    print a1,a2