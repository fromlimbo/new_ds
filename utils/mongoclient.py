#coding=utf-8
import pymongo
from pymongo.errors import ConnectionFailure
import logging

class MongoDBClient(object):

    def __init__(self,config=None):
        self.config=config
        self.client = pymongo.MongoClient(host=self.config.MONGO_ADDRESS,port=self.config.MONGO_PORT)
        try:
            self.client.admin.command("ping")
        except ConnectionFailure:
            raise ConnectionFailure
        else:
            self.db = self.client[self.config.MONGO_DATABASE]
            self.collection = self.db[self.config.MONGO_COLLECTION]
            # coll=db.collection_names(include_system_collections=False)

    def saveData(self,id,result):
        savdata = dict(task_id=id,result=result)
        try:
            self.collection.insert(savdata)
        except Exception as e:
            logging.debug(e)
            return -1
        else:
            logging.debug("ok")
            return 0

    def readData(self,id):
        try:
            res = self.collection.find_one({"task_id":id})
        except Exception as e:
            logging.debug(e)
            return -1
        else:
            if res is None:
                logging.debug("task_id is None")
                return -1
            return res



