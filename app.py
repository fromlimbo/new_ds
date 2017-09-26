# -*- coding: utf-8 -*-

from flask import Flask
from utils import CacheHandler,MQHandler, Logger, Reporter, DataLoader
from config import *
from celery import Celery

flask = Flask(__name__)
flask.config.from_object(AppConfig)

celery=Celery(CeleryConfig.MAIN_NAME, broker=CeleryConfig.BROKER_ADDRESS)

dataloader=DataLoader(config=DataLoaderConfig)
mqhandler=MQHandler(config=MQConfig)
logger=Logger(config=LoggerConfig)
reporter=Reporter(config=ReporterConfig)
cachehandler=CacheHandler(config=CacheConfig)

from app_view import *

if __name__ == '__main__':
    # app.run(debug=True)
    # celery.start()
    flask.run()
