import numpy as np
from sklearn.cluster import KMeans
from Clustering import clustering
from plotting import *

data = np.load('load_annual_avg.npy')
#REmoves all rows containing NAN's

data = data[~np.isnan(data).any(axis=1)]

'''
Comment/uncomment the following line to include/remove the outlier row'''
#data = np.delete(data,70, axis = 0)

classes , centroids = clustering(data,5)

print(classes)
print(centroids)

plotting(centroids)

#Check that the right row was removed
print(data[69:71])