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
import os

flask = Flask(__name__)
configfile=os.path.abspath("config/local_config_liangliang.ini")

AppConfig = ConfigBuilder(configfile,"AppConfig")
AppConfigs = AppConfig.todict()
flask.config.from_object(AppConfigs)

LoggerConfig = ConfigBuilder(configfile,"LoggerConfig")
LoggerConfigs = LoggerConfig.todict()

MongoConfig = ConfigBuilder(configfile,"MongoConfig")
MongoConfigs = MongoConfig.todict()

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='myapp.log',
                filemode='a')



CeleryConfig = ConfigBuilder(configfile,"CeleryConfig")
CeleryConfigs = CeleryConfig.todict()

celery=Celery(CeleryConfigs["main_name"], broker=CeleryConfigs["broker_address"],
              task_serializer=CeleryConfigs["celery_task_serializer"],
              accept_content=['pickle'])
celery.conf['CELERY_TASK_SERIALIZER'] = 'pickle'
celery.conf['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']
celery.conf['CELERYD_HIJACK_ROOT_LOGGER'] = False


# from app_view import *

if __name__ == '__main__':
    from app_view import *
    logger = logging.getLogger(__name__)
    logger.info("service starts.")
    flask.run()
