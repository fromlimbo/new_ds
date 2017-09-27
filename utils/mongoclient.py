#coding=utf-8
import pymongo
from pymongo.errors import ConnectionFailure

class MongoDBClient(object):

    def __init__(self,config=None):
        self.config=config
        self.client = pymongo.MongoClient(host=self.config.MONGO_ADDRESS,port=self.config.MONGO_PORT)
        try:
            self.client.admin.command("ismaster")
        except ConnectionFailure:
            print "server not available "
        else:
            self.db = self.client.config.DynamicSchedule
            self.collection = self.db.config.my_collection
            # coll=db.collection_names(include_system_collections=False)

    def saveData(self,id,result):
        savdata = dict(task_id=id,result=result)
        try:
            self.collection.insert(savdata)
        except Exception as e:
            print e
            return -1
        else:
            print "ok"
            return 0

    def readData(self,id):
        try:
            res = self.collection.find_one({"task_id":id})
        except Exception as e:
            print e
            return -1
        else:
            if res is None:
                print "task_id is None"
                return 0
            print res
            return 0



