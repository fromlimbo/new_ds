# -*- coding: utf-8 -*-

import unittest
from dataProcess import GAVRP_Process
from algorithmModel import algorithm_entry

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Request():
    def __init__(self):
        self.form = {}

    def putValue(self, key, value):
        self.form[key] = value

class dataProcessTester(unittest.TestCase):
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




if "__name__" == "__main__":
    unittest.main()
