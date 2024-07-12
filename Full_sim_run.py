import numpy as np
from plotting import get_cost, plotting
from get_best_capacity import get_best_capacity
from battery import battery
from Clustering import clustering
from get_cluster_recommendation import get_cluster_recommendation


'''
Further Data cleaning:
'Load_annual_avg.npy', 
Has nan entries for row 86 and 123
There is an outlier house at row 70 which slightly breaks the k-means algorithm and this will be removed 
i.e. it gets its own cluster and peak usage about 5x that of any other property in the data

'new_load_seasonal_avg.npy' and 'new_gen_seasonal_avg.npy'
Has nan entries for pages 86 and 123
Has the outlier house at page 70

The 86 and 123 houses correspond to given site ID's in the dictionary that had no corresponding data
Some of the rationale for the discovery and removal of these can be found in 'test3.py'

The data will be further split to take 10 houses for testing and the remaining to generate the model
'''

#Full year average data
year_u_data = np.load('load_annual_avg.npy')
#Seasonal usage data
s_u_data = np.load('new_load_seasonal_avg.npy')
#Season gen data
s_pv_data = np.load('new_gen_seasonal_avg.npy')




#Remove the desired rows
year_u_data = np.delete(year_u_data,[70,86,123], axis = 0)
#Remove the desired pages
s_u_data = np.delete(s_u_data,[70,86,123], axis = 0)
s_pv_data = np.delete(s_pv_data,[70,86,123], axis = 0)

# Split into test and model datasets
year_u_data_t = year_u_data[:40,:]
year_u_data_m = year_u_data[40:,:]

s_u_data_t = s_u_data[:40,:,:]
s_u_data_m = s_u_data[40:,:,:]

s_pv_data_t = s_pv_data[:40,:,:]
s_pv_data_m = s_pv_data[40:,:,:]


#Cluster the houses by annual average usage and pull out a list with their corresponding cluster index [0,1,2,3,4,5]
kmeans, classes, centroids = clustering(year_u_data_m,5)

plotting(centroids)

'''
used for debugging
for i in range(len(s_u_data_m)):
    #print(s_u_data_m[i,:,:])
    #print(s_pv_data_m[i,:,:])
    #print(year_u_data_m[i,:])
    print(get_best_capacity(s_u_data_m[i,:,:],s_pv_data_m[i,:,:]))
'''

#This will iterate for every cluster index and makes

# Will return cluster recommendations with the output (cluster_number, no. of houses in the cluster, cluster_rec)
cluster_recs = []
cluster_savings = []
for i in range(len(centroids)):
    n, cluster_size, cluster_rec, cluster_saving = get_cluster_recommendation(i, s_u_data_m, s_pv_data_m, classes)
    cluster_recs.append(cluster_rec)
    cluster_savings.append(cluster_saving)
    print(n, cluster_size, cluster_rec, cluster_saving)


# return the average for every house together
n_houses = len(s_u_data_m)
cap_cum_sum = 0
save_cum_sum = 0
for i in range(n_houses):
    best_cap,best_cost,best_saving = get_best_capacity(s_u_data_m[i,:,:], s_pv_data_m[i,:,:])
    cap_cum_sum += best_cap
    save_cum_sum += best_saving

print('Averages')
Average_rec = cap_cum_sum/n_houses
Average_save = save_cum_sum/n_houses
print('Average Capacity: ', Average_rec)
print('Average Saving: ', Average_save)


'''
TESTING
TESTING
TESTING
Use the test sets 'foo_t' to compare how well they would perform if they were recommended a battery solely on what cluster they fell into
based on usage 'shape' from the clustering algorithm vs actually performing the more complex sim using a few seasonal days


'''


classes_t = kmeans.predict(year_u_data_t)
print('house no. , cluster, cluster cap rec,  saving if we had cluster rec battery, sim cap rec, sim saving')

p_error_cum_sum = 0

n_houses_t = len(year_u_data_t)

holder = n_houses_t
for i in range(n_houses_t):
    cluster_index = classes_t[i]
    model_rec = cluster_recs[cluster_index]
    model__ind_save = cluster_savings[cluster_index]

    # This calls get_best_capacity where we consider the case where the house had the capacity as recommended by the cluster
    #and store the saving for this case
    blah, bleh, model_rec_save = get_best_capacity(s_u_data_t[i,:,:], s_pv_data_t[i,:,:], [0, model_rec])

    sim_rec,best_cost, sim_save = get_best_capacity(s_u_data_t[i,:,:], s_pv_data_t[i,:,:])
    
    if sim_save == 0:
        p_error = 0
        holder -= 1
    else:
        p_error = (sim_save - model_rec_save)/abs(sim_save) * 100

    #For debugging
    
    print(i, cluster_index, model_rec, model_rec_save,  sim_rec, sim_save, p_error)
    
    p_error_cum_sum += p_error

n_p_errors = holder

avg_p_error = round(p_error_cum_sum/n_p_errors,2)
print(avg_p_error)