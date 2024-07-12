from battery import *
from plotting import get_cost
#season_lens['s']


def get_best_capacity(u_data, pv_data, capacities = range(0, 10100, 100)):
    '''
    Per House
    Our 'Simulation'

    Allocated to/Completed By: Cezar
    
    Inputs:
    u_data    -  a (3,24) np array that has average uses for each season, order (summer, winter, others)
    pv_data   - a (3,24) np array that has average hourly pv gen for each season, order (summer, winter, other)
    length of summer, length of winter, length of other - days  (to be clarified)
    
    Calls to:
    ToU/ToU.get_cost()
    

    Outputs:
    best capacity for a household

    Use the battery object, will iterate over a range of capacities and choose the best one for a house

    '''
    
    net_usage = u_data - pv_data
    
    #Our processed data is implicitly structured in this way
    s_net = net_usage[0,:]
    w_net = net_usage[1,:]
    o_net = net_usage[2,:]

    #As determined by Ausgrids definition of pricing seasons
    season_lens = {'s' : 151, 'w' : 92, 'o' : 122}
    season_data = {'s' : s_net, 'w' : w_net , 'o' : o_net }

    seasons = ['s', 'w','o']
    
    best_cost = 100000000

    best_cap = 0

    for capacity in capacities:
        #print(capacity)
        
        
        #cost for the given capacity
        cap_cost = 0

        for season in seasons:
            #print(season)
            #initialise an instance of the battery object with the given capacity
            bat = battery(capacity)
            #pull the relevant seasons data from the dictionary
            seasonal_u = season_data[season]

            #run a few 'dummy days' to get a realistic starting charge of the battery at midnight for the given season
            for dummy_count in range(3):
                for hour in range(0,24):
                    hours_u = seasonal_u[hour]
                    
                    #Ask the battery to charge/discharge (cost/sale of excess not yet relevant)
                    if capacity != 0:
                        hours_u = bat.check_net_usage(hours_u)
                    
                    
                    #Used in debugging to check the leftover charge in the battery at midnight
                    '''
                    if hour == 23:
                        print(dummy_count+1)
                        print('battery charge')
                        print(bat.charge)
                    '''
                    


            #Battery charge persists within the battery object within the given season
            #Can now run a 'true' indicative day and use it to generate cost for the ToU season
            day_cost = 0
            

            for hour in range(0,24):
                hours_u = seasonal_u[hour]
                
                #Ask the battery to charge/discharge
                if capacity != 0:
                    hours_u = bat.check_net_usage(hours_u)
                #Apply the ToU model/class to get cost from usage, time and season
                #Converts the post battery load/gen to a cost/sale for the hour
                hour_cost = get_cost(hours_u, hour, season)
                
                #As this iterates we will get a full day of energy use costs and sales
                day_cost += hour_cost
                
                #used to check the leftoveer charge in the battery
                '''
                if hour == 23:

                    print(bat.charge)
                '''

            season_cost = day_cost * season_lens[season]
            cap_cost += season_cost


        # Account for the increasing cost of a battery with increasing capacity
        # Research suggests a fair model is as below: $1250 per kwh with a lifetime of 10 years 
        cap_cost +=  1250*(capacity/1000)/10
        if capacity == 0:
            no_bat_cost = cap_cost
        if cap_cost < best_cost:
            best_cap = capacity
            best_cost = cap_cost

    best_saving = no_bat_cost - best_cost
    return best_cap, best_cost, best_saving