# coding:utf-8
########################################################################################################################
"""
To set related parameters and start GA based dynamic scheduling by Zhe Ma.

There is no input parameters which need to be adjusted by the scheduling starf.

Input: the data needed in this algorithm is loaded in the packaging.py file.

Output: the output of this program, solution, is printed in the end of the code.
"""
########################################################################################################################
import main
from packaging import *
from main import *
from app import celery#for transporting parameters

weight = [0.0, 0.5, 0.0, 0.5]

# ---------------------------To carry out optimization and record results in result_record.pkl--------------------------#
@celery.task(serializer='pickle')
def optimization(data):
    #----------------- To generate scheduling solutions through hierarchical mult-object optimization--------------
    weight_set = [weight[0], weight[1], weight[2], weight[3]]
    ind1 = main.ga_vrp(data, weight_set, 5, 0.0001)
    solution = xmatrix_to_solution(convert_ind_to_matrix(ind1))
    print solution
    return solution