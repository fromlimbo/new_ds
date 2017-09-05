"""
This file contains all the classes used in genetic algorithm.
"""
import _temp_tools as tt
import pandas as pd
import numpy as np
CAR_TYPE_LOC = {'XL': 0, 'L': 1, 'M': 2, 'S': 3, 'XS': 4}


class CrossoverParameters:
    def __init__(self, mutant_rate=0.05, fit_threshold=0, crossover_ratio=1):
        self.mutant_rate = mutant_rate
        self.fit_threshold = fit_threshold
        self.co_ratio = crossover_ratio


class Data:
    def __init__(self, ship_dict, trailer_dict):
        self.ship_dict = ship_dict
        self.trailer_dict = trailer_dict


class AllMightyRoute:
    def __init__(self):
        self.id = 'AllMightyRoute'
        self.ships = {}
        self.fit = -float('Inf')

    def add_ship(self, ship):
        self.ships[ship.order_code] = ship
        return True

    def pop_ship(self, ship_code):
        if ship_code in self.ships:
            self.ships.pop(ship_code)
            return True
        else:
            return False

    def rearrange_ships(self):
        return None

    def renew_fit(self):
        return None

    def to_matrix(self):
        return None


class Route:
    def __init__(self, _trailer, misc):
        self.trailer = _trailer
        self.id = _trailer.code
        self.slot_cap = [_trailer.capacity_for_xl_car,
                         _trailer.capacity_for_l_car,
                         _trailer.capacity_for_m_car,
                         _trailer.capacity_for_s_car,
                         _trailer.capacity_for_xs_car]
        self.slot = [{}, {}, {}, {}, {}]# the list of shipment dictionary
        self.ships = {}# shipment dictionary
        self._ship_loc = {}
        self.misc = misc
        self.fit = 0

    # To add a shipment into this route
    def add_ship(self, ship, bool_log=False):
        # flag = TRUE if ships is empty, simultaneously this ship satisfies preferred direction constraint.
        if not constraints_tier_0(ship, self.trailer):
            return False
        flag = (not len(self.ships)) and constraints_tier_0(ship, self.trailer)
        if not flag:#It is possible that the constraints_tier_0 is not satisfied, i.e, the shipment conflicts with the preferred direction???????????????
            if bool_log:
                flag, bool_list = constraints_tier_1(self.ships.values(), ship, self.misc, full_check=True)
            else:
                flag = constraints_tier_1(self.ships.values(), ship, self.misc)

        if flag:
            car_type = CAR_TYPE_LOC[ship.car_type]
            while car_type >= 0:
                if len(self.slot[car_type]) < self.slot_cap[car_type]:#actual number of cars of this type is smaller than the capacity
                    self.slot[car_type][ship.order_code] = ship
                    self.ships[ship.order_code] = ship
                    self._ship_loc[ship.order_code] = car_type
                    return True
                car_type -= 1
        return False

    def pop_ship(self, ship_code):
        if ship_code not in self.ships:
            return False
        else:
            self.ships.pop(ship_code)
            the_slot_type = self._ship_loc[ship_code]
            self.slot[the_slot_type].pop(ship_code)
            self._ship_loc.pop(ship_code)
            return True

    def rearrange_ships(self):
        self.slot = [{}, {}, {}, {}, {}]
        self._ship_loc = {}
        temp_ship_list = self.ships.values()
        for i in temp_ship_list:
            self.add_ship(i)
        return None

    def renew_fit(self):
        if len(self.ships) == sum(self.slot_cap):
            self.fit = cal_fit(self, self.misc)
        else:
            self.fit = 0

    def renew_trailer(self):
        self.trailer.shipments_set = list(self.ships.values())

    def to_matrix(self):
        matrix = pd.DataFrame()
        for i in self.ships:
            matrix = matrix.append(pd.DataFrame(data=1, index=[i], columns=[self.id], dtype=np.int8))
        matrix = matrix.fillna(0)
        return matrix


def constraints_tier_0(ship, trl):
    """
    This function checks whether the input shipment satisfies the preferred direction requirement when loaded onto the input trailer.
    :param ship: the input shipment
    :param trl: the input trailer
    :return: return True if the constraint is satisfied, otherwise reture False if.
    """
    # Constraint: 2
    return tt.preferred_direction_check(trl, ship)


def constraints_tier_1(as_ships, ship, misc, full_check=False):
    mix_city_limit = 2
    check_list = [True] * 4


    if not tt.mix_city_number_check(as_ships, ship, mix_city_limit):
        if not full_check:
            return False
        else:
            check_list[0] = False

    # Constraint: 4
    if not tt.mix_dealer_check(as_ships, ship, misc):
        if not full_check:
            return False
        else:
            check_list[1] = False

    # Constraint: 6
    if not tt.mix_city_set_check(as_ships, ship, misc.mix_city):
        if not full_check:
            return False
        else:
            check_list[2] = False

    # Constraint: 9 - limit for maximum number of warehouse in a trailer
    if not tt.mix_warehouse_number_check(as_ships, ship, misc):
        if not full_check:
            return False
        else:
            check_list[3] = False

    if not full_check:
        return True
    else:
        return sum(check_list) == 4, check_list


def ppl_cost(ppl, misc, with_optimal_goal=False):
    """
    This function calculate the cost value of the input population.
    :param ppl: the input population
    :param misc: the parameter set
    :param with_optimal_goal: to determine whether the best cost among the input population is returned
    :return: the average cost of the input population and the best cost
    """
    if not with_optimal_goal:
        return float(sum(ind_cost(ind, misc) for ind in ppl)) / len(ppl)
    else:
        cost_list = [ind_cost(ind, misc) for ind in ppl]
        return sum(cost_list)/len(cost_list), max(cost_list)


def convert_ind_to_matrix(ind):
    """
    This function transfer the input individual into the a matrix
    :param ind: the input individual 
    :return: solution matrix
    """
    matrix = pd.DataFrame()
    for _id, route in ind.iteritems():
        if _id != 'AllMightyRoute' and len(route.ships) == sum(route.slot_cap): # To select the trailer whose total number of shipments achieves the capacity volume.
            matrix = matrix.append(route.to_matrix())
    matrix = matrix.fillna(0)
    return matrix


def ind_cost(ind, misc):
    """
    This function calculate the cost of the input individual 
    :param ind: input individual
    :param misc: parameter set
    :return: the cost of the input individual
    """
    return misc.cf(ind, misc.cost_weight,misc.trailer_dict, misc.ship_dict)

def cal_fit(route, misc):
    """
    to calculate fitness according to cost_function, misc.cf
    :param route: a 'gene' in individual
    :param misc: parameter set
    :return: the fitness of the input gene(the set of trailer and loaded shipments)
    """
    return misc.cf({route.id:route}, misc.cost_weight, misc.trailer_dict, misc.ship_dict, True)
