from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
#metric= [[0 for col in range(67)] for row in range(67)]
fi=open("metric.txt","rb")
j1=None
for i in fi:
    j2=j1
    j1=i
fi.close()
j2=json.loads(j2)
j1=json.loads(j1)
metric= [[0 for col in range(66)] for row in range(66)]
for i in xrange(66):
    for j in xrange(66):
        n1=j2[i+1][j+1]
        n2=j1[i+1][j+1]
        if (i!=j):
            n1+=j2[j+1][i+1]
            n2+=j1[j+1][i+1]
        if n2!=0:
            metric[i][j]=n1/n2
        else:
            metric[i][j]=0
#metric=[[2,1],[1,2]]
mds = manifold.MDS(n_components=2, max_iter=10000, eps=1e-9,dissimilarity='precomputed')
pos = mds.fit(metric).embedding_
clf = PCA(n_components=2)
pos = clf.fit_transform(pos)
print pos
fo=open("position.txt","wb")
fig = plt.figure(1)
ax = plt.axes([0., 0., 1., 1.])
plt.scatter(pos[:, 0], pos[:, 1], s=66, c='g')
#
ar=[]
for i in xrange(66):
    ar.append([pos[i][0],pos[i][1]])
fo.write(json.dumps(ar))
plt.show()