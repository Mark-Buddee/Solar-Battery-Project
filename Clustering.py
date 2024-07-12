from sklearn.cluster import KMeans
import numpy as np

def clustering(usage_data,n):
    '''

    Allocated to / Completed by: 

    Inputs:
    usage_data   - A (510,24) np array containing average usages
    n            - The number of clusters to be made

    Outputs:
    classes     - An (510,) numpy vector containing the households corresponding class 
    centroids   - An (n,24) np matrix containing the cluster centres from the algorithm
                    -> For plotting and approximation

    Uses k-means unsupervised clustering, please leave 'n' general so that plotting can be repeated quickly
    and we can choose the best n (this will probably end up being 5 as in the presentation anyway). The classes and centroids will

    '''
    # random_state = x for reproducability
    kmeans = KMeans(n_clusters=n, random_state=3)
    kmeans.fit(usage_data)
    
    classes = np.array(kmeans.labels_)
    centroids = np.array(kmeans.cluster_centers_)

    return kmeans, classes, centroids




'''
X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

classes, centroids = clustering(X, 2)

print(classes)
print(np.shape(classes))
print(centroids)
print(np.shape(centroids))
'''
