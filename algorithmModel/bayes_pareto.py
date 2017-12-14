# coding:utf-8

from operator import itemgetter
from numpy import *
import time
#import pandas as pd
#import cPickle as pickle
#import copy
#from multiprocessing.dummy import Pool as ThreadPool
#from basic_class import *
from bayes_packaging import *
from main import *
import pinche

# parameters
mix_city_limit = 2
EPISODE = 1
population_size = 1
sub_population_size =1
# ------------------------ Cost / Value Functions ------------------


#  目标1： 最大化装载数量
def value_car_quantity(solution, separated_mode=False):
    loaded_shipment_num = 0
    loading_capacity = 0

    for trailer_sol in solution:
        loaded_shipment_num += len(trailer_sol.shipments_set)
        loading_capacity += trailer_sol.capacity_all
    if not separated_mode:
        return loaded_shipment_num
    elif separated_mode:
        return float(loaded_shipment_num)
        # return float(loaded_shipment_num)/float(loading_capacity)


#  目标2： 最大化装载商品车紧急程度
def value_priority(solution, separated_mode=False):
    loaded_shipment_num = 0
    total_loaded_priority = 0

    for trailer_sol in solution:
        loaded_shipment_num += len(trailer_sol.shipments_set)
        # print 'len(trailer_sol.shipments_set) = ', len(trailer_sol.shipments_set)
        # total_loaded_priority += sum([shipment_sol.priority for shipment_sol in trailer_sol.shipments_set])
        for shipment_sol in trailer_sol.shipments_set:
            if shipment_sol.OTD >=6:
                total_loaded_priority+=1
        # total_loaded_priority += sum([shipment_sol.OTD for shipment_sol in trailer_sol.shipments_set])

    if not separated_mode:
        return total_loaded_priority
    elif separated_mode:
        return float(total_loaded_priority)
        # return float(total_loaded_priority)/float(loaded_shipment_num*max_priority + 1)


#  目标3： 最大化大、中型商品车数量
def value_large_cars_quantity(solution_x,misc):
    loaded_big_car_num = 0

    for trailer_sol in solution_x:
        for shipment_sol in trailer_sol.shipments_set:
            if shipment_sol.car_type in ['L', 'XL']:
                loaded_big_car_num += 1

    total_trailer_capacity = sum([i.capacity_all for i in misc.trailer_dict.values()])

    # return float(loaded_big_car_num)/float(total_trailer_capacity)
    return float(loaded_big_car_num)

#  目标4:最小化异地拼车数量
def val_mix_city_num(solution_x):
    mix_city_number = 0
    trailer_number = 0
    for trailer_i in solution_x:
        if len(trailer_i.shipments_set) != 0:
            trailer_number+=1
        mix_city_number += len({shipment_j.end_city for shipment_j in trailer_i.shipments_set})
    # return float(mix_city_number)/float(mix_city_limit * len(solution_x))
    return float(trailer_number)/float(mix_city_number)


#  目标5:最小化经销商拼车数量
def val_mix_dealer_num(solution_x):
    load_info,order_info=ind_info(solution_x)
    load_rate = pinche.load_rate(load_info, order_info)
    average_load_rate = np.mean(load_rate)
    return average_load_rate


#  目标8:最小化可拼库区数量
def val_mix_warehouse_num(solution_x):
    mix_warehouse_number = 0
    trailer_number = 0
    for trailer_i in solution_x:
        if len(trailer_i.shipments_set) != 0:
            trailer_number+=1
        mix_warehouse_number += len({shipment_j.start_loc for shipment_j in trailer_i.shipments_set})
    # return float(mix_warehouse_number) / float(max(OTD_pinche['cSameWarehouse']) * len(solution_x))

    return (float(trailer_number)/float(mix_warehouse_number))

# 目标：最大化拼车装载量
def max_load_rate(solution_x):
    load_info, order_info = ind_info(ind)
    load_rate = pinche.load_rate(load_info, order_info)
    average_load_rate = np.mean(load_rate)
    return average_load_rate

def mix_city_num(solution_x):
    mix_city_number = 0
    trailer_number = 0
    for trailer_i in solution_x:
        mix_city_number += len({shipment_j.end_city for shipment_j in trailer_i.shipments_set})
    # return float(mix_city_number)/float(mix_city_limit * len(solution_x))
    return mix_city_number
def mix_dealer_num(solution_x):
    mix_dealer_number = []

    trailer_number = 0
    for trailer_i in solution_x:
        mix_dealer_number.append( len({shipment_j.dealer_code for shipment_j in trailer_i.shipments_set}))
    # return float(mix_dealer_number)/float(max(OTD_pinche['cOtherVendor']) * len(solution_x))
    return max(mix_dealer_number)
def mix_warehouse_num(solution_x):
    mix_warehouse_number = 0
    trailer_number = 0
    for trailer_i in solution_x:
        mix_warehouse_number += len({shipment_j.start_loc for shipment_j in trailer_i.shipments_set})
    # return float(mix_warehouse_number) / float(max(OTD_pinche['cSameWarehouse']) * len(solution_x))
    return mix_warehouse_number

def value_obj_level1(solution,separated_mode=True):
    return value_car_quantity(solution, separated_mode)

def value_obj_level2(solution,separated_mode=True):
    return value_priority(solution, separated_mode)

def value_obj_level3(solution_x,misc):
    return value_large_cars_quantity(solution_x,misc)

def value_obj_level4(solution_x):
    return val_mix_city_num(solution_x)

def value_obj_level5(solution_x):
    return val_mix_dealer_num(solution_x)

def value_obj_level6(solution_x):
    return val_mix_warehouse_num(solution_x)

# ------------------------ Program Start ---------------------------
# Initialize the population with a size of population_size
def population_gen(population_size,data,misc):
    population = []
    for i in range(population_size):
        total_assigned_shipments, solution_matrix, solution_output = packaging(data.ship_dict, data.trailer_dict,misc)
        solution_output1 = copy.deepcopy(solution_output)
        solution_output2 = [i for i in solution_output1 if i.shipments_set != []]
        if solution_output2 != []:
            population.append(solution_output2)
    population_stat(population)
    return population


# Population Sort by Rank ()
def non_domination_sort_by_rank(population, misc, present=False):
    population_tuple = [[i, value_obj_level1(i),value_obj_level2(i), value_obj_level3(i,misc), value_obj_level5(i)] for i in population]
    for i in xrange(len(population_tuple)):
        dominated_num = 0
        for j in xrange(len(population_tuple)):
            if population_tuple[j][1] <population_tuple[i][1]:
                dominated_num += 1
        population_tuple[i].append(dominated_num)

    population_tuple_sorted = sorted(population_tuple, key=itemgetter(5), reverse=True)
    population_sorted = [k[0] for k in population_tuple_sorted]

    if not present:
        return population_sorted

    if present:
        if population_sorted ==[]:
            return [],[],0
        else:
            population_matrix_index = ['+']

            # assigned_order_number:
            assigned_order_number_vector = []
            # assigned_trailer_number:
            assigned_trailer_number_vector = []
            # emergent_order_number:
            emergent_order_number_vector = []
            # large_medium_order_number：
            large_medium_order_number_vector = []
            assigned_mix_city_vector = []
            assigned_mix_dealer_vector = []
            assigned_mix_warehouse_vector = []

            # one_city_one_dealer_number:
            one_city_one_dealer_number_vector = []
            # one_city_two_dealer_number:
            one_city_two_dealer_number_vector = []
            # one_city_three_dealer_number:
            one_city_three_dealer_number_vector = []
            # two_city_two_dealer_number:
            two_city_two_dealer_number_vector = []
            # two_city_three_dealer_number:
            two_city_three_dealer_number_vector = []
            # population_matrix
            solution_seq = 0
            # pareto_set_size = population_sorted_rank.count(0)
            # print 'pareto_set_size = ', pareto_set_size
            max_space_num = max([max([len(trailer_j.shipments_set) for trailer_j in solution_i]) for solution_i in population_sorted])
            population_matrix_data = array(['*'] * max_space_num)
            load_info = {}
            order_info = {}


            for solution_i in population:
                load_info, order_info = ind_info(solution_i)
                route = pinche.trailer_route(load_info, order_info)
                assigned_order_number = 0
                assigned_trailer_number = 0
                emergent_order_number = 0
                large_medium_order_number = 0
                mix_city_number_list = []
                mix_dealer_number_list = []
                one_city_one_dealer_number = 0
                one_city_two_dealer_number = 0
                one_city_three_dealer_number = 0
                two_city_two_dealer_number = 0
                two_city_three_dealer_number = 0
                for trailer_j in solution_i:
                    assigned_order_number += len(trailer_j.shipments_set)
                    population_matrix_index.append(trailer_j.code)
                    population_matrix_data = vstack((population_matrix_data, array([order_j.order_code for order_j in trailer_j.shipments_set]
                    + [' '] * (max_space_num - len(trailer_j.shipments_set)))))
                    mix_city_number_list.append(len({order_j.end_city for order_j in trailer_j.shipments_set}))
                    mix_dealer_number_list.append(len({order_j.dealer_code for order_j in trailer_j.shipments_set}))
                    if len(trailer_j.shipments_set) == trailer_j.capacity_all:
                        assigned_trailer_number += 1
                    for order_z in trailer_j.shipments_set:
                        if order_z.OTD >= 6:
                            emergent_order_number += 1
                        if order_z.car_type in ['L', 'XL']:
                            large_medium_order_number += 1
                assigned_mix_city_vector.append(mix_city_num(solution_i))
                assigned_mix_dealer_vector.append(mix_dealer_num(solution_i))
                assigned_mix_warehouse_vector.append(mix_warehouse_num(solution_i))
                assigned_order_number_vector.append(assigned_order_number)
                assigned_trailer_number_vector.append(assigned_trailer_number)
                emergent_order_number_vector.append(emergent_order_number)
                large_medium_order_number_vector.append(large_medium_order_number)

                one_city_one_dealer_number_vector.append(one_city_one_dealer_number)
                one_city_two_dealer_number_vector.append(one_city_two_dealer_number)
                one_city_three_dealer_number_vector.append(one_city_three_dealer_number)
                two_city_two_dealer_number_vector.append(two_city_two_dealer_number)
                two_city_three_dealer_number_vector.append(two_city_three_dealer_number)

                solution_split_line = array(['Solution: ' + str(solution_seq)] + ['*'] * (max_space_num-1))
                population_matrix_index.append('+')
                population_matrix_data = vstack((population_matrix_data, solution_split_line))
                solution_seq += 1

            # output the summary and the population_sorted


            summary_columns = ['带走运单数', '轿运车使用数量', '运走紧急订单数量', '带走大中型商品车数量', '拼城市数量', '拼经销商数量',
                               '拼库数量']
            summary_index = ['Solution'+str(i+1) for i in xrange(len(population_sorted))]
            summary_data = transpose(array([assigned_order_number_vector, assigned_trailer_number_vector, emergent_order_number_vector,
                            large_medium_order_number_vector, assigned_mix_city_vector,assigned_mix_dealer_vector,assigned_mix_warehouse_vector]))
            summary = pd.DataFrame(summary_data, index=summary_index, columns=summary_columns)
            print summary
            #summary.to_csv('../output_data/summary.csv')
            #print '\n The summary of the solutions has been saved to "output_data/summary.csv" '

            # Generate the solution matrix

            population_matrix_columns = ['space_' + str(i + 1) for i in xrange(max_space_num)]
            population_matrix = pd.DataFrame(population_matrix_data, index=population_matrix_index, columns=population_matrix_columns)
            # population_matrix.to_csv('../output_data/solutions.csv')
            #
            # summary_pickle = open('../output_data/summary.pkl', 'wb')
            # pickle.dump(summary, summary_pickle)
            # summary_pickle.close()
            #
            # solutions_pickle = open('../output_data/solutions.pkl', 'wb')
            # pickle.dump(population_matrix, solutions_pickle)
            # solutions_pickle.close()


            # solution to matrix
            solution = population[0]
            assert (len(population[0]) != 0)
            space_list = population_matrix_columns
            solution_matrix = pd.DataFrame(index=[trailer.code for trailer in solution], columns=space_list)

            for trailer in solution:
                shipment_code_list = [shipment.order_code for shipment in trailer.shipments_set]
                for ii in xrange(len(space_list)):
                    if ii < len(shipment_code_list):
                        solution_matrix.loc[trailer.code, space_list[ii]] = shipment_code_list[ii]
                    else:
                        solution_matrix.loc[trailer.code, space_list[ii]] = -1

            solution_matrix = pd.concat([route, solution_matrix], axis=1)
            #print(solution_matrix)
            return population_sorted,solution_matrix,route.shape[1]


# Update the population
def population_update(population, sup_population):
    population[len(population) - len(sup_population):] = sup_population
    return population


# Solution statistics
def population_stat(population_tested):
    for solution_i in population_tested:
        solution_order_num = 0
        for trailer_j in solution_i:
            solution_order_num += len(trailer_j.shipments_set)
        print 'Solution order number is: ', solution_order_num


def ind_info(solution):
    load_info = {}
    order_info = {}
    for i in solution:
        if len(i.shipments_set)==i.capacity_all:
            load_info[i.code]=[j.order_code for j in i.shipments_set]
            for ship in i.shipments_set:
                order_info[ship.order_code]=ship
    return load_info, order_info

def run(input_data):
    #start=time.clock()
    logger = logging.getLogger(__name__)
    try:
        misc = gen_misc(None, input_data)
    except KeyError:
        print "Ineffective input data!"
        logger.error("Ineffective input data!")
    data = Data(misc.ship_dict, misc.trailer_dict)

    #print '\n -------------------------- Parallel Computing ----------------------------- \n'
    #print '\n ---------- Version I  Serial Computing----------------------------- \n'
    population = population_gen(population_size,data,misc)
    for i in xrange(EPISODE):
        print 'Episode: ' + str(i+1)
        population = non_domination_sort_by_rank(population,misc)
        sup_population = population_gen(sub_population_size,data,misc)
        population = population_update(population, sup_population)

    #print '\n -------------------------- Result Report ----------------------------- \n'
    #print '\n The statistics of the result information : \n'
    population,solution_matrix,length = non_domination_sort_by_rank(population,misc, present=True)
    #summary_reader = pickle.load(open('../output_data/summary.pkl', 'rb'))
    #print 'summary_reader = \n', summary_reader
    if (len(population)==0):
        return False,solution_matrix,0
    #end = time.clock()
    #print '\n The total time cost by the Pareto MC algorithm (by second) is: ', end - start
    return True,solution_matrix,length