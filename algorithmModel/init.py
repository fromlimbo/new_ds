# coding:utf-8
""""
This file is called by the generic procedure to initialize a new generation.
"""
import copy
from basic_class_GA import *
from packaging import *
import pinche

def initialization(ppl_size, data, misc, flag_crossover=False, print_switch=0, old_genes=None):
    """
    This function generates the initial generation based on raw data.

    :param ppl_size: poplulation size
    :param data: a variable of Data class containing order dictionary and shipment dictionary.
    :param misc: the variable passed by main.py to set parameters
    :param flag_crossover: a flag to indicate whether this initialization is for crossover
    :param print_switch: if print_switch=1, some variables will be printed
    :param old_genes:
    :return: a generation of ppl_size
    """
    logger = logging.getLogger(__name__)

    population = []
    count = 0

    def random_packaging():
        shipment_list = copy.copy(data.ship_dict.values())
        trailer_list = data.trailer_dict.values()

        np.random.shuffle(shipment_list)
        np.random.shuffle(trailer_list)

        if misc.cost_weight[0] > 0.4 or misc.cost_weight[1] > 0.4 or misc.cost_weight[2] > 0.4:
            try:
                trailer_list.sort(key=operator.attrgetter('capacity_for_xl_car'), reverse=True)
                trailer_list.sort(key=operator.attrgetter('capacity_for_l_car'), reverse=True)
                trailer_list.sort(key=operator.attrgetter('capacity_all'), reverse=False)
                #trailer_list.sort(key=operator.attrgetter('priority'), reverse=False)
            except KeyError:
                print "The input trailer data is ineffective!"
                logger.error("The input trailer data is ineffective!")
        if misc.cost_weight[2] > 0.4:
            try:
                shipment_list.sort(key=operator.attrgetter('car_type'), reverse=True)
            except KeyError:
                print "The input shipment data is ineffective!"
                logger.error("The input shipment data is ineffective!")
        if misc.cost_weight[3] > 0.4:
            try:
                shipment_list.sort(key=operator.attrgetter('start_loc'), reverse=False)
                shipment_list.sort(key=operator.attrgetter('dealer_code'), reverse=False)
            except KeyError:
                print "The input shipment data is ineffective!"
                logger.error("The input shipment data is ineffective!")
        if misc.cost_weight[1] > 0.4:
            try:
                shipment_list.sort(key=operator.attrgetter('OTD'), reverse=False)
            except KeyError:
                print "The input shipment data is ineffective!"
                logger.error("The input shipment data is ineffective!")
        gene_list = [ScheduleGene(i, misc) for i in trailer_list]#所有大板车及其装载情况类ScheduleGene的变量组成的列表

        all_mighty_gene = RemainShipsContainer()#The super trailer which can take any shipment which is not taken by normal trailers
        gene_list.append(all_mighty_gene)
        full_pre = 0 #the total number of full trailers in the previous iteration
        full_gene = 1# the total number of full trailers in this iteration
        while full_gene != full_pre:# iteration stops when the number of full trailers cannot be bigger
            full_pre = full_gene
            while shipment_list:#把所有运单都装走
                ship = shipment_list.pop()
                for gene in gene_list:
                    if gene.add_ship(ship):# Added this ship into this gene successfully
                        break
            for gene in gene_list:
                if gene.id == 'RemainShipsContainer' or len(gene.ships) < sum(gene.slot_cap):#If the trailer in this gene is not full
                    shipment_list += list(gene.ships.values())# all the shipments in this trailer are put back into shipment_list
                    gene.ships = {}#this trailer is set empty
                    gene.rearrange_ships()#gene.slot, gene._ship_loc,gene.ships are reset
            full_gene = sum(len(i.ships) == sum(i.slot_cap) for i in gene_list if i.id != 'RemainShipsContainer')# The total number of full trailers

        for i in shipment_list:
            all_mighty_gene.add_ship(i)#To add shipments in shipment_list to the super trailer, all_mighty

        individual = {i.id: i for i in gene_list}

        return individual

    while count < ppl_size:
        count += 1
        ind = random_packaging()#产生一个随机装载方案

        population.append(ind)
        if print_switch > 1:
            print 'Individual: %4d    GoneTrailer: %4d    GoneShips: %4d    RemainShips: %4d' % \
                  (count,
                   sum(len(i.ships) == sum(i.slot_cap) for i in ind.values() if i.id != 'RemainShipsContainer'),
                   sum(len(i.ships) for i in ind.values() if i.id != 'RemainShipsContainer'),
                   len(ind['RemainShipsContainer'].ships)
                   )
            logger.info('Individual: %4d    GoneTrailer: %4d    GoneShips: %4d    RemainShips: %4d' % \
                        (count,
                          sum(len(i.ships) == sum(i.slot_cap) for i in ind.values() if i.id != 'RemainShipsContainer'),
                          sum(len(i.ships) for i in ind.values() if i.id != 'RemainShipsContainer'),
                          len(ind['RemainShipsContainer'].ships)
                          ))
    if not population:
        logger.info("population random initial failed.")
    return population