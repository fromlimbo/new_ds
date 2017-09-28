# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from io import StringIO
import csv
import json
import logging
from basic_class import *
from datetime import datetime

def GAVRP_Validation(request):
    print "validating"
    return True

def  GAVARP_Process_json(jsondemo):
    var_dict = {}
    #order_example_json 值为-1，该变量可为空
    order_example_json = """[{"order_code":"order",
                   "customer_code":"",
                   "dealer_code":"",
                    "OTD":"",
                    "priority":"",
                    "VIN":-1,
                    "shipment_code_set":-1,
                    "start_loc":"",
                    "end_city":"",
                    "end_loc":"",
                    "created_time":-1,
                    "effective_time":1,
                    "car_type":1,
                    "transport_type":-1
    }]"""

    try:
        orderjosn = json.loads(order_example_json)
    except Exception:
        logging.debug("json type is error")
        return -1
    else:
        order_dict = {
            data["order_code"]:order(data["order_code"],data["customer_code"],data["dealer_code"],
                                      data["OTD"],data["priority"],data["VIN"],
                                     data["shipment_code_set"],data["start_loc"],data["end_city"],
                                     data["end_loc"],data["created_time"],data["effective_time"],
                                     data["car_type"],data["transport_type"]) for data in orderjosn
    }
        var_dict["order_dict"] = order_dict

    #trailer_example_json  值为-1，该变量可为空
    trailer_example_json = """[{"code":"",
                            "supplier_code": -1,
                            "capacity_all": "",
                            "capacity_for_xl_car": "",
                            "capacity_for_l_car":"",
                            "capacity_for_m_car": "",
                            "capacity_for_s_car": "",
                            "capacity_for_xs_car": "",
                            "reported_package_type": -1,
                            "history_package_type":-1,
                            "preferred_direction":"",
                            "availability": "",
                            "trailer_available_time":"",
                            "shipments_set":-1,
                            "loading_time": -1,
                            "planed_start_time": -1,
                            "planed_arrive_time":-1,
                            "actual_start_time": -1,
                            "actual_arrive_time": -1,
                            "start_location": "",
                            "current_location": "",
                            "destination":"",
                            "historic_trajectory": ""
    }]"""
    try:
        trailerjson=json.loads(trailer_example_json)
    except Exception:
        logging.debug("json type is error")
        return -1
    else:
        trailer_dict = {
            data["code"]:order(data["code"],data["supplier_code"],data["capacity_all"],
                           data["capacity_for_xl_car"],data["capacity_for_l_car"],data["capacity_for_m_car"],
                           data["capacity_for_s_car"],data["capacity_for_xs_car"],data["reported_package_type"],
                           data["history_package_type"],data["preferred_direction"],data["availability"],
                           data["trailer_available_time"],data["shipments_set"],data["loading_time"],
                           data["planed_start_time"], data["planed_arrive_time"], data["actual_start_time"],
                           data["actual_arrive_time"], data["start_location"], data["current_location"],
                           data["destination"], data["historic_trajectory"]) for data in trailerjson
        }
        var_dict["trailer_dict"] = trailer_dict
    print "hello worldqqqqqqq"
    return var_dict


def GAVRP_Process(request):
    if not GAVRP_Validation(request):
        return "Not Valid"
    print "data processing"
    var_dict = {}
    today = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').date()
    order_tmpFile = request.form.get("order_raw")
    strIo = StringIO(order_tmpFile)

    input_file = csv.reader(strIo)

    order_dict = {
    i[0]: order(str(i[0]), int(i[1]), int(i[4]), (today - datetime.strptime(i[11], '%Y-%m-%d %H:%M:%S').date()).days,
                int(i[12]), -1,
                -1, int(i[3]), int(i[7]), int(i[6]), -1, datetime.strptime(i[11], '%Y-%m-%d %H:%M:%S').date(), i[14],
                -1) for i in input_file}
    var_dict['order_dict']=order_dict

    trailer_tmpFile = request.form.get("trailer_raw_truck")
    strIo = StringIO(trailer_tmpFile)
    input_file = csv.reader(strIo)
    trailer_dict = {
    str(i[15]): trailer(str(i[15].strip()), -1, int(i[7]), int(i[9]), int(i[10]), int(i[11]), int(i[12]), int(i[13]),
                        -1, -1, (map(int, ((i[6] + '、' + i[19]).split('、')))), 1,
                        datetime.strptime('2015-06-1', '%Y-%m-%d').date(), -1, -1, -1, -1, -1, -1, int(i[0]), -1, -1,
                        -1)for i in input_file}
    var_dict['trailer_dict'] = trailer_dict

    mixCity_tmpFile = request.form.get("mix_city")
    strIo = StringIO(mixCity_tmpFile)
    mix_city = pd.read_csv(strIo)
    var_dict['mix_city'] = mix_city

    OTD_pinche_tmpFile = request.form.get("OTD_pinche")
    strIo = StringIO(OTD_pinche_tmpFile)
    OTD_pinche = pd.read_csv(strIo)
    var_dict['OTD_pinche'] = OTD_pinche

    # for key in request.form.keys():
    #     tmpFile = request.form.get(key)
    #     strIo = StringIO(tmpFile)
    #     df = pd.read_csv(strIo, header=None)
    #     input_dict[key] = df
    # print var_dict

    return var_dict


'''
sample_json={'mix_city':[{'CenterCityId':..,
                          'OtherCityId':...},
                          ...]
}
'''

def data_processing_json(input_json=None):
    mix_city= pd.read_json(input_json['mix_city'])
    OTD_pinche = pd.read_json(input_json['OTD_pinche'])


if __name__ == "__main__":
    GAVARP_Process_json(None)
