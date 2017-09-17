import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

pca_2 = PCA(2)
cdj = pd.read_csv("data.csv")
cols = cdj.columns.tolist()
cols.insert(0, cols.pop(cols.index('titleOfBook')))
cdj = cdj[cols]

kmeans_model = KMeans(n_clusters=10, random_state=1).fit(cdj.iloc[:, 1:])
labels = kmeans_model.labels_
centroids = kmeans_model.cluster_centers_
plot_columns = pca_2.fit_transform(cdj.iloc[:,1:642]) 
plt.figure()

plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1],c=labels)
#plt.scatter(x=plot_columns[-1:,0],y = plot_columns[-1:,1],color="red",marker="v",s=100)
plt.show()
