import string
import os
import math
path2=r"E:\ditechcomp\training_data\RegTree-10-N03.csv"#"E:\ditechcomp\training_data\Record\GBDC20160531\DC10.m.csv"#"
path1="E:\\ditechcomp\\version4\\resultDCV2-D10-trasversed.csv"#".\\Record\\DC20160531\\DC-Rvs-D10-N20.m.csv"#
X1=[]
X2=[]
for i in open(path1,"rb"):
    i=i.split(",")
    i=string.atof(i[2])
    X1.append(i)
for i in open(path2,"rb"):
    i=i.split(",")
    i=string.atof(i[2])
    X2.append(i)
ct=0
er=0.0
for i in xrange(len(X1)):
    ct+=1
    if X1[i]>0:
        er+=abs(X1[i]-X2[i])/X1[i]
print er/ct
