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
        # mongoclient.saveData("task4",{'result':'result'})

    def testRead(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        retval=mongoclient.readData("task4")
        logging.debug(retval)


if __name__ == "__main__":
    unittest.main()
