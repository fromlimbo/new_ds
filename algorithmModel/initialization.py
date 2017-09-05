# coding:utf-8
""""
This file is called by the generic procedure to initialize a new generation.
"""
import copy
from Bases import *
from packaging import *


def initialization(ppl_size, data, misc, flag_crossover=False, print_switch=0, old_routes=None):
    """
    This function generates the initial generation based on raw data.

    :param ppl_size: poplulation size
    :param data: a variable of Data class containing order dictionary and shipment dictionary.
    :param misc: the variable passed by GAVRP.py to set parameters
    :param flag_crossover: a flag to indicate whether this initialization is for crossover
    :param print_switch: if print_switch=1, some variables will be printed
    :param old_routes: 
    :return: a generation of ppl_size
    """

    population = []
    count = 0

    def random_packaging():
        shipment_list = copy.copy(data.ship_dict.values())
        trailer_list = data.trailer_dict.values()

        np.random.shuffle(shipment_list)
        np.random.shuffle(trailer_list)

        if misc.cost_weight[0] > 0.4 or misc.cost_weight[1] > 0.4 or misc.cost_weight[2] > 0.4:
            trailer_list.sort(key=operator.attrgetter('capacity_for_xl_car'), reverse=True)
            trailer_list.sort(key=operator.attrgetter('capacity_for_l_car'), reverse=True)
            trailer_list.sort(key=operator.attrgetter('capacity_all'), reverse=False)
        if misc.cost_weight[2] > 0.4:
            shipment_list.sort(key=operator.attrgetter('car_type'), reverse=True)
        if misc.cost_weight[3] > 0.4:
            shipment_list.sort(key=operator.attrgetter('start_loc'), reverse=False)
            shipment_list.sort(key=operator.attrgetter('dealer_code'), reverse=False)
        if misc.cost_weight[1] > 0.4:
            shipment_list.sort(key=operator.attrgetter('OTD'), reverse=False)
        route_list = [Route(i, misc) for i in trailer_list]#所有大板车及其装载情况类Route的变量组成的列表

        all_mighty_route = AllMightyRoute()#The super trailer which can take any shipment which is not taken by normal trailers
        route_list.append(all_mighty_route)
        full_pre = 0 #the total number of full trailers in the previous iteration
        full_route = 1# the total number of full trailers in this iteration
        while full_route != full_pre:# iteration stops when the number of full trailers cannot be bigger
            full_pre = full_route
            while shipment_list:#把所有运单都装走
                ship = shipment_list.pop()
                for route in route_list:
                    if route.add_ship(ship):# Added this ship into this route successfully
                        break
            for route in route_list:
                if route.id == 'AllMightyRoute' or len(route.ships) < sum(route.slot_cap):#If the trailer in this route is not full
                    shipment_list += list(route.ships.values())# all the shipments in this trailer are put back into shipment_list
                    route.ships = {}#this trailer is set empty
                    route.rearrange_ships()#route.slot, route._ship_loc,route.ships are reset
            full_route = sum(len(i.ships) == sum(i.slot_cap) for i in route_list if i.id != 'AllMightyRoute')# The total number of full trailers

        for i in shipment_list:
            all_mighty_route.add_ship(i)#To add shipments in shipment_list to the super trailer, all_mighty

        individual = {i.id: i for i in route_list}

        return individual

    while count < ppl_size:
        ind = random_packaging()#产生一个随机装载方案

        population.append(ind)
        count += 1
        if print_switch > 1:
            print 'Individual: %4d    GoneTrailer: %4d    GoneShips: %4d    RemainShips: %4d' % \
                  (count,
                   sum(len(i.ships) == sum(i.slot_cap) for i in ind.values() if i.id != 'AllMightyRoute'),
                   sum(len(i.ships) for i in ind.values() if i.id != 'AllMightyRoute'),
                   len(ind['AllMightyRoute'].ships)
                   )

    return population