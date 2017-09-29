#coding=utf-8
import pymongo
from pymongo.errors import ConnectionFailure
import logging
from datetime import datetime

class MongoDBClient(object):
    '''
    mongodb客户端
    '''
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

    def saveData(self,task_id,result):
        savdata = {'task_id':task_id,
                   # "created_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   'result':result}
        try:
            id=self.collection.insert_one(savdata).inserted_id
        except Exception as e:
            logging.debug(e)
            return -1
        else:
            logging.debug("ok")
            return id

    def readData(self,task_id):
        try:
            res = self.collection.find_one({"task_id":task_id})
        except Exception as e:
            logging.debug(e)
            return -1
        else:
            if res is None:
                logging.debug("No result for this task id.")
                return -1
            return res

    def deleteData(self, task_id):
        try:
            res = self.collection.delete_one({'task_id':task_id})
        except Exception as e:
            logging.debug(e)
            return -1
        else:
            if res is None:
                logging.debug("No result for this task id.")
                return -1
            return res




