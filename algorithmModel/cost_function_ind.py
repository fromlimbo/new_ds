# coding:utf-8
""""
This file computes all the optimization targets when the solution is described with dictionary.
"""
from packaging import *

####################################################################################################################
#----------------------------------------------- 已有ind词典情况下，封装所有目标为一个函数-------------------------------------#
############################################################################################################3##########

def cost_computation_ind(ind, weight_set, trailer_dict=None, shipment_dict=None, GeneEvaluate=False):
    """
    This function computes optimization object of the input individual or gene
    :param trailer_dict:
    :param shipment_dict:
    :param ind: the input individual or gene
    :param weight_set: weights to describe relative importance of all the optimization objects
    :param GeneEvaluate: the input is a gene instead of an individual when GeneEvaluate = True
    :return: evaluated value of the input individual or gene
    """

    normalized_cost_result = []# To record 6 normolized cost values, which will be returned.
    num_of_loaded_shipments = 0
    num_of_high_priority = 0
    num_of_big_car = 0
    num_of_mix_city = 0
    num_of_mix_dealer = 0
    num_of_mix_warehouse = 0
    num_trailer = 0

    for i in ind.values():
        if i.id != 'AllMightyRoute' and len(i.ships) == sum(i.slot_cap):
            num_trailer += 1
            num_of_loaded_shipments += len(i.ships)
            num_of_high_priority += len([x_ship for x_ship in i.ships.values() if x_ship.OTD > 2])
            num_of_big_car += len([x_ship for x_ship in i.ships.values() if x_ship.car_type in ['L', 'XL']])
            num_of_mix_city += len(set([x_ship.end_loc for x_ship in i.ships.values()]))
            num_of_mix_dealer += len(set([x_ship.dealer_code for x_ship in i.ships.values()]))
            num_of_mix_warehouse += len(set([x_ship.start_loc for x_ship in i.ships.values()]))

    # ------------------------------------------- 测试目标1:最大化装载数 --------------------------------------------------#
    if GeneEvaluate:
        normalized_cost_result.append(float(num_of_loaded_shipments) / float(sum(i.slot_cap)))
    else:
        num_of_loading_capacity = sum([i.capacity_all for i in trailer_dict.values()])
        normalized_cost_result.append(float(num_of_loaded_shipments) / float(num_of_loading_capacity))
    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------- 测试目标2:最大化装载商品车紧急程度 ----------------------------------------#
    if GeneEvaluate:
        normalized_cost_result.append(float(num_of_high_priority) / float(num_of_loaded_shipments))
    else:
        num_of_urgent_shipment = len([i.order_code for i in shipment_dict.values() if i.OTD > 2])
        normalized_cost_result.append(float(num_of_high_priority) / float(min(num_of_loading_capacity, num_of_urgent_shipment)))
    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------- 测试目标3:最大化大、中型商品车数量 ----------------------------------------#
    if GeneEvaluate:
        normalized_cost_result.append(float(num_of_big_car) / float(num_of_loaded_shipments))
    else:
        total_num_of_big_car = len([i.order_code for i in shipment_dict.values() if i.car_type in ['L', 'XL']])
        big_car_capacity = sum([i.capacity_for_xl_car + i.capacity_for_l_car for i in trailer_dict.values()])
        normalized_cost_result.append(float(num_of_big_car) / float(min(total_num_of_big_car,big_car_capacity)))
    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------- 测试目标4:最小化异地拼车数量 ---------------------------------------------#
    average_mix_city = float(num_of_mix_city) / float(num_trailer)
    #------------------------------------------------------------------------------------------------------------------#


    #------------------------------------------- 测试目标5:最小化经销商拼车数量 --------------------------------------------#
    average_mix_dealer = float(num_of_mix_dealer) / float(num_trailer)
    #------------------------------------------------------------------------------------------------------------------#


    #------------------------------------------- 测试目标8:最小化拼车库区数量 ---------------------------------------------#
    average_mix_warehouse = float(num_of_mix_warehouse) / float(num_trailer)
    #------------------------------------------------------------------------------------------------------------------#

    normalized_cost_result.append(float(6+3+12) / float(6*average_mix_dealer + 3*average_mix_warehouse + 12*average_mix_city))
    return float(np.dot(np.array(weight_set), (np.array(normalized_cost_result).T)))
