import pandas as pd
import matplotlib.pyplot as plt
import shelve
import xml.etree.ElementTree as ET
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def remove_non_ascii(text):
   return ''.join([i if ord(i) < 128 else ' ' for i in text])
tree = ET.parse('treegen.xml')
root = tree.getroot()
listOfIndices = [0,2,3,6,9,20,23]
pca_2 = PCA(2)
user_avg = shelve.open("user_avg")
cdj = pd.read_csv("data.csv")
clusters = shelve.open("clusters")
cols = cdj.columns.tolist()
cols.insert(0, cols.pop(cols.index('titleOfBook')))
cdj = cdj[cols]
kmeans_model1 = KMeans(n_clusters=6, random_state=1).fit(cdj.iloc[:, 1:])
labels1 = kmeans_model1.labels_
centroids1 = kmeans_model1.cluster_centers_
plot_columns1 = pca_2.fit_transform(cdj.iloc[:,1:642])


#TO BE SEEN
cdj = cdj.drop('titleOfBook', 1)
counter=-1
counter1 = 1
for key,value in user_avg.iteritems() :
	counter =counter + 1
	if counter in listOfIndices :
		counter1 = counter1 +1
		m = open("results/finalResultDemo"+str(counter1)+".txt", "w+")
		to_merge = []
		to_merge.append(cdj)
		to_merge.append(value)
		nw = pd.concat(to_merge)
		plot_columns = pca_2.fit_transform(nw.iloc[:,:]) 
		kmeans_model = KMeans(n_clusters=6, random_state=1).fit(nw.iloc[:,:])
		labels = kmeans_model.labels_
		plt.figure()
		#print plot_columns
		labelx = kmeans_model1.predict(value)
		for k in clusters[str(labelx[0])] : 
			m.write(k)
			m.write("\n")
		m.write("\n \n \n \n The facebook profile data \n \n \n \n")
		for target in root.findall(".//user[@id='"+key+"']"):
			for child in target :
				m.write(remove_non_ascii(child.tag))
				m.write("      " +remove_non_ascii(child.text))
				m.write("\n")
		m.write("\n \n \n \n Recommended Books : \n \n")
		m.write(clusters[str(labelx[0])][0])
		m.write("\n")
		m.write(clusters[str(labelx[0])][2])
		m.write("\n")
		m.write(clusters[str(labelx[0])][5])
		m.write("\n")
		m.close()
		plt.scatter(x=plot_columns1[:,0], y=plot_columns1[:,1],c=labels1)
		plt.scatter(x=plot_columns[-1:,0], y=plot_columns[-1:,1],color='red',marker='v',s=100)
		plt.show()
		
		raw_input("success")
