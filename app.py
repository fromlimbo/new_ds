# -*- coding: utf-8 -*-

from flask import Flask
from utils import Logger, MongoDBClient
from config import *
from celery import Celery
import logging

flask = Flask(__name__)
flask.config.from_object(AppConfig)

celery=Celery(CeleryConfig.MAIN_NAME, broker=CeleryConfig.BROKER_ADDRESS,
              task_serializer=CeleryConfig.CELERY_TASK_SERIALIZER)
celery.conf.update(CELERY_ACCEPT_CONTENT=['pickle'])


logger=Logger(config=LoggerConfig)
mongoclient=MongoDBClient(config=MongoConfig)

logging.basicConfig(level=logging.DEBUG)

from app_view import *

logging.debug("service starts")

if __name__ == '__main__':
    flask.run()