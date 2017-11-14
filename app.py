# -*- coding: utf-8 -*-

from flask import Flask
from utils import Logger, MongoDBClient
from celery import Celery
import logging
from config import ConfigBuilder
import threading
from celery.events import EventReceiver
from celery.events.state import State
import time
from events import *

flask = Flask(__name__)

AppConfig = ConfigBuilder("config/config_sample.ini","AppConfig")
AppConfigs = AppConfig.todict()
flask.config.from_object(AppConfigs)

LoggerConfig = ConfigBuilder("config/config_sample.ini","LoggerConfig")
LoggerConfigs = LoggerConfig.todict()

MongoConfig = ConfigBuilder("config/config_sample.ini","MongoConfig")
MongoConfigs = MongoConfig.todict()

logger=Logger(config=LoggerConfigs)
logging.basicConfig(level=logging.DEBUG)


<<<<<<< HEAD
=======

# logger=Logger(config=LoggerConfig)

>>>>>>> master
mongoclient=MongoDBClient(config=MongoConfigs)

CeleryConfig = ConfigBuilder("config/config_sample.ini","CeleryConfig")
CeleryConfigs = CeleryConfig.todict()
<<<<<<< HEAD
=======
celery=Celery(CeleryConfigs["main_name"], broker=CeleryConfigs["broker_address"],
              task_serializer=CeleryConfigs["celery_task_serializer"],
              accept_content=['pickle'])
celery.conf['CELERY_TASK_SERIALIZER'] = 'pickle'
celery.conf['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']

>>>>>>> master

celery=Celery(CeleryConfigs["main_name"],
              broker=CeleryConfigs["broker_address"],
              loglevel = "info",
              backend = "rpc://",
              task_serializer=CeleryConfigs["celery_task_serializer"])

state = State()
from app_view import *
<<<<<<< HEAD
logging.debug("service starts")



=======

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

logging.debug("service starts")


>>>>>>> master
if __name__ == '__main__':
    tasks_event = Events(state)
    tasks_event.setDaemon(True)
    tasks_event.run()
    flask.run()