# -*- coding:utf-8 -*-
"""
Find the shortest route with DP
2017.10.11
"""

from __future__ import division, print_function, absolute_import
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

__all__ = 'find_path_DP'


def find_path_DP(city_coord):
    """
    find the shortest route with DP
    :param city_coord: the coord of cities
    :return: the route and the distance between cities
    """
    n_city = len(city_coord)
    dist_mat = euclidean_distances(city_coord)
    dist_mat = dist_mat - np.diag(np.diag(dist_mat)+1)

    # initialize the dp_table
    dp_table = np.zeros([n_city, 1 << (n_city - 1)])
    route_table = np.zeros([n_city, 1 << (n_city - 1)], dtype=int) - 1

    for j_col in range(1, 1 << (n_city - 1)):
        for i_row in range(n_city):
            dp_table[i_row, j_col] = 0x7ffff
            if i_row > 0:
                # if {b} is in S ={a,b,c}, we have already visit {b}; i.e., no repeated path
                if (j_col >> (i_row - 1)) & 1:
                    continue

            # find the optimal action with dp(i, V) = min(cik + dp(k, V-{k}))
            for k_row in range(1, n_city):
                # if {b} is not in S = {a}, we can't select {b} from S
                if not (j_col >> (k_row - 1)) & 1:
                    continue

                # xor: j_col^(1 << (k_row - 1)), {a,b,c}^{a} = {b,c}
                if dp_table[i_row, j_col] > dist_mat[i_row, k_row] + dp_table[k_row, j_col ^ (1 << (k_row - 1))]:
                    # save the optimal value with smaller distance
                    dp_table[i_row, j_col] = dist_mat[i_row, k_row] + dp_table[k_row, j_col ^ (1 << (k_row - 1))]
                    # save the optimal action
                    route_table[i_row, j_col] = k_row

    route_dist = []     # [route, dist]
    i_ind = (1 << (n_city - 1))-1
    j_ind = 0       # show the route index
    while i_ind > 0:
        j_ind_ = route_table[j_ind, i_ind]
        i_ind = i_ind - (1 << (j_ind_ - 1))
        route_dist.append(list((j_ind_, dist_mat[j_ind, j_ind_])))
        j_ind = j_ind_

    return route_dist
