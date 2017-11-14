# coding:utf-8
""""
This file load all the raw data need in scheduling for the whole program.

Input: data_117_0626.pkl

Output: All the data related variants, e.g. order_dict, shipment_dict, etc.
"""
from basic_class import *
import pandas as pd
import cPickle as pickle
import operator
import datetime
import numpy as np
import copy
import logging

Logger = logging.getLogger(__name__)
# parameters
mix_city_limit = 2
mix_dealer_limit = 2

def xmatrix_generation(trailer_list, shipment_list):
    trailer_index = [i.code for i in trailer_list]
    shipment_index = [i.order_code for i in shipment_list]
    matrix_gen = np.zeros([len(shipment_index), len(trailer_list)])
    x_matrix = pd.DataFrame(matrix_gen, index=shipment_index, columns=trailer_index)
    for i in trailer_list:
        if i.shipments_set:
            for j in range(len(i.shipments_set)):
                row = shipment_index.index(i.shipments_set[j].order_code)
                col = trailer_index.index(i.code)
                x_matrix.iloc[row, col] = 1
    return x_matrix

def xmatrix_to_solution(x_matrix,route):
    ####----------step1----------####
    trailer_index = []
    for i in range(x_matrix.shape[1]):
        trailer_index.append(x_matrix.columns[i])
    ####----------step2----------####
    temp_dict = dict()
    for i in range(x_matrix.shape[1]):
        i_trailer_list = []
        for j in range(x_matrix.shape[0]):
            if x_matrix.iloc[j, i] == 1:
                i_trailer_list.append(x_matrix.index[j])#shipments
        temp_dict[x_matrix.columns[i]] = i_trailer_list
    output_column_quantity = max([len(temp_dict[trailer_index[x]]) for x in range(len(trailer_index))])
    ####----------step3----------####
    shipment_index = ['city1']+['city2']+['space_'+str(i + 1) for i in xrange(output_column_quantity)]
    ####----------step4----------####
    matrix_gen = [ None ] *len(trailer_index)
    ####----------step5----------####
    city1 = []
    city2 = []
    for city in route:
        city1.append(city[0])
        city2.append(city[1])
    for i in range(len(trailer_index)):
        ####----------step6----------####
        lst=temp_dict[trailer_index[i]]
        l=len(temp_dict[trailer_index[i]])
        matrix_gen[i] = lst + [-1]*(output_column_quantity-l)
        matrix_gen[i].sort(reverse=True)
        matrix_gen[i].insert(0,city2[i])
        matrix_gen[i].insert(0, city1[i])
    ####----------step7----------####
    solution = pd.DataFrame(matrix_gen, index=trailer_index,
                          columns=shipment_index)

    return solution