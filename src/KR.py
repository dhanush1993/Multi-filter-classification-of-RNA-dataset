import pandas as pd
import pdb
from sklearn.cluster import KMeans
import numpy as np
def kmeans_reduce(X):
	kmeans = KMeans(n_clusters=28)
	kmeans.fit(X)
	p=kmeans.predict(X)
	indexes = {}
	centroids = kmeans.cluster_centers_
	msse = np.zeros(X.shape)
	drop = np.zeros(X.shape)
	orgSize = X.shape[1]
	print("Kmeans Done")
	for i,val in enumerate(X.values):
		for j,val_ in enumerate(val):
			msse[i][j] = (np.abs((val_-centroids[p[i]][j])))
		mean_row = np.mean(msse[i])
		for k,m in enumerate(msse[i]):
			if(m > mean_row):
				drop[i][k] = 1;
	z = np.sum(drop,axis=0)	
	columns = np.array(X.columns.values)
	drop_cols = []
	limit = (X.shape[0]/2)
	for i,m in enumerate(z):
		if(m >= limit):
			drop_cols.append(columns[i])
	print("Dropping Features")
	X.drop(drop_cols, axis=1, inplace=True)
	print("Features reduced from "+str(orgSize)+" to "+str(X.shape[1]))
	return X