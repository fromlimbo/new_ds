# -*- coding: utf-8 -*-

# import numpy as np
import pandas as pd
################################################################################
class order:
    def __init__(self, order_code, customer_code, dealer_code, OTD, priority, VIN,
                 shipment_code_set, start_loc, end_city, end_loc, created_time, effective_time,
                 car_type, transport_type):
        self.order_code = order_code
        self.customer_code = customer_code
        self.dealer_code = dealer_code
        self.OTD = OTD
        self.priority = priority
        self.VIN = VIN
        self.shipment_code_set = shipment_code_set
        self.start_loc = start_loc
        self.end_city = end_city
        self.end_loc = end_loc
        self.created_time = created_time
        self.effective_time = effective_time
        self.car_type = car_type
        self.transport_type = transport_type
        self.time_line = pd.DataFrame({},[], [])

    def add_time_line(self, time_str, effective_time_t, priority_t, shipment_set_t):
        temp_index = [self.time_line.index[j] for j in range(0, len(self.time_line.index))]
        temp_index.append(time_str)
        temp_df = pd.DataFrame({}, temp_index, columns=['effective time', 'priority', 'shipment set'])
        temp_loc = len(self.time_line.index)
        for i in range(0, temp_loc):
            temp_df.loc[i] = self.time_line.loc[i]
        temp_df.loc[time_str] = [effective_time_t, priority_t, shipment_set_t]
        self.time_line = temp_df
        return True
    
    def change_time_line(self, time_str, effective_time_t, priority_t, shipment_set_t):
        self.time_line.loc[time_str] = [effective_time_t, priority_t, shipment_set_t]
        return True

class shipment:
    def __init__(self, shipment_code, dealer_code, order_code, customer_code, OTD, priority, VIN,
                 start_loc, end_city, end_loc, effective_time, car_type, transport_type):
        self.shipment_code = shipment_code
        self.dealer_code = dealer_code
        self.order_code = order_code
        self.customer_code = customer_code
        self.OTD = OTD
        self.priority = priority
        self.VIN = VIN
        self.start_loc = start_loc
        self.end_city = end_city
        self.end_loc = end_loc
        self.effective_time = effective_time
        self.car_type = car_type
        self.transport_type = transport_type
        self.time_line = pd.DataFrame({},[], [])

    def add_time_line(self, time_str, effective_time_t, priority_t):
        temp_index = [self.time_line.index[j] for j in range(0, len(self.time_line.index))]
        temp_index.append(time_str)
        temp_df = pd.DataFrame({}, temp_index, columns=['effective time', 'priority'])
        temp_loc = len(self.time_line.index)
        for i in range(0, temp_loc):
            temp_df.loc[i] = self.time_line.loc[i]
        temp_df.loc[time_str] = [effective_time_t, priority_t]
        self.time_line = temp_df
        return True

    def change_time_line(self, time_str, effective_time_t, priority_t):
        self.time_line.loc[time_str] = [effective_time_t, priority_t]
        return True
    
# Carriers: Edited by Bohao
## Trailers
class trailer:
    def __init__(self, code, supplier_code, capacity_all, capacity_for_xl_car, capacity_for_l_car, capacity_for_m_car, capacity_for_s_car,
                 capacity_for_xs_car, reported_package_type, history_package_type, preferred_direction, availability, trailer_available_time,
                 shipments_set, loading_time, planed_start_time, planed_arrive_time, actual_start_time, actual_arrive_time, start_location,
                 current_location, destination, historic_trajectory=None):
        self.code = code
        self.supplier_code = supplier_code
        self.capacity_all = capacity_all
        self.capacity_for_xl_car = capacity_for_xl_car
        self.capacity_for_l_car = capacity_for_l_car
        self.capacity_for_m_car = capacity_for_m_car
        self.capacity_for_s_car = capacity_for_s_car
        self.capacity_for_xs_car = capacity_for_xs_car
        self.reported_package_type = reported_package_type
        self.history_package_type = history_package_type
        self.preferred_direction = preferred_direction
        self.availability = availability
        self.trailer_available_time = trailer_available_time

        ## assigned
        self.shipments_set = shipments_set 
        self.loading_time = loading_time 
        self.planed_start_time = planed_start_time
        self.planed_arrive_time = planed_arrive_time
        self.actual_start_time = actual_start_time
        self.actual_arrive_time = actual_arrive_time
        self.start_location = start_location
        self.current_location = current_location
        self.destination = destination
        self.historic_trajectory = historic_trajectory
        self.time_line = pd.DataFrame({}, [], [])

    def add_time_line(self, time_str, shipments_set_t, loading_time_t, planed_start_time_t, planed_arrive_time_t,actual_start_time_t, actual_arrive_time_t, start_location_t, current_location_t, destination_t):
        temp_index = [self.time_line.index[j] for j in range(0, len(self.time_line.index))]
        temp_index.append(time_str)
        temp_df = pd.DataFrame({}, temp_index, columns=['shipments_set', 'loading_time', 'planed_start_time', 'planed_arrive_time','actual_start_time', 'actual_arrive_time', 'start_location', 'destination', 'destination'])
        temp_loc = len(self.time_line.index)
        for i in range(0, temp_loc):
            temp_df.loc[i] = self.time_line.loc[i]
        temp_df.loc[time_str] = [shipments_set_t, loading_time_t, planed_start_time_t, planed_arrive_time_t,actual_start_time_t, actual_arrive_time_t, start_location_t, current_location_t, destination_t]
        self.time_line = temp_df
        return True

    def change_time_line(self, time_str, shipments_set_t, loading_time_t, planed_start_time_t, planed_arrive_time_t,actual_start_time_t, actual_arrive_time_t, start_location_t, current_location_t, destination_t):
        self.time_line.loc[time_str] = [shipments_set_t, loading_time_t, planed_start_time_t, planed_arrive_time_t,actual_start_time_t, actual_arrive_time_t, start_location_t, current_location_t, destination_t]
        return True
    
## Train
class train:
    def __init__(self, code, capacity_for_big_car, capacity_for_small_car, start_station, end_station,
                 time_table, shipments_set, planed_start_time, planed_arrive_time, actual_start_time,
                 actual_arrive_time, current_location=None):

        ## Self
        self.code = code
        self.capacity_for_big_car = capacity_for_big_car
        self.capacity_for_small_car = capacity_for_small_car
        self.start_station = start_station
        self.end_station = end_station
        self.time_table = time_table

        ## assigned
        self.shipments_set = shipments_set
        self.planed_start_time = planed_start_time
        self.planed_arrive_time = planed_arrive_time
        self.actual_start_time = actual_start_time
        self.actual_arrive_time = actual_arrive_time
        self.current_location = current_location


## ship
class ship:
    def __init__(self, code, max_capacity, min_capacity, start_station, end_station,
                 time_table, stops, shipments_set, planed_start_time, planed_arrive_time,
                 actual_start_time, actual_arrive_time, current_location=None):

        ## self
        self.code = code
        self.max_capacity = max_capacity
        self.min_capacity = min_capacity
        self.start_station = start_station
        self.end_station = end_station
        self.time_table = time_table
        self.stops = stops

        ## assigned
        self.shipments_set = shipments_set
        self.planed_start_time = planed_start_time
        self.planed_arrive_time = planed_arrive_time
        self.actual_start_time = actual_start_time
        self.actual_arrive_time = actual_arrive_time
        self.current_location = current_location


## scheduling command
class scheduling_command:
    def __init__(self, SD, customer, start_warehouse, arrive_warehouse, used_trailers, lane, clearing_corp,
                 loading_time, loading_number, create_time, operator, orders=None):
        self.SD = SD
        self.customer = customer
        self.start_warehouse = start_warehouse
        self.arrive_warehouse = arrive_warehouse
        self.used_trailers = used_trailers
        self.lane = lane
        self.clearing_corp = clearing_corp
        self.loading_time = loading_time
        self.loading_number = loading_number
        self.create_time = create_time
        self.operator = operator
        self.orders = orders


# Stations : Edited by Mazhe
class station:
    def __init__(self, station_code, capacity, free_period, location, load_time):
        self.code = station_code
        self.capacity = capacity
        self.free_period = free_period
        self.location = location
        self.load_time = load_time


class warehouse:
    def __init__(self, warehouse_code, location, priority, type,
                 dispatch_ability, capacity, time_start,
                 time_end, sub, lane_number, locked_lanes, lane_number_available, cost):
        self.code = warehouse_code
        self.location = location
        self.priority = priority
        self.type = type
        self.dispatch_ability = dispatch_ability
        self.capacity = capacity
        self.time_start = time_start
        self.time_end = time_end
        self.sub = sub
        self.lane_number = lane_number
        self.locked_lanes = locked_lanes
        self.lane_number_available = lane_number_available
        self.cost = cost
        self.time_line = pd.DataFrame({},[],[])

    def add_time_line(self, time_str, locked_lanes_t, lane_number_available_t):
        temp_index = [self.time_line.index[j] for j in range(0, len(self.time_line.index))]
        temp_index.append(time_str)
        temp_df = pd.DataFrame({}, temp_index, columns=['locked_lanes', 'lane_number_available'])
        temp_loc = len(self.time_line.index)
        for i in range(0, temp_loc):
            temp_df.loc[i] = self.time_line.loc[i]
        temp_df.loc[time_str] = [locked_lanes_t, lane_number_available_t]
        self.time_line = temp_df
        return True
    
    def change_time_line(self, time_str, locked_lanes_t, lane_number_available_t):
        self.time_line.loc[time_str] = [locked_lanes_t, lane_number_available_t]
        return True

class wharf:
    def __init__(self, wharf_code, capacity, time_start, time_end,
                 free_period, location, load_time):
        self.code = wharf_code
        self.capacity = capacity
        self.time_start = time_start
        self.time_end = time_end
        self.free_period = free_period
        self.location = location
        self.load_time = load_time


class dealer:
    def __init__(self, dealer_code, location, order_freq, add):
        self.code = dealer_code
        self.location = location
        self.order_freq = order_freq #下单频率
        self.add = add

# Edited by Wenbo
class supplier:
    def __init__(self, supplier_code, trailer_set, trailer_available):
        self.code = supplier_code
        self.trailer_set = trailer_set
        self.trailer_available = trailer_available
        self.time_line = pd.DataFrame({}, [], [])

    def add_time_line(self, time_str, trailer_available_t):
        temp_index = [self.time_line.index[j] for j in range(0, len(self.time_line.index))]
        temp_index.append(time_str)
        temp_df = pd.DataFrame({}, temp_index, columns=['trailer_available'])
        temp_loc = len(self.time_line.index)
        for i in range(0, temp_loc):
            temp_df.loc[i] = self.time_line.loc[i]
        temp_df.loc[time_str] = [trailer_available_t]
        self.time_line = temp_df
        return True
        
    def change_time_line(self, time_str, trailer_available_t):
        self.time_line.loc[time_str] = [trailer_available_t]
        return True
    

class route:
    def __init__(self, route_code, start, end, dist, duration, price, supplier_code):
        self.code = route_code
        self.start = start
        self.end = end
        self.dist = dist
        self.duration = duration
        self.price = price
        self.supplier = supplier_code

class car:
    def __init__(self, car_code, type, shipment_code):
        self.code = car_code
        self.type = type
        self.shipment_code = shipment_code  ##############

class customer:
    def __init__(self, customer_code):
        self.code = customer_code
