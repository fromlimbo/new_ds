from app import flask
from flask import jsonify, request
from app import celery
from dataProcess.processing import GAVARP_Process_json
from algorithmModel.algorithm_entry import optimization
import time
import os

@flask.route('/')
def index():
    return "hello world!"

@flask.route("/revoke")
def test_revoke():
    res = add.delay(3,2)
    return "test revoke over"

@flask.route('/start',methods=['POST'])
def start_task():
    data = request.get_json()
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


@celery.task(bind=True,track_started=True)
def add(self,x,y):
    # self.update_state(meta={"taskpid":os.getpid()})
    time.sleep(30)
    return x+y

def on_raw_message(body):
    print body