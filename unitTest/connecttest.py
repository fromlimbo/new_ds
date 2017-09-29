# -*- coding: utf-8 -*-
from utils import Reporter
from config import *
import unittest
import logging

class connectTest(unittest.TestCase):

    def testGetConnection(self):
        report=Reporter(config=reportConfig)
        res = report.reportGet('[{"data":"get"}]')
        logging.debug("ok"+str(res))

    def testPostConnection(self):
        report = Reporter(config=reportConfig)
        res = report.reportPost('[{"data":"get"}]')
        logging.debug("ok"+str(res))



if __name__ == "__main__":
    unittest.main()