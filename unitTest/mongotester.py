# -*- coding: utf-8 -*-
from utils import MongoDBClient
from config import *
import unittest

class MongoTester(unittest.TestCase):
    def testConnection(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        self.assertIsNotNone(mongoclient)

    def testSave(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        retval=mongoclient.saveData('task5','result')
        self.assertIsNotNone(retval)

    def testRead(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        retval=mongoclient.readData('task5')
        # self.assertNotEqual(retval,-1)
        # self.assertEqual(retval['result'],'result')

    def testDelete(self):
        mongoclient = MongoDBClient(config=MongoConfig)
        mongoclient.deleteData('task5')
        retval = mongoclient.readData("task5")
        self.assertEqual(retval, -1)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(MongoTester('testConnection'))
    suite.addTest(MongoTester('testSave'))
    suite.addTest(MongoTester('testRead'))
    suite.addTest(MongoTester('testDelete'))
    return suite

if __name__ == "__main__":
    suite=suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
