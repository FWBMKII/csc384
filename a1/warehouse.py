#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
warehouse STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint

##################################################
# The search space class 'warehouse'             #
# This class is a sub-class of 'StateSpace'      #
##################################################

class warehouse(StateSpace):
    def __init__(self, action, gval, time, order_list, robot_list, prod_list, pack_list, parent = None):
#IMPLEMENT
        """Initialize a warehouse search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.time = time
        self.prod_list = prod_list
        self.pack_list = pack_list
        self.order_list = order_list
        self.robot_list = robot_list

    def successors(self): 
#IMPLEMENT
        '''Return list of warehouse objects that are the successors of the current object'''
        States = list()
        delivery_exist = False
        
        #for any idle robot, it can goes to deliver any unfulfilled orders
        robot_index = 0
        for r in self.robot_list:
            if r[1] == "idle":
                #exist idle robot -> does not allow skip action
                for o in self.order_list:
                    
                    #delete order in next state when a robot is going to take it
                    new_order_list = self.order_list.copy()
                    new_order_list.remove(o)
                    
                    #culculate required time
                    r_position = r[2]
                    prod_position = self.get_prod_position(o[0])
                    pack_position = self.get_pack_position(o[1])
                    time = (abs(r_position[0] - prod_position[0]) + abs(r_position[1] - prod_position[1])) + (abs(pack_position[0] - prod_position[0]) + abs(pack_position[1] - prod_position[1]))
                    
                    #update the robot's status
                    new_robot_list = self.robot_list.copy()

                    new_robot_list[robot_index] = [r[0], "on_delivery", pack_position, self.time + time]
                    
                    #append states list
                    States.append(warehouse("deliver(" + str(r[0]) + ", " + str(o[0]) + ", " + str(o[1]) + ")",
                                            self.gval,
                                            self.time,
                                            new_order_list,
                                            new_robot_list,
                                            self.prod_list,
                                            self.pack_list,
                                            self))
            else:
                delivery_exist = True
            robot_index += 1

        #wait is allow only when not all robots are idle
        if (delivery_exist):
            #find the minimum time need to wait till some robot finish its action
            new_time = -1
            for r in self.robot_list:
                if (len(r) == 4):
                    if new_time == -1:
                        new_time = r[3]
                    elif (r[3] < new_time):
                        new_time = r[3]
                                

            #update robot list after waiting
            new_robot_list = self.robot_list.copy()
            robot_index = 0
            for r in self.robot_list:
                if len(r) == 4:
                    if r[3] == new_time:
                        new_robot_list[robot_index] = r[:3]
                        new_robot_list[robot_index][1] = "idle"
                robot_index += 1
                    
            #append states list
            States.append(warehouse("move_forward(" + str(new_time) + ")" ,
                                    self.gval + new_time - self.time,
                                    new_time, 
                                    self.order_list, 
                                    new_robot_list, 
                                    self.prod_list, 
                                    self.pack_list,
                                    self))
                
       
        
        return States

    '''
    Helper functions to get product and pack station's position by given name
    '''
    def get_prod_position(self, prod):
        for p in self.prod_list:
            if (p[0] == prod):
                return p[1]
        return 0

    def get_pack_position(self, pack):
        for p in self.pack_list:
            if (p[0] == pack):
                return p[1]
        return 0


    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        return (self.time, str(self.robot_list), str(self.order_list), str(self.prod_list), str(self.pack_list))
        
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("Time = {}".format(self.get_time()))
        print("Unfulfilled Orders")
        for o in self.get_orders():
            print("    {} ==> {}".format(o[0], o[1]))
        print("Robot Status")
        for rs in self.get_robot_status():
            print("    {} is {}".format(rs[0], rs[1]), end="")
            if rs[1] == 'idle':
                print(" at location {}".format(rs[2]))
            elif rs[1] == 'on_delivery':
                print(" will be at location {} at time {}".format(rs[2], rs[3]))

#Data accessor routines.

    def get_robot_status(self):
#IMPLEMENT
        '''Return list containing status of each robot
           This list has to be in the format: [rs_1, rs_2, ..., rs_k]
           with one status list for each robot in the state. 
           Each robot status item rs_i is itself a list in the format [<name>, <status>, <loc>, <ftime>]
           Where <name> is the name of the robot (a string)
                 <status> is either the string "idle" or the string "on_delivery"
                 <loc> is a location (a pair (x,y)) 
                       if <status> == "idle" then loc is the robot's current location
                       if <status> == "on_delivery" then loc is the robot's future location
                <ftime> 
                       if <status> == "idle" this item is missing (i.e., the list is of 
                                      length 3)
                       if <status> == "on_delivery" then this is a number that is the 
                                      time that the robot will complete its current delivery
        '''
        return self.robot_list

    def get_time(self):
#IMPLEMENT
        '''Return the current time of this state (a number)'''
        return self.time

    def get_orders(self):
#IMPLEMENT
        '''Return list of unfulfilled orders of this state
           This list is in the format [o1, o2, ..., om]
           one item for each unfulfilled order. 
           Each oi is itself a list [<product_name>, <packing_station_name>]
           where <product_name> is the name of the product to be delivered
           and  <packing_station_name> is the name of the packing station it is to be delivered to'''
        return self.order_list


#############################################
# heuristics                                #
#############################################
    
def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_min_completion_time(state):
#IMPLEMENT
    '''warehouse heuristic'''
    #We want an admissible heuristic. Since the aim is to delivery all
    #of the products to their packing station in as short as a time as
    #possible. 
    #NOTE that we want an estimate of the ADDED time beyond the current
    #     state time.
    #Consider all of the possible delays in moving from this state to
    #a final delivery of all orders.
    # 1. All robots have to finish any current delivery they are on.
    #    So the earliest we could finish is the 
    #    maximum over all robots on delivery of 
    #       (robot's finish time - the current state time)
    #    we subtract the current state time because we want time
    #    beyond the current time required to complete the delivery
    #    Let this maximum be TIME1.
    #    Clearly we cannot finish before TIME1
    #
    # 2. For all unfulfilled orders we need to pick up the product of
    #    that order with some robot, and then move it to the right
    #    packing station. However, we could do many of these
    #    deliveries in parallel. So to get an *admissible* heuristic
    #    we take the MAXIMUM of a MINUMUM time any unfulfilled order
    #    can be completed. There are many different minimum times that
    #    could be computed...of varying complexity. For simplicity we
    #    ignore the time required to get a robot to package, and
    #    instead take the time to move the package from its location
    #    to the packing station location as being a suitable minimum.
    #    So we compute these minimums, then take the maximum of these
    #    minimums Call this max of mins TIME2
    #    Clearly we cannot finish before TIME@
    #
    # Finally we return as a the heuristic value the MAXIMUM of ITEM1 and ITEM2
    TIME1 = 0
    for r in state.robot_list:
        if r[1] == "on_delivery":
            if r[3] > TIME1:
                TIME1 = r[3]
    TIME1 = TIME1 - state.time

    TIME2 = 0
    for o in state.order_list:
        order_time = get_order_distance(state, o)
        if (order_time > TIME2):
            TIME2 = order_time

    return max(TIME1, TIME2)


def get_order_distance(state, order):
    '''
    based on the packet station list and product list of given state
    return the distance between product and packet station in a order
    '''
    prod = state.get_prod_position(order[0])
    pack = state.get_pack_position(order[1])
    return (abs(prod[0] - pack[0]) + abs(prod[1] - pack[1]))

def warehouse_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal when all orders have been delivered'''
    for r in state.robot_list:
        if (len(r) == 4):
            return False
    return (state.order_list == [])

def make_init_state(product_list, packing_station_list, current_time, open_orders, robot_status):
#IMPLEMENT
    '''Input the following items which specify a state and return a warehouse object 
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       product_list = [p1, p2, ..., pk]
          a list of products. Each product pi is itself a list
          pi = [product_name, (x,y)] where 
              product_name is the name of the product (a string) and (x,y) is the
              location of that product.
       packing_station = [ps1, ps2, ..., psn]
          a list of packing stations. Each packing station ps is itself a list
          pi = [packing_station_name, (x,y)] where 
              packing_station_name is the name of the packing station (a string) and (x,y) is the
              location of that station.
       current_time = an integer >= 0
          The state's current time.
       open_orders = [o1, o2, ..., om] 
          a list of unfulfilled (open) orders. Each order is itself a list
          oi = [product_name, packing_station_name] where
               product_name is the name of the product (a string) and
               packing_station_name is the name of the packing station (a string)
               The order is to move the product to the packing station
        robot_status = [rs1, rs2, ..., rsk]
          a list of robot and their status. Each item is itself a list  
          rsi = ['name', 'idle'|'on_delivery', (x, y), <finish_time>]   
            rsi[0] robot name---a string 
            rsi[1] robot status, either the string "idle" or the string
                  "on_delivery"
            rsi[2] robot's location--if "idle" this is the current robot's
                   location, if "on_delivery" this is the robots final future location
                   after it has completed the delivery
            rsi[3] the finish time of the delivery if the "on_delivery" 
                   this element of the list is absent if robot is "idle" 

   NOTE: for simplicity you may assume that 
         (a) no name (robot, product, or packing station is repeated)
         (b) all orders contain known products and packing stations
         (c) all locations are integers (x,y) where both x and y are >= 0
         (d) the robot status items are correctly formatted
         (e) the future time for any robot on_delivery is >= to the current time
         (f) the current time is >= 0
    '''
    return warehouse("START()", 0, 0, open_orders, robot_status, product_list, packing_station_list, None)

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_init_state(nprods, npacks, norders, nrobots):
    '''Generate a random initial state containing 
       nprods = number of products
       npacks = number of packing stations
       norders = number of unfulfilled orders
       nrobots = number of robots in domain'''

    prods = []
    for i in range(nprods):
        ii = int(i)
        prods.append(["product{}".format(ii), (randint(0,50), randint(0,50))])
    packs = []
    for i in range(npacks):
        ii = int(i)
        packs.append(["packing{}".format(ii), (randint(0,50), randint(0,50))])
    orders = []
    for i in range(norders):
        orders.append([prods[randint(0,nprods-1)][0], packs[randint(0,npacks-1)][0]])
    robotStatus = []
    for i in range(nrobots):
        ii = int(i)
        robotStatus.append(["robot{}".format(ii), "idle", (randint(0,50), randint(0,50))])
    return make_init_state(prods, packs, 0, orders, robotStatus)


def test(nprods, npacks, norders, nrobots):
    s0 = make_rand_init_state(nprods, npacks, norders, nrobots)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, warehouse_goal_fn, heur_min_completion_time)
