# -*- coding: utf-8 -*-
from utils import MongoDBClient
from config import *
import unittest
import logging

class MongoTester(unittest.TestCase):
    def testConnection(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        print "connection ok"

    def testSave(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        mongoclient.saveData('task5','result')

    def testRead(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        retval=mongoclient.readData("task5")
        assert retval['result']=='result'

if __name__ == "__main__":
    unittest.main()
