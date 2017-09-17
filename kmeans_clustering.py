import pandas as pd
import shelve
from sklearn.cluster import KMeans


cdj = pd.read_csv("data.csv")
cols = cdj.columns.tolist()
cols.insert(0, cols.pop(cols.index('titleOfBook')))
cdj = cdj[cols]
clusters = shelve.open("clusters")
kmeans_model = KMeans(n_clusters=6, random_state=1).fit(cdj.iloc[:, 1:])
# kmeans_model.labels_ is the list
f1=open('./sixCresults', 'w+')
lab = 0
for lab in range(0,6)  :

	thisCluster =[]
	for index , row in cdj.iterrows() :

		if kmeans_model.labels_[index] == lab :
			thisCluster.append(row['titleOfBook'])
	clusters[str(lab)] = thisCluster
	del thisCluster[:]
print clusters