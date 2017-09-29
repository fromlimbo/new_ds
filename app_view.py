from app import flask
from flask import jsonify
from app import celery

@flask.route('/')
def index():
    return "hello world!"


@flask.route('/start')
def start_task():
    add.delay(3,4)
    return jsonify({'id':'123'})

@flask.route('/con',methods=['GET', 'POST'])
def connect_Test():
    return 'connection ok'


@celery.task
def add(x,y):
    return x+y