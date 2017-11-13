#!/usr/bin/python2
#  coding:utf-8
""""
This file is the main file called by test.py.

Input: all the parameters used in genetic algorithm.

Output: the best individual during evolution.
"""
import init
import crossover as co
import copy
from basic_class_GA import *
import logging
import pinche
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

max_step_para = 10  # The maximum of iteretion
converge_gap_para = 0.0001  # The converge gap between two continuous iterations when the algorithm stops
ppl_size_para = 5  # The population size
mutant_rate_para = 0.3
fit_threshold_para = 0.5  # The percentage of full loaded trailers (genes whose fitness are bigger than 0.0) which remain during crossover
crossover_ratio_para = 0.6  # To select individuals remaining to crossover. This parameter is useless when wheel disc is used.


class Misc:
    """
    This class contains parameters and operations needed during the whole algorithm
    """
    def __init__(self, cost_weight):
        self.mix_city = None
        self.OTD_pinche = None
        self.mix_dealer_rule = None
        self.ship_dict = None
        self.trailer_dict = None
        self.cost_computation = None#Cost_computation is the ind_cost_computation() in ind_cost_function.py. This reference is made in gen_misc().
        self.cost_weight = cost_weight


def gen_misc(cost_weight, _data):
    """
    To package some frequently used variables into the class Misc.

    :param cost_weight: the weights to determine importance of different optimization objects.
    :return: a variable of class Misc
    """

    import ind_cost_function as pk
    misc = Misc(cost_weight)
    misc.mix_city = _data['mix_city']
    misc.OTD_pinche = _data['OTD_pinche']
    misc.ship_dict = copy.deepcopy(_data['order_dict'])
    misc.trailer_dict = copy.deepcopy(_data['trailer_dict'])
    misc.mix_dealer_rule = gen_mix_dealer_rule(misc)
    misc.cost_computation = pk.ind_cost_computation

    return misc

def gen_mix_dealer_rule(misc):
    """

    :param ship_dict:
    :return:
    """
    list = [[None for j in range(3)] for i in range(len(misc.ship_dict))]
    dealer_index = ['dealer_code'] + ['end_loc_longitude'] + ['end_loc_latitude']
    i = 0
    for ship_info in misc.ship_dict.values():
        list[i][0] = ship_info.dealer_code
        list[i][1] = int(ship_info.end_loc_longitude)
        list[i][2] = int(ship_info.end_loc_latitude)
        i += 1
    dealer_rule = pd.DataFrame(list, index=misc.ship_dict.keys(), columns=dealer_index)
    dealer_rule = dealer_rule.drop_duplicates('dealer_code')
    dealer_rule = dealer_rule.reset_index(drop=True)
    dealer_rule = pinche.find_nearest_id(dealer_rule)

    return dealer_rule.as_matrix(columns=None)

def ga_vrp(_data, cost_weight=[0.6, 0.4, 0, 0], ppl_size=ppl_size_para, converge_gap=converge_gap_para, max_steps=max_step_para, print_switch=2):
    """
    To perform GA iteratively until stop condition is met.

    :param cost_weight: weights to determine importance of optimization objects.
    :param ppl_size: population size of each generation.
    :param converge_gap: the gap between object values of two continuous generations when the iteration stops.
    :param max_steps: the number of max steps to stop iteration.
    :param print_switch: the bool value to determine whether variables should be printed.
    :return: the individual set containing the last generation and the best individual among all the individuals during evolution.
    """
    try:
        misc = gen_misc(cost_weight, _data)
    except KeyError:
        print "Ineffective input data!"
        logging.error("Ineffective input data!")
    data = Data(misc.ship_dict, misc.trailer_dict)  # build a new variant of Data class, containing shipment dictionary and trailer dictionary
    co_par = CrossoverParameters(mutant_rate_para, fit_threshold_para, crossover_ratio_para)  # set a variant containing crossover ratio, fitness threshold and mutant rate


    # To generate the initial solution population
    ppl = init.initialization(ppl_size, data, misc, False, print_switch)
    # To calculate the best individual in the initial population
    ave_goal, optimal_goal, optimal_ind = ppl_cost(ppl, misc, with_optimal_goal=True)
    ave_goal_pre = float('-Inf')
    best_value = optimal_goal
    best_ind = optimal_ind

    # The iteration stops when the gap bwteen the previous goal value and the present goal is small enough or algorithm iterates for enough times
    stop_count = 3  # To record how many continuous times the algorithm stops get better we can determin to quit optimization.
    stay_flag = False  # To record whehther the algorithm stays and doesn't achieve better objects.
    step = 1

    while stop_count and step < max_steps:
        if np.abs(ave_goal - ave_goal_pre) < converge_gap and not stay_flag:
            stop_count = 3
            stay_flag = True
        if np.abs(ave_goal - ave_goal_pre) < converge_gap and stay_flag:
            stop_count -= 1
            stay_flag = True
        if np.abs(ave_goal - ave_goal_pre) > converge_gap:
            stay_flag = False
        ave_goal_pre = ave_goal
        ppl = co.co_pro(ppl, co_par, data, misc, print_switch)
        ave_goal, optimal_goal, optimal_ind = ppl_cost(ppl, misc, with_optimal_goal=True)
        logging.info('OptimalIndividual   GoneTrailer: %4d    GoneShips: %4d    RemainShips: %4d' % \
                     (sum(len(i.ships) == sum(i.slot_cap) for i in optimal_ind.values() if i.id != 'RemainShipsContainer'),
                      sum(len(i.ships) for i in optimal_ind.values() if i.id != 'RemainShipsContainer'),
                      len(optimal_ind['RemainShipsContainer'].ships)
                      ))
        if optimal_goal > best_value:
            best_ind = optimal_ind
            best_value = optimal_goal
        step += 1

    return best_ind