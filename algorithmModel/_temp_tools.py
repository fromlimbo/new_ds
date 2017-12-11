
# coding:utf-8
"""
This file contains many functions called during genetic algorithm.
"""

# Constraint 2:
def preferred_direction_check(new_shipment, trailer):
    """
    This fuction check whether the input shipment and the input trailer satisfies the preferred direction requirement,
     if yes, return True, else return False
    :param trailer: input trailer
    :param new_shipment: input shipment
    :return: True or False
    """
    return new_shipment.end_city in trailer.preferred_direction

# Constraint 3:
# def mix_city_number_check(shipment_set, new_shipment, max_mix_city_number):
#     city_set = {i.end_loc for i in shipment_set}
#     city_set.add(new_shipment.end_loc)
#     return len(city_set) <= max_mix_city_number

# Constraint 4:
def mix_dealer_check(shipment_set, new_shipment, misc):
    city_list = [i.end_loc for i in shipment_set]
    city_list.append(new_shipment.end_loc)
    city_list = list(set(city_list))
    OTD_list = [shipment_x.OTD for shipment_x in shipment_set]
    OTD_list.append(new_shipment.OTD)

    idx=min(10,max(OTD_list))
    if len(city_list) < 2:
        max_mix_dealer_number = int(misc.OTD_pinche[idx]['cSameVendor'])
    else:
        max_mix_dealer_number = int(misc.OTD_pinche[idx]['cOtherVendor'])

    dealer_set = {i.dealer_str for i in shipment_set}
    dealer_set.add(new_shipment.dealer_str)
    return len(dealer_set) <= max_mix_dealer_number

# Constraint 5:
def availability_check(shipment_set, new_shipment):
    pass

# Constraint 6:
# def mix_city_set_check(shipment_set, new_shipment, mix_city_rule_matrix):
#     destination_temp = [i.end_loc for i in shipment_set]
#     destination_temp.append(new_shipment.end_loc)
#     destination_set = list(set(destination_temp))
#
#     if len(destination_set) < 2:
#         return True
#
#     # 在拼车规则文件mix_city中查找
#     for i in range(len(mix_city_rule_matrix[0])):
#         mix_city_rule = mix_city_rule_matrix[i].values()
#         # If all the end cities are in this list of mix city table, the requirement is satisfied.
#         if len([x for x in destination_set if x not in mix_city_rule]) == 0:
#             return True
#     return False

def mix_dealer_set_check(shipment_set, new_shipment, misc):
    destination_temp = [i.dealer_str for i in shipment_set]
    destination_temp.append(new_shipment.dealer_str)
    destination_set = list(set(destination_temp))

    if len(destination_set) < 2:
        return True
    #在拼经销商规则mix_dealer_rule中查找

    for i in range(len(misc.mix_dealer_rule1[0])):
        mix_dealer_rule = misc.mix_dealer_rule1[i]
        # If all the end cities are in this list of mix city table, the requirement is satisfied.
        if len([x for x in destination_set if x not in mix_dealer_rule]) == 0:
            return True

    return False

# Constraint 9:
def mix_warehouse_number_check(shipment_set, new_shipment, misc):
    max_mix_warehouse_number = 4

    # shipment.start_loc have been used for start warehouse
    warehouse_set = {i.start_loc for i in shipment_set}
    warehouse_set.add(new_shipment.start_loc)
    return len(warehouse_set) <= max_mix_warehouse_number