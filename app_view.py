# -*- coding: utf-8 -*-
from app import flask,state
from flask import jsonify, request
from app import celery
from dataProcess.processing import GAVARP_Process_json
from algorithmModel.algorithm_entry import optimization

import time
from celery.app.control import Inspect

import json
from collections import OrderedDict
from celeflow import tasks
# from events import state,listtasks



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

@flask.route('/api/workers')
def workers():
    '''
    获取所有worker的基本信息，返回格式为：
    [{"worker_name":xx,
      "state":xx,
       "pid":xx,
       "pool":xx,
       "broker":xx},
       ...]
    :return:
    '''
    info = {}
    for name,worker in state.workers.items():
        info[name] = worker.alive
    return json.dumps(info,ensure_ascii=False)




@flask.route('/api/workers/shutdown/<worker_id>',methods=['POST'])
def workers_shutdown(worker_id):
    inspect = Inspect(destination=[worker_id], app=celery)
    test_ping = inspect.ping()
    if test_ping != None:
        celery.control.broadcast("shutdown",destination=[worker_id])
    shut_ping = inspect.ping()
    if shut_ping == None:
        return "the worker {} was shutdown".format(worker_id)


@flask.route('/api/tasks')
def task_basics():
    '''
    获取所有task的基本信息，返回格式为：
    [{"task_name":xx,
      "id":xx,
       "start_time":xx,
       "worker_name":xx},
       ...]
    :return:
    '''
    result = []
    for task_id, task in tasks.iter_tasks(state):
        task = tasks.as_dict(task)
        task.pop('worker', None)
        result.append((task_id, task))
    return json.dumps(dict(result),ensure_ascii=False)




@celery.task()
def add(x,y):
    time.sleep(20)
    return x +y


