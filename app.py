# -*- coding: utf-8 -*-

from flask import Flask
from utils import Logger, MongoDBClient
from config import *
from celery import Celery
import logging
from config import ConfigBuilder

flask = Flask(__name__)
AppConfig = ConfigBuilder("config/config_sample.ini","AppConfig")
AppConfigs = AppConfig.todict()
flask.config.from_object(AppConfigs)

LoggerConfig = ConfigBuilder("config/config_sample.ini","LoggerConfig")
LoggerConfigs = LoggerConfig.todict()
logger=Logger(config=LoggerConfigs)
logging.basicConfig(level=logging.DEBUG)

CeleryConfig = ConfigBuilder("config/config_sample.ini","CeleryConfig")
CeleryConfigs = CeleryConfig.todict()
celery=Celery(CeleryConfigs["main_name"], broker=CeleryConfigs["broker_address"],
              task_serializer=CeleryConfigs["celery_task_serializer"],
              accept_content=['pickle'])
celery.conf['CELERY_TASK_SERIALIZER'] = 'pickle'
celery.conf['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']

MongoConfig = ConfigBuilder("config/config_sample.ini","MongoConfig")
MongoConfigs = MongoConfig.todict()
mongoclient=MongoDBClient(config=MongoConfigs)

from app_view import *

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

logging.debug("service starts")


if __name__ == '__main__':
    flask.run()