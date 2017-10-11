import platform
import unittest
from utils import MQLoggingHandler
import logging
from config import *
import os
import json

class rabbitTest(unittest.TestCase):

    def testProducerConnect(self):
        loger = logging.getLogger(__name__)
        handler = MQLoggingHandler(MQLogConfig)
        loger.addHandler(handler)
        loger.setLevel(logging.DEBUG)

        computer_name=platform.node()
        pid=os.getpid()
        loger.debug(json.dumps({'computer_name':computer_name,
                                'pid':pid,
                                'msg':'hello world'}))
        loger.info('hello')

if __name__ == "__main__":
    unittest.main()