#coding=utf-8
from KDTree import KDTree, to_Cartesian
from DP_TSP import find_path_DP
import pandas as pd

# ---------------------------------------------the route and the loading rate----------------------------------#
def average_loading_rate(Warehouse, Retailers, n_capacity):
    """
    :param Warehouse: the start_warehouse with DF[start_warehouse_id, start_warehouse_name,LATITUDE,LONGITUDE]
    :param Retailers: the Retailers_AB with DF[ID, ADDRESS, LATITUDE, LONGITUDE, num_orders]
    :param n_capacity: the maximum number of cars on the truck, i.e., capacity
    :return: avg_loading_rate in (0,1)
    """
    StWarehouse = Warehouse.copy()
    StWarehouse['x'], StWarehouse['y'], StWarehouse['z'] = list(to_Cartesian(StWarehouse['LATITUDE'],
                                                                             StWarehouse['LONGITUDE']))
    Retailers_AB = Retailers.copy()
    Retailers_AB['x'], Retailers_AB['y'], Retailers_AB['z'] = zip(*map(to_Cartesian, Retailers_AB['LATITUDE'],
                                                                       Retailers_AB['LONGITUDE']))
    route_AB = pd.DataFrame(find_the_path(StWarehouse, Retailers_AB), columns=['CODE', 'dist', 'num_order'])
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
    start_node = list((StWarehouse['x'], StWarehouse['y'], StWarehouse['z'], StWarehouse['ID'], 0))
    end_nodes = list(zip(Retailers_AB['x'], Retailers_AB['y'], Retailers_AB['z'], Retailers_AB['ID'],
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
    k_nn = k_nn
    leaf_size = leaf_size
    now_retailer_gps = retailer_info

    if isinstance(now_retailer_gps, pd.DataFrame):
        pass
    else:
        raise Exception("inpute data is not DataFrame")
    now_retailer_gps.reset_index(drop=True)

    now_retailer_gps['x'], now_retailer_gps['y'], now_retailer_gps['z'] = zip(
        *map(to_Cartesian, now_retailer_gps['end_loc_latitude'],
             now_retailer_gps['end_loc_longitude']))
    now_retailer_xyz = list(zip(now_retailer_gps['x'], now_retailer_gps['y'], now_retailer_gps['z']))

    RetlTree = KDTree(now_retailer_xyz, leafsize=leaf_size)
    dist_k, ind_k = RetlTree.query(now_retailer_xyz, k=k_nn + 1)
    B_retailer_list = now_retailer_gps.iloc[ind_k[:, 1:].flatten(), :]
    # B_retailer_dist = now_retailer_gps.iloc[dist_k[:, 1:].flatten(), :]

    retailerAB_IDlist = pd.DataFrame(
        data=B_retailer_list['dealer_code'].values.reshape([len(now_retailer_gps), k_nn]),
        index=now_retailer_gps.dealer_code)
    # 需求不明，距离不知何时返回
    retailerAB_dist = pd.DataFrame(data=dist_k, index=now_retailer_gps.dealer_code).drop(0, 1)

    return retailerAB_IDlist

def load_rate(load_info, order_info):   #字段严重不符合？？？？？
    # 输入的订单信息为字典组成的list
    item = list(order_info.values())[0]
    id = [item['SRC_WH_ID']]
    name = [item['SRC_WH_NAME']]
    address = [item['SRC_WH_ADDRESS']]
    SRC_WH_LATITUDE = [item['SRC_WH_LATITUDE']]
    SRC_WH_LONGITUDE = [item['SRC_WH_LONGITUDE']]
    test_StWarehouse = pd.DataFrame()
    test_StWarehouse['ID'] = id
    test_StWarehouse['NAME'] = name
    test_StWarehouse['ADDRESS'] = address
    test_StWarehouse['LATITUDE'] = SRC_WH_LATITUDE
    test_StWarehouse['LONGITUDE'] = SRC_WH_LONGITUDE
    #
    load_order = [order_info[item] for item in list(load_info.values())[0]]
    ID,ADDRESS,LATITUDE,LONGITUDE = [],[],[],[]
    for item in load_order:
        ID.append(item['RETAILER_ID'])
        ADDRESS.append(item['PURCHASER_ADDRESS'])
        LATITUDE.append(item['LATITUDE'])
        LONGITUDE.append(item['LONGITUDE'])
    test_Retailers_order = pd.DataFrame()
    test_Retailers_order['ID'] = ID
    test_Retailers_order['ADDRESS'] = ADDRESS
    test_Retailers_order['LATITUDE'] = LATITUDE
    test_Retailers_order['LONGITUDE'] = LONGITUDE
    count_order_dict = test_Retailers_order['ID'].groupby(test_Retailers_order['ID']).count()
    #print(count_order_dict)
    test_Retailers_order.drop_duplicates(['ID'], inplace=True)
    #print(test_Retailers_order.index)
    count_order_list = [count_order_dict[item] for item in test_Retailers_order['ID']]
    test_Retailers_order['num_order'] = count_order_list
    # the route and their averaged loading rate
    n_capacity = test_Retailers_order['num_order'].sum()  # just the sum of the orders//should be the real capacity
    test_route, test_loading_rate = average_loading_rate(test_StWarehouse, test_Retailers_order, n_capacity)
    return test_route, test_loading_rate

