# -*- coding: utf-8 -*-

import unittest
from dataProcess import GAVRP_Process
from algorithmModel import algorithm_entry
import pandas as pd

import sys

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
        algorithm_entry.optimization(data)

class DataProcessJsonTester(unittest.TestCase):

    def test_process_json(self):
        mix_city=pd.read_csv('testData/mix_city.csv')
        mix_city_json=mix_city.to_json(orient='records')

        otd_pinche=pd.read_csv('testData/OTD_pinche.csv')
        otd_pinche_json=otd_pinche.to_json(orient='records')

        order=pd.read_csv('testData/order_raw_json.csv')
        order_json=order.to_json(orient='records')

        trailer=pd.read_csv('testData/trailer_raw_truck_json.csv')
        trailer_json=trailer.to_json(orient='records')

        data_json={'mix_city':mix_city_json,'otd_pinche':otd_pinche_json,
              'order':order_json, 'trailer':trailer_json}

        # data=GAVRP_Process_json()


def jsonsuite():
    suite = unittest.TestSuite()
    suite.addTest(DataProcessJsonTester('test_process_json'))
    return suite

if __name__ == "__main__":
    suite = jsonsuite()
    unittest.TextTestRunner(verbosity=2).run(suite)
