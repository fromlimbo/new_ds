#coding=utf-8
import pymongo
from pymongo.errors import ConnectionFailure
import logging
from datetime import datetime

class MongoDBClient(object):
    '''
    Mongodb数据库 连接，保存数据，读取数据
    __init__ 连接数据库，saveData 保存数据， readData重数据库中读取数据
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
        '''
        把指定的json数据result,保存到__init__ 初始化的数据库
        :param task_id: celery中生成task_id，对存储到mongodb的记录result进行标识
        :param result: 需要存储到mongodb中的数据
        :return: 数据在mongodb中的ObjectId
        '''
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
        '''
        mongodb数据库中根据task_id,读取数据
        :param task_id: celery中生成task_id，对存储到mongodb的记录result进行标识
        :return: res 根据task_id读取到的数据
        '''
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
        '''
        删除数据库中的一条记录
        :param task_id: celery中生成task_id，对存储到mongodb的记录result进行标识
        :return: res 删除的数据
        '''
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




