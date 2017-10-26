# coding:utf-8
########################################################################################################################
"""
To set related parameters and start GA based dynamic scheduling by Zhe Ma.

There is no input parameters which need to be adjusted by the scheduling starf.

Input: the data needed in this algorithm is loaded in the packaging.py file.

Output: the output of this program, solution, is printed in the end of the code.
"""
########################################################################################################################
import main
from packaging import *
from main import *
from app import celery#for transporting parameters
import pickle
import json
import requests

weight = [0.0, 0.5, 0.0, 0.5]

# ---------------------------To carry out optimization and record results in result_record.pkl--------------------------#
@celery.task(serializer='pickle')
def optimization(data):
    #----------------- To generate scheduling solutions through hierarchical mult-object optimization--------------

    retval = {"taskId": optimization.request.id,
              "trailerOrders": []}
    headers = {'content-type': 'application/json'}
    try:
        logging.info("The algorithm starts")
        ind1 = main.ga_vrp(data, weight, 5, 0.0001)
    except ValueError:
        print "Ineffective input data!"
        logging.error("Ineffective input data!")
    #solution = xmatrix_to_solution(convert_ind_to_matrix(ind1))

    flag, matrix, route = convert_ind_to_matrix(ind1)
    if not flag:
        print("report result")
        r = requests.post("http://192.168.204.169:28109/ids/engine/dealPlan", data=json.dumps(retval),
                          headers=headers)
        print r
        print 'empty plan'
        return 0
    solution = xmatrix_to_solution(matrix, route)
    # print solution

    # TODO:
    # {
    #     "taskId": "fewewewerwr32",
    #     "trailerOrders":
    #         [
    #             {"code": "板车code1",
    #              "orderCoes": ["订单code1-1", "订单code1-2"],
    #              "sequenceCitys": ["城市code1", "城市code2"]
    #              },
    #             {"code": "板车code2",
    #              "orderCoes": ["订单code2-1", "订单code2-2"],
    #              "sequenceCitys": ["城市code3", "城市code4"]
    #              }
    #         ]
    # }

    retval={"taskId":optimization.request.id,
            "trailerOrders":[]}
    for index, row_data in solution.iterrows():
        row={}
        row["code"]=index
        row["sequenceCitys"]=[]
        if not row_data['city1']==0:
            row["sequenceCitys"].append(row_data['city1'])
        if not row_data['city2']==0:
            row["sequenceCitys"].append(row_data['city2'])
        a=row_data.iloc[2:-1]
        row["orderCodes"]=a[a!="-1"].tolist()

        retval["trailerOrders"].append(row)

    headers = {'content-type': 'application/json'}
    r = requests.post("http://192.168.204.169:28109/ids/engine/dealPlan", data=json.dumps(retval),
                      headers=headers)
    print r.text
    return 0

