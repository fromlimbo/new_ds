# -*- coding: utf-8 -*-
from io import StringIO
import csv
import json
import logging
from basic_class import *
from datetime import datetime


def GAVRP_Validation(request):
    print "validating"
    return True


def GAVARP_Process_json(input_json):
    """
    这是一个注释
    """
    var_dict = {}
    required_order_keys = ['order_code', 'customer_code', 'dealer_code',
                           'OTD', 'priority', 'start_loc', 'end_loc', 'car_type', 'effective_time']

    # key: default value
    optional_order_keys = {'VIN': -1,
                           'shipment_code_set': -1,
                           'created_time': -1,
                           'transport_type': -1
                           }

    try:
        orderjson = json.loads(input_json['order'])
    except Exception:
        logging.debug("json type is error")
        return -1

    order_dict = {}
    for item in orderjson:
        for k in required_order_keys:
            if not item.has_key(k):
                logging.debug('lost required keys.')
                return -1
        for k in optional_order_keys.keys():
            if not item.has_key(k):
                item[k] = optional_order_keys[k]

        item['effective_time'] = datetime.strptime(item['effective_time'], '%Y-%m-%d %H:%M:%S').date()
        order_dict[item["order_code"]] = order(item["order_code"], item["customer_code"], item["dealer_code"],
                                               item["OTD"], item["priority"], item["VIN"],
                                               item["shipment_code_set"], item["start_loc"], item["end_city"],
                                               item["end_loc"], item["created_time"], item["effective_time"],
                                               item["car_type"], item["transport_type"])
    var_dict["order_dict"] = order_dict

    required_trailer_keys = ['code', 'capacity_all', 'capacity_for_xl_car',
                             'capacity_for_l_car', 'capacity_for_m_car',
                             'capacity_for_s_car', 'capacity_for_xs_car',
                             'preferred_direction', 'availability',
                             'trailer_available_time', 'start_location']

    # key: default value
    optional_trailer_keys = {'supplier_code': -1,
                             'reported_package_type': -1,
                             'history_package_type': -1,
                             'shipments_set': -1,
                             'loading_time': -1,
                             'planed_start_time': -1,
                             'planed_arrive_time': -1,
                             'actual_start_time': -1,
                             'actual_arrive_time': -1,
                             'current_location': -1,
                             'destination': -1,
                             'historic_trajectory': -1}

    try:
        trailerjson = json.loads(input_json['trailer'])
    except Exception:
        logging.debug("json type is error")
        return -1
    trailer_dict = {}
    for item in trailerjson:

        # check required keys
        for k in required_trailer_keys:
            if not item.has_key(k):
                logging.warning('lost required trailer keys.')
                return -1

        for k in optional_trailer_keys.keys():
            if not item.has_key(k):
                item[k] = optional_trailer_keys[k]
        item['preferred_direction'] = (map(int, (item['preferred_direction'].split('、'))))
        trailer_dict[item["code"]] = trailer(item["code"], item["supplier_code"], item["capacity_all"],
                                             item["capacity_for_xl_car"], item["capacity_for_l_car"],
                                             item["capacity_for_m_car"],
                                             item["capacity_for_s_car"], item["capacity_for_xs_car"],
                                             item["reported_package_type"],
                                             item["history_package_type"], item["preferred_direction"],
                                             item["availability"],
                                             item["trailer_available_time"], item["shipments_set"],
                                             item["loading_time"],
                                             item["planed_start_time"], item["planed_arrive_time"],
                                             item["actual_start_time"],
                                             item["actual_arrive_time"], item["start_location"],
                                             item["current_location"],
                                             item["destination"], item["historic_trajectory"])
    var_dict["trailer_dict"] = trailer_dict
    var_dict['mix_city'] = pd.read_json(input_json['mix_city'])
    var_dict['OTD_pinche'] = pd.read_json(input_json['OTD_pinche'])
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
        i[0]: order(str(i[0]), int(i[1]), int(i[4]),
                    (today - datetime.strptime(i[11], '%Y-%m-%d %H:%M:%S').date()).days,
                    int(i[12]), -1,
                    -1, int(i[3]), int(i[7]), int(i[6]), -1, datetime.strptime(i[11], '%Y-%m-%d %H:%M:%S').date(),
                    i[14],
                    -1) for i in input_file}
    var_dict['order_dict'] = order_dict

    trailer_tmpFile = request.form.get("trailer_raw_truck")
    strIo = StringIO(trailer_tmpFile)
    input_file = csv.reader(strIo)
    trailer_dict = {
        str(i[15]): trailer(str(i[15].strip()), -1, int(i[7]), int(i[9]), int(i[10]), int(i[11]), int(i[12]),
                            int(i[13]),
                            -1, -1, (map(int, ((i[6] + '、' + i[19]).split('、')))), 1,
                            datetime.strptime('2015-06-1', '%Y-%m-%d').date(), -1, -1, -1, -1, -1, -1, int(i[0]), -1,
                            -1,
                            -1) for i in input_file}
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
    mix_city = pd.read_json(input_json['mix_city'])
    OTD_pinche = pd.read_json(input_json['OTD_pinche'])


if __name__ == "__main__":
    GAVARP_Process_json(None)
