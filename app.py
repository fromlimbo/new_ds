# -*- coding: utf-8 -*-

from flask import Flask
from utils import Logger, MongoClient
from config import *
from celery import Celery

flask = Flask(__name__)
flask.config.from_object(AppConfig)

celery=Celery(CeleryConfig.MAIN_NAME, broker=CeleryConfig.BROKER_ADDRESS)


logger=Logger(config=LoggerConfig)
mongoclient=MongoClient(config=MongoConfig)

from app_view import *

if __name__ == '__main__':
    # app.run(debug=True)
    # celery.start()
    flask.run()
