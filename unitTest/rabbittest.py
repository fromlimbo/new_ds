import unittest
from utils import Handler
import logging

class rabbitTest(unittest.TestCase):

    def testProducerConnect(self):
        Loger = logging.getLogger()
        handler = Handler(host="localhost",port=5672)
        Loger.addHandler(handler)
        Loger.debug("hello world warning")





if __name__ == "__main__":
    unittest.main()