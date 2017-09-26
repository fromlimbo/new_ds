# coding:utf-8
########################################################################################################################
"""
To set related parameters and start GA based dynamic scheduling by Zhe Ma.

There is no input parameters which need to be adjusted by the scheduling starf.

Input: the data needed in this algorithm is loaded in the packaging.py file.

Output: the output of this program, solution, is printed in the end of the code.
"""
########################################################################################################################
import numpy as np
import datetime
import GAVRP
import cProfile
import re
from packaging import *
from cost_function_ind import *
from Bases import *
from GAVRP import *
from app import celery

weight = [0.0, 0.5, 0.0, 0.5]
epsilon1 = 0.0
epsilon2 = 0.0
num_iteration = 1


# ---------------------------To carry out optimization and record results in result_record.pkl--------------------------#
@celery.task
def optimization(data):
    output = open('result_record.pkl', 'wb')

    for i in range(num_iteration):
        start_time = datetime.datetime.now()
        # ----------------- To generate scheduling solutions through hierarchical mult-object optimization--------------#
        # --------------------------------------------------The first level---------------------------------------------#
        weight_set = [weight[0], weight[1], weight[2], weight[3]]
        extra_weight = [[0, 0, 0, 0], [0, 0, 0, 0]]
        extra_constraint = [0, 0]
        result_temp1 = GAVRP.ga_vrp(data, weight_set, extra_weight, extra_constraint, 5, 0.0001)
        ind1 = result_temp1[len(result_temp1) - 1]

        # ----------------------------  To record the output solutions in pickle file-----------------------------------#
        solution = xmatrix_to_solution(convert_ind_to_matrix(ind1))
        print solution

    return solution