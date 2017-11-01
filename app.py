# -*- coding: utf-8 -*-

from flask import Flask
from utils import Logger, MongoDBClient
from config import *
from celery import Celery
import logging

flask = Flask(__name__)
AppConfig = ConfigBuild("document.ini","AppConfig")
AppConfigs = AppConfig.todict()

CeleryConfig = ConfigBuild("document.ini","CeleryConfig")
CeleryConfigs = CeleryConfig.todict()

MongoConfig = ConfigBuild("document.ini","MongoConfig")
MongoConfigs = MongoConfig.todict()

LoggerConfig = ConfigBuild("document.ini","LoggerConfig")
LoggerConfigs = LoggerConfig.todict()

flask.config.from_object(AppConfigs)
celery=Celery(CeleryConfigs["main_name"], broker=CeleryConfigs["broker_address"],
              task_serializer=CeleryConfigs["celery_task_serializer"])


logger=Logger(config=LoggerConfigs)
mongoclient=MongoDBClient(config=MongoConfigs)

logging.basicConfig(level=logging.DEBUG)

from app_view import *

logging.debug("service starts")

