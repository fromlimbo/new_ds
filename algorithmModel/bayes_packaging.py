# coding:utf-8

import logging
import pandas as pd
import random
import cPickle as pickle
import operator
import datetime
import numpy as np
import random
import copy
from basic_class import *
# from boundary_test import *
import _temp_tools as tt

# parameters
mix_city_limit = 2
EPISODE = 1
def dealer_cluster(shipment_list, priority='dealer', OTD_emergent = 5):
    # 1. dealer code cluster 2. OTD rank
    if priority == 'dealer':
        dealer_code_list = list(set([shipment.end_loc for shipment in shipment_list]))
        cluster_len = np.zeros(len(dealer_code_list))
        for ii in xrange(len(cluster_len)):
            cluster_len[ii] = len([shipment for shipment in shipment_list
                                   if shipment.end_loc == dealer_code_list[ii]])

        sorted_ind = list(np.argsort(-cluster_len))
        sorted_shipment_list = []
        for ii in sorted_ind:
            temp_list = [shipment for shipment in shipment_list if shipment.end_loc == dealer_code_list[ii]]
            temp_list.sort(key=operator.attrgetter('OTD'), reverse=True)
            sorted_shipment_list.extend(temp_list)
            # print([shipment.end_loc for shipment in temp_list])
            # print([shipment.OTD for shipment in temp_list])
        aa = 1
    # 1. OTD cluster 2. dealer cluster
    else:
        sorted_shipment_list = []
        for ii in xrange(2):
            if ii == 0:
                shipments_temp = [shipment for shipment in shipment_list if shipment.OTD > OTD_emergent]
            else:
                shipments_temp = [shipment for shipment in shipment_list if shipment.OTD <= OTD_emergent]
            dealer_code_list = list(set([shipment.end_loc for shipment in shipments_temp]))
            cluster_len = np.zeros(len(dealer_code_list))
            for ii in xrange(len(cluster_len)):
                cluster_len[ii] = len([shipment for shipment in shipments_temp
                                       if shipment.end_loc == dealer_code_list[ii]])

            sorted_ind = list(np.argsort(-cluster_len))
            sorted_temp = []
            for ii in sorted_ind:
                temp_list = [shipment for shipment in shipments_temp if shipment.end_loc == dealer_code_list[ii]]
                sorted_temp.extend(temp_list)

            sorted_shipment_list.extend(sorted_temp)

    return sorted_shipment_list

# Convert mix-city table into mix-city set
def packaging(shipment_dict, trailer_dict,misc):
    shipment_list = shipment_dict.values()
    trailer_list = trailer_dict.values()
    for i in trailer_list:
        i.shipments_set = []





    trailer_list.sort(key=operator.attrgetter('capacity_for_xl_car'), reverse=True)
    trailer_list.sort(key=operator.attrgetter('capacity_for_l_car'), reverse=True)
    trailer_list.sort(key=operator.attrgetter('capacity_all'), reverse=True)


    total_assigned_shipments = 0
    for i in xrange(len(trailer_list)):
        # print (i)
        shipment_list = dealer_cluster(shipment_list)
        # o = random.uniform(0, 1)
        #
        # if o > 0.5:
        #     shipment_list.sort(key=operator.attrgetter( 'dealer_code'), reverse=True)
        # else:
        #     shipment_list.sort(key=operator.attrgetter('OTD'), reverse=True)
        assigned_shipments = []

        type_num_list = [trailer_list[i].capacity_for_xl_car, trailer_list[i].capacity_for_l_car,
                         trailer_list[i].capacity_for_m_car, trailer_list[i].capacity_for_s_car,
                         trailer_list[i].capacity_for_xs_car]
        w = 0
        while w <len(shipment_list):
            j = 0
            while j < len(shipment_list):
                # try:
                #     if shipment_list[j].
                # Constraint: 2
                if tt.preferred_direction_check(shipment_list[j], trailer_list[i]) == False:
                    j+=1
                    continue

                # Constraint: 3
                # if mix_city_number_check(assigned_shipments, shipment_list[j], mix_city_limit) == False:
                #     j+=1
                #     continue

                # Constraint: 4
                otd_type = 'T+' + str(shipment_list[j].OTD - 1)
                if tt.mix_dealer_check(assigned_shipments, shipment_list[j], misc) == False:
                    j+=1
                    continue

                # Constraint: 6
                if tt.mix_dealer_set_check(assigned_shipments, shipment_list[j], misc) == False:
                    j+=1
                    continue

                # Constraint: 9 - limit for maximum number of warehouse in a trailer
                # otd_type = 'T+' + str(shipment_list[j].OTD - 1)
                if tt.mix_warehouse_number_check(assigned_shipments, shipment_list[j], misc) == False:
                    j+=1
                    continue

                # Constraint: 1 - limit for capacity
                sequence = ['XL', 'L', 'M', 'S', 'XS']
                car_type = shipment_list[j].car_type
                temp = copy.deepcopy(type_num_list)
                if car_type == 'XL' and type_num_list[0] > 0:
                    assigned_shipments.append(shipment_list[j])
                    del (shipment_list[j])
                    j-=1
                    # 向下兼容: 出现需要被兼容的较小型商品车运单时,寻找用最小代价兼容的方法
                    # 也就是说,[XL. L. M. S. XS]中寻找左边最近的不为0的元素,并减去1个空位
                    temp.reverse()
                    sequence.reverse()
                    type_num_list[
                        len(temp) - 1 - next(temp.index(x) for x in temp[sequence.index(car_type):] if x > 0)] -= 1
                elif car_type == 'L' and (type_num_list[0] > 0 or type_num_list[1] > 0):
                    assigned_shipments.append(shipment_list[j])
                    del (shipment_list[j])
                    j-=1
                    temp.reverse()
                    sequence.reverse()
                    type_num_list[
                        len(temp) - 1 - next(temp.index(x) for x in temp[sequence.index(car_type):] if x > 0)] -= 1
                elif car_type == 'M' and (type_num_list[0] > 0 or type_num_list[1] > 0 or type_num_list[2] > 0):
                    assigned_shipments.append(shipment_list[j])
                    del (shipment_list[j])
                    j-=1
                    temp.reverse()
                    sequence.reverse()
                    type_num_list[
                        len(temp) - 1 - next(temp.index(x) for x in temp[sequence.index(car_type):] if x > 0)] -= 1
                elif car_type == 'S' and (
                                        type_num_list[0] > 0 or type_num_list[1] > 0 or type_num_list[2] > 0 or
                                type_num_list[
                                    3] > 0):
                    assigned_shipments.append(shipment_list[j])
                    del (shipment_list[j])
                    j-=1
                    temp.reverse()
                    sequence.reverse()
                    type_num_list[
                        len(temp) - 1 - next(temp.index(x) for x in temp[sequence.index(car_type):] if x > 0)] -= 1
                elif car_type == 'XS' and (
                                            type_num_list[0] > 0 or type_num_list[1] > 0 or type_num_list[2] > 0 or
                                    type_num_list[
                                        3] > 0 or type_num_list[4] > 0):
                    assigned_shipments.append(shipment_list[j])
                    del (shipment_list[j])
                    j-=1
                    temp.reverse()
                    sequence.reverse()
                    type_num_list[
                        len(temp) - 1 - next(temp.index(x) for x in temp[sequence.index(car_type):] if x > 0)] -= 1
                elif len(assigned_shipments)==trailer_list[i].capacity_all:
                    break

                else:
                    j+=1
                    continue

                j+=1
            trailer_list[i].shipments_set = assigned_shipments

            if len(trailer_list[i].shipments_set) == trailer_list[i].capacity_all:
                total_assigned_shipments += trailer_list[i].capacity_all
                break
            else:

                shipment_list.extend(trailer_list[i].shipments_set)
                # random.shuffle(shipment_list)
                # if w%2==0:
                #
                #     shipment_list.sort(key=operator.attrgetter('OTD','start_loc'), reverse=True)
                # else:
                #     shipment_list.sort(key=operator.attrgetter('OTD','dealer_code'), reverse=True)

                # shipment_list.sort(key=operator.attrgetter('car_type'), reverse=True)
                trailer_list[i].shipments_set = []
                assigned_shipments = []
                type_num_list = [trailer_list[i].capacity_for_xl_car, trailer_list[i].capacity_for_l_car,
                                 trailer_list[i].capacity_for_m_car, trailer_list[i].capacity_for_s_car,
                                 trailer_list[i].capacity_for_xs_car]
                w+=1
                shipment_list = dealer_cluster(shipment_list)
                shipment_list = shipment_list[w:len(shipment_list)] + shipment_list[0:w]


    trailer_index = [i.code for i in trailer_list]
    output_column_quantity = max([len(i.shipments_set) for i in trailer_list])
    shipment_index = ['space_'+str(i + 1) for i in xrange(output_column_quantity)]
    matrix_gen = [ None ] * len(trailer_index)
    for i in range(len(trailer_index)):
        matrix_gen[i] = [j.order_code for j in trailer_list[i].shipments_set] + [-1]*(output_column_quantity-len(trailer_list[i].shipments_set))

    solution_out = pd.DataFrame(matrix_gen, index=trailer_index,
                              columns=shipment_index)
    return total_assigned_shipments, solution_out, trailer_list

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


