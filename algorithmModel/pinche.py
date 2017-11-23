# -*- coding:utf-8 -*-
from KDTree import KDTree, to_Cartesian
from DP_TSP import find_path_DP
import pandas as pd
import copy

# ---------------------------------------------the route and the loading rate----------------------------------#
def average_loading_rate(Warehouse, Retailers, n_capacity):
    """
    :param Warehouse: the start_warehouse with DF[start_warehouse_id, start_warehouse_name,LATITUDE,LONGITUDE]
    :param Retailers: the Retailers_AB with DF[ID, ADDRESS, LATITUDE, LONGITUDE, num_orders]
    :param n_capacity: the maximum number of cars on the truck, i.e., capacity
    :return: avg_loading_rate in (0,1)
    """
    StWarehouse = Warehouse.copy()
    StWarehouse['x'], StWarehouse['y'], StWarehouse['z'] = list(to_Cartesian(StWarehouse['start_loc_latitude'],
                                                                             StWarehouse['start_loc_longitude']))
    Retailers_AB = Retailers.copy()
    Retailers_AB['x'], Retailers_AB['y'], Retailers_AB['z'] = zip(*map(to_Cartesian, Retailers_AB['end_loc_latitude'],
                                                                       Retailers_AB['end_loc_longitude']))
    route_AB = pd.DataFrame(find_the_path(StWarehouse, Retailers_AB), columns=['dealer_code', 'dist', 'num_order'])
    dist_cusum = route_AB['dist'].cumsum().values
    num_f = (dist_cusum * route_AB['num_order'].values).sum()
    den_f = dist_cusum[-1]
    avg_loading_rate = num_f / den_f / n_capacity

    return route_AB, avg_loading_rate


# the route from S to {A, B} cities
def find_the_path(StWarehouse, Retailers_AB):
    """
    find the shortest route with DP
    :param StWarehouse: the start_warehouse with DF[start_warehouse_id, start_warehouse_name,LATITUDE,LONGITUDE, x,y,z]
    :param Retailers_AB: the Retailers_AB with DF[ID, ADDRESS, LATITUDE, LONGITUDE,x,y,z]
    :return: the route and their distances between each two cities
    """
    # change to the array and cartesian format
    start_node = list((StWarehouse['x'], StWarehouse['y'], StWarehouse['z'], StWarehouse['start_loc'], 0))
    end_nodes = list(zip(Retailers_AB['x'], Retailers_AB['y'], Retailers_AB['z'], Retailers_AB['dealer_code'],
                         Retailers_AB['num_order']))
    end_nodes.insert(0, start_node)
    nodes = end_nodes

    nodes_list = []  # only the coord
    for item in nodes:
        nodes_list.append(list((item[0], item[1], item[2])))

    # return the route and the dist with DP
    route_dist = find_path_DP(nodes_list)

    # add the order
    route_dist_order = []
    for item in route_dist:
        route_dist_order.append(list((nodes[item[0]][3], item[1], nodes[item[0]][4])))

    return route_dist_order



def find_nearest_id(retailer_info, k_nn=12, leaf_size=10):
    k_nn = min(k_nn, len(retailer_info)-1)
    leaf_size = leaf_size
    now_retailer_gps = copy.deepcopy(retailer_info)

    if isinstance(now_retailer_gps, pd.DataFrame):
        pass
    else:
        raise Exception("传入数据格式不是DataFrame")

    now_retailer_gps = now_retailer_gps.reset_index(drop=True)

    now_retailer_gps['x'], now_retailer_gps['y'], now_retailer_gps['z'] = zip(
        *map(to_Cartesian, now_retailer_gps['end_loc_latitude'],
             now_retailer_gps['end_loc_longitude']))
    now_retailer_xyz = list(zip(now_retailer_gps['x'], now_retailer_gps['y'], now_retailer_gps['z']))

    RetlTree = KDTree(now_retailer_xyz, leafsize=leaf_size)
    dist_k, ind_k = RetlTree.query(now_retailer_xyz, k=k_nn + 1)
    # B_retailer_list = now_retailer_gps.iloc[ind_k[:, 1:].flatten(), :]
    # B_retailer_dist = now_retailer_gps.iloc[dist_k[:, 1:].flatten(), :]
    pinche_retailer = []
    for i in now_retailer_gps.index:
        temp = []
        start_dealer = now_retailer_gps.loc[i,'dealer_code']
        temp.append(start_dealer)
        for j in range(1,k_nn+1):
            if dist_k[i,j]>625:
                temp.append(None)
            else:
                temp.append(now_retailer_gps.loc[ind_k[i,j],'dealer_code'])
        pinche_retailer.append(temp)

    retailerAB_IDlist = pd.DataFrame(data=pinche_retailer)
    # 需求不明，距离不知何时返回
    # retailerAB_dist = pd.DataFrame(data=dist_k, index=now_retailer_gps.dealer_code).drop(0, 1)
    # return retailerAB_IDlist.reset_index()

    return retailerAB_IDlist




def trailer_route(load_info, order_info):
    load_rate_route = pd.DataFrame()
    trailer_list = []
    route_list = []
    # load_rate_list = []
    # produce the dealer_code:end_loc pair
    dealer_code_loc = {}
    for item in order_info.values():
        dealer_code_loc[item.dealer_str] = item.end_loc
    for trailer_code, order_id in load_info.items():
        assert len(order_id) > 0
        item = order_info[order_id[0]]
        id = item.start_loc
        SRC_WH_LATITUDE = item.start_loc_latitude
        SRC_WH_LONGITUDE = item.start_loc_longitude
        test_StWarehouse = pd.DataFrame()
        test_StWarehouse['start_loc'] = [id]
        test_StWarehouse['start_loc_latitude'] = [SRC_WH_LATITUDE]
        test_StWarehouse['start_loc_longitude'] = [SRC_WH_LONGITUDE]
        #
        load_order = [order_info[item] for item in order_id]
        dealer_code, LATITUDE, LONGITUDE = [], [], []
        for item in load_order:
            dealer_code.append(item.dealer_str)
            # ADDRESS.append(item['PURCHASER_ADDRESS'])
            LATITUDE.append(item.end_loc_latitude)
            LONGITUDE.append(item.end_loc_longitude)
        test_Retailers_order = pd.DataFrame()
        test_Retailers_order['dealer_code'] = dealer_code
        # test_Retailers_order['ADDRESS'] = ADDRESS
        test_Retailers_order['end_loc_latitude'] = LATITUDE
        test_Retailers_order['end_loc_longitude'] = LONGITUDE
        count_order_dict = test_Retailers_order['dealer_code'].groupby(test_Retailers_order['dealer_code']).count()
        test_Retailers_order.drop_duplicates(['dealer_code'], inplace=True)
        count_order_list = [count_order_dict[item] for item in test_Retailers_order['dealer_code']]
        test_Retailers_order['num_order'] = count_order_list
        # the route and their averaged loading rate
        n_capacity = test_Retailers_order['num_order'].sum()  # just the sum of the orders//should be the real capacity
        test_route, test_loading_rate = average_loading_rate(test_StWarehouse, test_Retailers_order, n_capacity)

        trailer_list.append(trailer_code)
        route = [dealer_code_loc[x] for x in list(test_route['dealer_code'])]
        # drop duplicates
        temp = []
        for item in route:
            if item not in temp:
                temp.append(item)
        route = temp
        route_list.append(route)
        #load_rate_list.append(test_loading_rate)
    # load_rate_path['load_rate'] = load_rate_list

    max_len=max(len(i) for i in route_list)
    route_index = ['route'+ str(i+1) for i in xrange(max_len)]
    route_temp_list=[]
    for i in route_list:
        route_temp_list.append(i+[0]*(max_len-len(i)))

    load_rate_route=pd.DataFrame(route_temp_list, index=trailer_list, columns=route_index)
    return load_rate_route


def load_rate(load_info, order_info):
    load_rate_path = pd.DataFrame()
    #trailer_list = []
    load_rate_list = []
    for trailer_code, order_id in load_info.items():
        assert len(order_id)>0
        item = order_info[order_id[0]]
        id = item.start_loc
        SRC_WH_LATITUDE = item.start_loc_latitude
        SRC_WH_LONGITUDE = item.start_loc_longitude
        test_StWarehouse = pd.DataFrame()
        test_StWarehouse['start_loc'] = [id]
        test_StWarehouse['start_loc_latitude'] = [SRC_WH_LATITUDE]
        test_StWarehouse['start_loc_longitude'] = [SRC_WH_LONGITUDE]
        #
        load_order = [order_info[item] for item in order_id]
        dealer_code,LATITUDE,LONGITUDE = [], [], []
        for item in load_order:
            dealer_code.append(item.dealer_str)
            #ADDRESS.append(item['PURCHASER_ADDRESS'])
            LATITUDE.append(item.end_loc_latitude)
            LONGITUDE.append(item.end_loc_longitude)
        test_Retailers_order = pd.DataFrame()
        test_Retailers_order['dealer_code'] = dealer_code
        #test_Retailers_order['ADDRESS'] = ADDRESS
        test_Retailers_order['end_loc_latitude'] = LATITUDE
        test_Retailers_order['end_loc_longitude'] = LONGITUDE
        count_order_dict = test_Retailers_order['dealer_code'].groupby(test_Retailers_order['dealer_code']).count()
        test_Retailers_order.drop_duplicates(['dealer_code'], inplace=True)
        count_order_list = [count_order_dict[item] for item in test_Retailers_order['dealer_code']]
        test_Retailers_order['num_order'] = count_order_list
        # the route and their averaged loading rate
        n_capacity = test_Retailers_order['num_order'].sum()  # just the sum of the orders//should be the real capacity
        test_route, test_loading_rate = average_loading_rate(test_StWarehouse, test_Retailers_order, n_capacity)

        #trailer_list.append(trailer_code)

        load_rate_list.append(test_loading_rate)
    #load_rate_path['code'] = trailer_list
    #load_rate_path['path'] = path_list
    #load_rate_path['load_rate'] = load_rate_list

    return load_rate_list

