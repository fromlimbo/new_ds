""""
This file generates a new generation through crossover and mutation.

Input: population size, parameter, initial data of orders and shipments, misc parameter

Output: the new generation
"""
import copy
from Bases import *
import initialization
import random


def co_pro(ppl, par, data, misc, print_switch, parallel=False):
    """
    This function generates a new generation through crossover based on the present generation

    :param ppl: The present population
    :param par: related parameters in crossover of two individuals 
    :param data: data of orders and shipments
    :param misc: the parameter set which is frequently used
    :param print_switch: a switch for print
    :param parallel: the flag to determine whether parallel computation is used
    :return: a new population through crossover
    """
    ppl_size = len(ppl)


    # To select individuals to generate the next generation using wheel disc
    privilege_ppl = [] #To record the selected individual to generate the next generation
    accumulated_cost = [] # To record accumulated cost till each individual
    accumulated_cost.append(0.0) # The first element is zero
    # To calculate accumulate_cost, which contains ppl_size+1 elements in the end
    for i in range(ppl_size):
        accumulated_cost.append(accumulated_cost[i]+ind_cost(ppl[i],misc))
    # Normolize each element in the list to [0,1]
    accumulated_cost = [accumulated_cost[i]/accumulated_cost[ppl_size] for i in range(ppl_size+1)]
    accumulated_cost[0] = -0.0000001 # To deal with the case where temp=0
    for i in range(ppl_size):
        temp = random.random()
        privilege_ppl.append([ppl[i] for i in range(ppl_size) if temp > accumulated_cost[i] and temp <= accumulated_cost[i+1]][0])
    privilege_size = ppl_size

    new_ppl = []
    while len(new_ppl) < ppl_size:
        # randomly get two different individuals
        ind1_loc = np.random.randint(privilege_size)
        ind2_loc = np.random.randint(privilege_size)
        while ind2_loc == ind1_loc:
            ind2_loc = np.random.randint(privilege_size)
        ind1 = privilege_ppl[ind1_loc]#get the individual ind1_loc
        ind2 = privilege_ppl[ind2_loc]
        new_ind = crossover(ind1, ind2, par, data, misc, print_switch)

        new_ppl.append(new_ind)
    return new_ppl

def crossover(ind1, ind2, par, data, misc, print_switch):#crossover individuals, ind1 and ind1, and return a new individual, new_ind

    remain_ship_dict = copy.copy(data.ship_dict)
    remain_trailer_dict = copy.copy(data.trailer_dict)
    new_ind = {}
    route_list = list(ind1.values()) + list(ind2.values())
    for i in route_list:#to calculate fitness of each trailer according to cost_function.py
        i.renew_fit()

    while route_list:

        route_list = filter(lambda x: x.fit > 0,route_list)  # To delete those empty trailers
        route_size = min(int(len(route_list)*par.fit_threshold), len(route_list))#to compute numbers of genes to crossover
        route_list.sort(key=lambda x: x.fit, reverse=True)#sort all the individuals according to fitness
        route_list = route_list[:route_size]#get the first privilege_size individuals
        np.random.shuffle(route_list)

        remain_list = []
        while route_list:# crossover to select those trailers meeting requirements into new_ind
            route = route_list.pop()
            if route.id not in remain_trailer_dict:  # pop the route with trailer influenced
                continue
            elif sum(map(lambda x: x not in remain_ship_dict, route.ships)):  # pop the route with ships influenced
                continue
            elif np.random.random() < par.mutant_rate:# Those mutant trailers are skipped and remain in the remain_trailer_dict to be initialized
                continue
            else:
                for i in route.ships:
                    remain_ship_dict.pop(i)
                remain_trailer_dict.pop(route.id)
                new_ind[route.id] = route

        route_list = remain_list

    data = Data(remain_ship_dict, remain_trailer_dict)
    new_ind.update(initialization.initialization(1, data, misc, True)[0])
    return new_ind