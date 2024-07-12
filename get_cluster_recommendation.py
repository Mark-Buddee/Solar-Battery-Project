from get_best_capacity import get_best_capacity
import numpy as np

def get_cluster_recommendation(n, u_data, pv_data, classes):
    '''
    Inputs:
    n               -    The cluster index 
    u_data          -    The full (3,24,510) seasonal usage averages np array
    pv_data         -    The full (3,24,510) seasonal pv generation averages np array
    classes         -    see clustering function output

    Outputs:
    Cluster_rec     -   A single best capacity for the whole cluster
    '''

    n_houses, = np.shape(classes)
    battery_sizes = [] 
    savings = []
    cluster_size = 0
    for i in range(n_houses):   
        if classes[i] == n:
            cluster_size += 1
            house_u_data = u_data[i,:,:]
            house_pv_data = pv_data[i,:,:]
            
            best_cap, best_cost, best_saving = get_best_capacity(house_u_data, house_pv_data)
            '''
            Used for debugging
            if type(best_cap) != int:
                print('\n \n\ \n \n \n \n ')
                print(i)
            '''
            battery_sizes.append(best_cap)    
            savings.append(best_saving)  

    battery_sizes = np.array(battery_sizes)
    cluster_rec = np.mean(battery_sizes)

    savings = np.array(savings)
    cluster_saving = np.mean(savings)

    return n, cluster_size, cluster_rec, cluster_saving