'''
Not started functions:
f1
f2
f3
f4

In progress:
Data Processing (line 110)
ToU
get_best_capacity

Completed functions:
Clustering      (line 130)
Plotting        (line 150)
Battery Class   (line 215) - maybe need get_initial_charge
f2
f3
f4
'''

'''
-------------------------------------------------
The plan in words (Ctrl+C , Ctrl+V from project proposal)
-------------------------------------------------

Parse and clean the data in such a way that we create a new external excel sheet / dataframe that consists of 24 features corresponding 
to the usage over the  24 hours of a day in local time averaged over the year (i.e. midnight to 1am, 1am to 2 am, …). 
With each row corresponding to an individual household. 

In a very similar manner, per household, we will average the PV production data into hourly intervals over a 24 hr day in local time. 
Once the usage data is cleaned and averaged into hour long intervals, it will be introduced to a k-means clustering method to 
characterise the individual households into group profiles. For a given household, the usage data is approximated as the cluster 
centre for its profile.

Based on this approximation a comparison between the 'typical' usage for the profile and the households actual PV generation will be made. 
This comparison in combination with consideration of Feed in Tariffs and Time of Use rate will be used to create a weighted
usage/cost profile over the day.
 
A simulation will be run/ a model will be created that compares the baseline cost of the household with no battery and then run with
a simplified battery of differing capacities and calculate a 'saving' on the baseline (with extra consideration of the 
capacity-dependent cost and lifetime of the battery). The best battery will be taken as the one that saves the most money per day. 
This simulation will be run for all households of the same cluster/category and used to generate the ideal battery size for the whole 
demand profile, repeated for all demand profiles.

For testing, we want to calculate how well our simpler 'clustered recommendation' works for a given household as compared to a
more complicated method of running the full simulation using the households usage and generation data by comparing the potential 
daily savings of the two models. We will generate a percentage difference between the simpler and 'truer' model as an indicator 
of the accuracy of the simplified model.


-------------------------------------------------
Protocols for Database Structure / Instructions
-------------------------------------------------
When creating your function create a new file per function and copy-paste instructions
When completed upload to the shared github so everyone can download to their own device and run as needed

Assume input and output is numpy matrix unless otherwise specified if you wish to use pandas please convert 
np to pd at start then convert back from pd to np at the end

I assume we all know standard shortenings for modules and will use them consistently:
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sklearn as skl
etc

Try to update this document and the list of completed/incomplete functions as as much as possible.

Reach out for help if you need it

----------------------------------
Structure of the Data post-processing
-----------------------------------

Allocated to: Mark (good luck mate)
Note: Not sure if we discussed with you so ill leave it here: different houses have different timezones and some states observe daylight savings 

Note: It might be useful to write some of these to excel files and circulate these to group members to store locally on their computers
as these may be very time consuming computations and generally dont need ot be run each iteration anyway

To be clarified: Do we want to take about 10 houses as testing?

From the Data need to Extract the following:
    1. A (510,24) np matrix corresponding to the overall average consumption delimited by hour (in local time) per household
        To be used in clustering

    2. No longer useful

    3. A (3, 24, 510) np matrix with averages of usage delimited similar to as above however in this case we have 
    '3' averages corresponding to the average usage per Time of Use season
    and each 'page' corresponding to a household
        These 3 seasons will be 'winter', 'summer' and 'else' as described by ausgrids savings
        Will be used with PV generation (4) and Time of use tariffs to determine cost / savings

    4. Ditto for PV generation
        Split into an average for each hour of a typical day of a given season, per household

    5. Values corresponding to the length of the Time of use 'seasons' from (3) and (4) in days.

    ... I probably missed some and will update

'''


#
#
#Functions
#
#



def function_format():
    '''
    Allocated to/Completed By:
    
    Inputs:

    Outputs:


    Notes
    '''
    return None



def clustering(usage_data,n):
    '''

    Allocated to / Completed by: 

    Inputs:
    usage_data   - A (510,24) np array containing average usages
    n            - The number of clusters to be made

    Outputs:
    classes     - An (510,) numpy vector containing the households corresponding class 
                e.g. [0,0,1,(n-1),4,3,(n-1),...,1]
    centroids   - An (n,24) np matrix containing the cluster centres from the algorithm
                    -> For plotting and approximation

    Uses k-means unsupervised clustering, please leave 'n' general so that plotting can be repeated quickly
    and we can choose the best n (this will probably end up being 5 as in the presentation anyway). The classes and centroids will

    '''

    return classes , centroids


def plotting(centres):
    '''
    Allocated to/Completed By: 
    
    Inputs: 
    Centroids          - this is (n,24) np array for some integer n that cannot be specified further
    Outputs:
    None

    Used to generate and display (and eventually save) a plot of overlapping profiles to determine if they are meaningful/useful
    '''
    return None




def get_cost(usage, time, season):
    '''
    Inputs: 
    Local time - number (0-23) corresponding to the start of the hour
    net_usage - number (+ve or negative) 
    ToU season - 's','w','o' - (summer,winter, other)

    Outputs:
    cost      -  A single value (rounded to the nearest cent) corresponding to the cost/sale of energu for that period

    Notes:
    Please have as a class method i.e. in Cezars simulation will be called as simply:
    cost = get_cost(u,t,s)
    '''


class battery:
    # simple  'fill whenever possible, empty whenever needed'
    # Model as described in presentation 


    def __init__(self,capacity,foo,bar):
        self.capacity = capacity
        self.charge = foo
        self.bar = bar

    # + Some method that can be called to determine the sign difference and hence
    # charge or discharge the battery. Or split into 3 methods
    ...

def get_best_capacity():
    '''
    Our 'Simulation'
    To be clarified ***Very hard***

    Allocated to/Completed By: Cezar
    
    Inputs:
    u_data    -  a (3,24) np array that has average uses for each season, order (summer, winter, other)
    pv_data   - a (3,24) np array that has average hourly pv gen for each season, order (summer, winter, other)
    length of summer, length of winter, length of other - days  (to be clarified)
    
    Calls to:
    ToU/ToU.get_cost




    Outputs:
    best capacity for a household


    Use the battery object, will iterate over a range of capacities and choose the best one for a house

    '''
    return None
    








