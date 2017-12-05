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
from app import celery #for transporting parameters
import json
import requests
import logging
import bayes_pareto


weight = [0.0, 0.5, 0.0, 0.5]

# ---------------------------To carry out optimization and record results in result_record.pkl--------------------------#
@celery.task(serializer='pickle')
def optimization(data):
    #----------------- To generate scheduling solutions through hierarchical mult-object optimization--------------
    logger = logging.getLogger(__name__)

    retval = {"taskId": optimization.request.id,
              "trailerOrders": []}
    headers = {'content-type': 'application/json'}
    try:
        logger.info("The algorithm starts")
        #has_solution, matrix, route = main.ga_vrp(data, weight, 5, 0.0001)

        has_solution,solution,length=bayes_pareto.run(data)

    except ValueError:
        logger.error("Ineffective input data!")
        print("report result")
        url = "http://192.168.204.169:28109/ids/engine/dealPlan"
        url = "http://10.108.11.50:28060/ids/engine/dealPlan"
        r = requests.post(url=url, data=json.dumps(retval), headers=headers)
        print 'Ineffective input data!'
        return 0

    if not has_solution:
        logger.info("empty solution")
        #url="http://192.168.204.169:28109/ids/engine/dealPlan"
        url="http://10.108.11.50:28060/ids/engine/dealPlan"
        r = requests.post(url=url, data=json.dumps(retval),headers=headers)
        print 'empty solution'
        return 0

    #solution, length = xmatrix_to_solution(matrix, route)
    print solution

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

    #retval={"taskId":optimization.request.id,
    #        "trailerOrders":[]}
    for index, row_data in solution.iterrows():
        row={}
        row["code"]=index
        row["sequenceCitys"]=[]
        a=row_data.iloc[0:length]
        row["sequenceCitys"]=a[a!=0].tolist()
        b=row_data.iloc[length:]
        row["orderCodes"]=b[b!=-1].tolist()
        retval["trailerOrders"].append(row)

    #headers = {'content-type': 'application/json'}
    url = "http://10.108.11.50:28060/ids/engine/dealPlan"
    #url="http://192.168.204.103:28109/ids/engine/dealPlan"
    r = requests.post(url=url, data=json.dumps(retval),
                      headers=headers)
    print(r.text)
    print "GoneTrailer: ",solution.shape[0]
    return 0

