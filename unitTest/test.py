# -*- coding: utf-8 -*-

import unittest
from dataProcess import GAVRP_Process, GAVARP_Process_json
# from dataProcess import GAVRP_Process, GAVARP_Process_json
import pandas as pd
import json
from datetime import datetime
from algorithmModel.algorithm_entry import optimization

import sys
import requests

reload(sys)
sys.setdefaultencoding('utf8')


class Request():
    def __init__(self):
        self.form = {}

    def putValue(self, key, value):
        self.form[key] = value

class DataProcessTester(unittest.TestCase):
    def testProcess(self):

        request = Request()
        with open('testData/order_raw.csv','r') as f:
            content=f.read()
            request.putValue('order_raw', unicode(content))
            f.close()

        with open('testData/trailer_raw_truck.csv', 'r') as f:
            content=f.read()
            request.putValue('trailer_raw_truck', unicode(content))
            f.close()

        with open('testData/OTD_pinche.csv', 'r') as f:
            content=f.read()
            request.putValue('OTD_pinche', unicode(content))
            f.close()

        with open('testData/mix_city.csv', 'r') as f:
            content=f.read()
            request.putValue('mix_city', unicode(content))
            f.close()

        assert(GAVRP_Process(request)!=None)

    def testConnection(self):
        print('testing connection')
        retval = {"taskId": optimization.request.id,
                  "trailerOrders": []}
        # retval = {'haha':'haha'}
        headers = {'content-type': 'application/json'}
        r = requests.post("http://192.168.204.169:28109/ids/engine/dealPlan", data=json.dumps(retval),
                          headers=headers)
        print(r)

    def testAlgorithm(self):
        request = Request()
        with open('testData/order_raw.csv','r') as f:
            content=f.read()
            request.putValue('order_raw', unicode(content))
            f.close()

        with open('testData/trailer_raw_truck.csv', 'r') as f:
            content=f.read()
            request.putValue('trailer_raw_truck', unicode(content))
            f.close()

        with open('testData/OTD_pinche.csv', 'r') as f:
            content=f.read()
            request.putValue('OTD_pinche', unicode(content))
            f.close()

        with open('testData/mix_city.csv', 'r') as f:
            content=f.read()
            request.putValue('mix_city', unicode(content))
            f.close()

        data=GAVRP_Process(request)
        # optimization(data)

class DataProcessJsonTester(unittest.TestCase):

    def test_process_json(self):
        mix_city=pd.read_csv('testData/mix_city.csv')
        mix_city_json=mix_city.to_json(orient='records')

        otd_pinche=pd.read_csv('testData/OTD_pinche.csv')
        otd_pinche_json=otd_pinche.to_json(orient='records')

        order=pd.read_csv('testData/order_raw_json.csv')
        order_dict=order.to_dict(orient='records')
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').date()
        for item in order_dict:
            item['OTD']=(today - datetime.strptime(item['effective_time'],'%Y-%m-%d %H:%M:%S').date()).days
        order_json=json.dumps(order_dict)
        print order_json[0]

        trailer=pd.read_csv('testData/trailer_raw_truck_json.csv')
        trailer['availability']=1
        trailer['trailer_available_time']='2015-06-1'
        trailer_json=trailer.to_json(orient='records')

        data_json={'mix_city':mix_city_json,'OTD_pinche':otd_pinche_json,
              'order':order_json, 'trailer':trailer_json}

        with open('data.txt', 'w') as outfile:
            json.dump(data_json, outfile)

        data=GAVARP_Process_json(data_json)
        result=optimization(data)


def jsonsuite():
    suite = unittest.TestSuite()
    suite.addTest(DataProcessJsonTester('test_process_json'))
    return suite


def normalsuite():
    suite = unittest.TestSuite()
    suite.addTest(DataProcessTester('testConnection'))
    suite.addTest(DataProcessTester('testAlgorithm'))
    return suite

if __name__ == "__main__":
    suite = normalsuite()
    unittest.TextTestRunner(verbosity=2).run(suite)

