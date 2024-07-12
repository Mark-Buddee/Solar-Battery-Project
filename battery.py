

class battery:
    # simple  'fill whenever possible, empty whenever needed'
    # Model as described in presentation 


    def __init__(self,capacity):
        #When initiating a battery object in the sim pass in the capacity that is being iterated over
        self.capacity = capacity
        self.charge = 0


    
    def check_net_usage(self,net_u):
        #The main method that will be called every 'hour' of simulation
        #usage: net_u = battery.check_net_usage(net_u)
        if net_u > 0:
            return self.discharging(net_u)
        elif net_u < 0:
            return self.charging(net_u)
        else:
            return 0

    def discharging(self,net_u):
        # net_u > 0
        if self.charge >= net_u:
            #excess demand can be completely filled by battery charge
            x = net_u
            ret = net_u - x
            self.charge -= x
            
        else:
            #self.charge < net_u 
            #excess demand exceeds what can be filled by the battery
            x = self.charge
            ret = net_u - x
            self.charge = 0
        return ret
        
    def charging(self, net_u):
        # net_u < 0
        if (self.capacity - self.charge) >= abs(net_u):
            #excess production can be fully absorbed by battery
            x = abs(net_u)
            self.charge += x
            ret = 0
            
        else:
            #(self.capacity - self.charge) < abs(net_u) 
            #excess production cannot be fully absorbed into battery
            x = (self.capacity - self.charge)
            ret = net_u + x        
            self.charge = self.capacity

        return ret