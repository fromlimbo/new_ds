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

MongoConfig = ConfigBuilder("config/config_sample.ini","MongoConfig")
MongoConfigs = MongoConfig.todict()

logger=Logger(config=LoggerConfigs)
logging.basicConfig(level=logging.DEBUG)


mongoclient=MongoDBClient(config=MongoConfigs)

CeleryConfig = ConfigBuilder("config/config_sample.ini","CeleryConfig")
CeleryConfigs = CeleryConfig.todict()

celery=Celery(CeleryConfigs["main_name"],
              broker=CeleryConfigs["broker_address"],
              backend = "rpc://",
              task_serializer=CeleryConfigs["celery_task_serializer"])



from app_view import *

logging.debug("service starts")

if __name__ == '__main__':
    flask.run()