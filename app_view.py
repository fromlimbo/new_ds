from app import flask
from flask import jsonify, request
from app import celery
from dataProcess.processing import GAVARP_Process_json
from algorithmModel.algorithm_entry import optimization
import json

@flask.route('/')
def index():
    return "hello world!"


@flask.route('/start',methods=['POST'])
def start_task():
    data = request.get_json()
    with open('input_data.json', 'w') as f:
        json.dump(data,f)
    input_data = GAVARP_Process_json(data)
    if not input_data == -1:
        print 'parsing successfully'
    else:
        return jsonify({'feedback': 'data error!'})
    res = optimization.delay(input_data)
    return jsonify({'task_id': res.id})


@flask.route('/con',methods=['GET', 'POST'])
def connect_Test():
    return 'connection ok'


@celery.task
def add(x,y):
    return x+y