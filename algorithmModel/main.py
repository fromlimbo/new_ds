#!/usr/bin/python2
#  coding:utf-8
""""
This file is the main file called by algorithm_entry.py.

Input: all the parameters used in genetic algorithm.

Output: the best individual during evolution.
"""
import initialization
import crossover as co
import copy
from Bases import *

max_step_para = 10  # The maximum of iteretion
converge_gap_para = 0.0001  # The converge gap between two continuous iterations when the algorithm stops
ppl_size_para = 5  # The population size
mutant_rate_para = 0.3
fit_threshold_para = 0.5  # The percentage of full loaded trailers (genes whose fitness are bigger than 0.0) which remain during crossover
crossover_ratio_para = 0.6  # To select individuals remaining to crossover. This parameter is useless when wheel disc is used.

class Misc:
    def __init__(self, cost_weight, extra_weight, extra_constraint):
        self.mix_city = None
        self.OTD_pinche = None
        # self.otd_type = None
        self.ship_dict = None
        self.trailer_dict = None
        self.x2s = None
        self.cf = None
        self.bd = None
        self.cost_weight = cost_weight
        self.extra_weight = extra_weight
        self.extra_constraint = extra_constraint


def gen_misc(cost_weight, extra_weight, extra_constraint,_data):
    """
    To package some frequently used variables into the class Misc.

    :param cost_weight: the weights to determine importance of different optimization objects.
    :param extra_weight: the weights to determine importance of different constraints.
    :param extra_constraint: the boundary of constraints.
    :return: a variable of class Misc
    """

    import cost_function_ind as pk
    misc = Misc(cost_weight, extra_weight, extra_constraint)
    misc.mix_city = _data['mix_city']
    misc.OTD_pinche = _data['OTD_pinche']
    misc.ship_dict = copy.deepcopy(_data['order_dict'])
    misc.trailer_dict = copy.deepcopy(_data['trailer_dict'])
    misc.cf = pk.cost_computation_ind
    return misc


def ga_vrp(_data, cost_weight=[0.6, 0.4, 0, 0], extra_weight=[[0, 0, 0, 0], [0, 0, 0, 0]], extra_constraint=[0, 0],
           ppl_size=ppl_size_para, converge_gap=converge_gap_para, max_steps=max_step_para, print_switch=2,):
    """
    To perform GA iteratively until stop condition is met.
    :param data from processing function
    :param cost_weight: weights to determine importance of optimization objects.
    :param extra_weight: weights to determine importance of different constraints.
    :param extra_constraint: weights to determine boundaries of constraints.
    :param ppl_size: population size of each generation.
    :param converge_gap: the gap between object values of two continuous generations when the iteration stops.
    :param max_steps: the number of max steps to stop iteration.
    :param print_switch: the bool value to determine whether variables should be printed.
    :return: the individual set containing the last generation and the best individual among all the individuals during evolution.
    """
    misc = gen_misc(cost_weight, extra_weight, extra_constraint,_data)
    data = Data(misc.ship_dict,
                misc.trailer_dict)
    # build a new variant of Data class, containing shipment dictionary and trailer dictionary

    co_par = CrossoverParameters(mutant_rate_para, fit_threshold_para,
                                 crossover_ratio_para)  # set a variant containing crossover ratio, fitness threshold and mutant rate

    if print_switch > 0:
        print '#' * 80
        print '###' + ' ' * 25 + 'Genetic Algorithm Start' + ' ' * 26 + '###'
        print '#' * 80
        print 'Shipments Number: %d' % len(data.ship_dict)
        print 'Trailer Number: %d' % len(data.trailer_dict)
        print 'Population Size: %d' % ppl_size
        print 'Convergence Check: %f' % converge_gap
        print 'Mutant Rate: %f' % co_par.mutant_rate
        print 'Fitness Threshold: %f' % co_par.fit_threshold
        print 'Privilege Ratio: %f' % co_par.co_ratio
        print ''
        print '-' * 30 + 'Initialization Begin' + '-' * 30
        print ''
    ppl = initialization.initialization(ppl_size, data, misc, False, print_switch)  # generate initial solution population
    if print_switch > 0:
        print ''
        print '-' * 31 + 'Initialization End' + '-' * 31
        print ''
    ave_goal_pre, optimal_goal = ppl_cost(ppl, misc, with_optimal_goal=True)
    optimal_ind_loc = max((ind_cost(ppl[x], misc), x) for x in xrange(len(ppl)))[
        1]  # To select the best individual whose cost is the biggest
    best_ind = ppl[optimal_ind_loc]  # 记录整个遗传进化过程中最好的个体
    best_value = ind_cost(ppl[optimal_ind_loc], misc)
    if print_switch > 0:
        print 'InitialGeneration   AverageGoal: %5f    OptimalGoal: %5f' % (ave_goal_pre, optimal_goal)
    ave_goal = float('Inf')
    step = 1
    if print_switch > 0:
        print ''
        print '-' * 31 + 'Reproducing  Begin' + '-' * 31
        print ''
    # The iteration stops when the gap bwteen the previous goal value and the present goal is small enough or algorithm iterates
    # for enough times


    solution_ind_set = []
    stop_count = 3  # To record how many continuous times the algorithm stops get better we can determin to quit optimization. We use stop_count to count down.
    stay_flag = False  # To record whehther the algorithm stays and doesn't achieve better objects.
    while stop_count and step < max_steps:
        if np.abs(ave_goal - ave_goal_pre) < converge_gap and not stay_flag:
            stop_count = 3
            solution_ind_set = []
            optimal_ind_loc = max((ind_cost(ppl[x], misc), x) for x in xrange(len(ppl)))[
                1]  # To select the best individual whose cost is the biggest
            optimal_ind = ppl[optimal_ind_loc]
            solution_ind_set.append(optimal_ind)
            stay_flag = True
        if np.abs(ave_goal - ave_goal_pre) < converge_gap and stay_flag:
            stop_count -= 1
            stay_flag = True
            optimal_ind_loc = max((ind_cost(ppl[x], misc), x) for x in xrange(len(ppl)))[
                1]  # To select the best individual whose cost is the biggest
            optimal_ind = ppl[optimal_ind_loc]
            solution_ind_set.append(optimal_ind)
        if np.abs(ave_goal - ave_goal_pre) > converge_gap:
            stay_flag = False
        ave_goal_pre = ave_goal
        ppl = co.co_pro(ppl, co_par, data, misc, print_switch)
        ave_goal, optimal_goal = ppl_cost(ppl, misc, with_optimal_goal=True)
        optimal_ind_loc = max((ind_cost(ppl[x], misc), x) for x in xrange(len(ppl)))[
            1]  # To select the best individual whose cost is the biggest
        if ind_cost(ppl[optimal_ind_loc], misc) > best_value:
            best_ind = ppl[optimal_ind_loc]
            best_value = ind_cost(ppl[optimal_ind_loc], misc)
        if print_switch > 1:
            print 'Generation: %4d    AverageGoal: %5f    OptimalGoal: %5f' % (step, ave_goal, optimal_goal)
        step += 1

    if print_switch > 0:
        print ''
        print '-' * 32 + 'Reproducing  End' + '-' * 32

    optimal_ind_loc = max((ind_cost(ppl[x], misc), x) for x in xrange(len(ppl)))[
        1]  # To select the best individual whose cost is the biggest
    optimal_ind = ppl[optimal_ind_loc]
    solution_ind_set.append(best_ind)

    if print_switch > 0:
        print 'OptimalIndividual   GoneTrailer: %4d    GoneShips: %4d    RemainShips: %4d' % \
              (sum(len(i.ships) == sum(i.slot_cap) for i in best_ind.values() if i.id != 'AllMightyRoute'),
               sum(len(i.ships) for i in best_ind.values() if i.id != 'AllMightyRoute'),
               len(best_ind['AllMightyRoute'].ships)
               )
        print '#' * 80
        print '###' + ' ' * 26 + 'Genetic Algorithm End' + ' ' * 27 + '###'
        print '#' * 80

    return solution_ind_set
