# -*- coding: utf-8 -*-
from utils import MongoDBClient
from config import *
import unittest

class MongoTester(unittest.TestCase):
    def testConnection(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        print "connection ok"

    def testSave(self):
        pass
        # mongoclient = MongoDBClient(config=MongoConfig)
        # mongoclient.saveData({"id":"123",'result':'result'})

    def testRead(self):
        pass
        # mongoclient = MongoDBClient(config=MongoConfig)
        # retval=mongoclient.resdData()


if __name__ == "__main__":
    unittest.main()
