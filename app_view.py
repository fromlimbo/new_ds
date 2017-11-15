# -*- coding: utf-8 -*-
from app import flask
from flask import jsonify, request
from app import celery
from dataProcess.processing import GAVARP_Process_json
from algorithmModel.algorithm_entry import optimization

import time
from celery.app.control import Inspect

import json
from celeflow import tasks
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
    t=time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time()))
    with open('input_data.json', 'w') as f:
        json.dump(data,f)
    print(os.path.abspath(os.path.join('querydata',t+'.json')))
    with open(os.path.join('querydata',t+'.json'),'w') as f:
        json.dump(data, f)
    input_data = GAVARP_Process_json(data)
    if not input_data == -1:
        print 'parsing successfully'
    else:
        return jsonify({'feedback': 'data error!'})
    res = optimization.delay(input_data)
    return jsonify({'task_id': res.id})

@flask.route('/add')
def start_add():
    res = add.delay(1,3)
    return jsonify({'task_id': res.id})

@flask.route('/con',methods=['GET', 'POST'])
def connect_Test():
    return 'connection ok'

@flask.route('/api/workers')
def workers():
    '''
    获取所有worker的基本信息，返回格式为：
    {'active': {u'celery@ubuntu': []},
 'active_queues': {u'celery@ubuntu': [{u'alias': None,
    u'auto_delete': False,
    u'binding_arguments': None,
    u'bindings': [],
    u'consumer_arguments': None,
    u'durable': True,
    u'exchange': {u'arguments': None,
     u'auto_delete': False,
     u'delivery_mode': None,
     u'durable': True,
     u'name': u'celery',
     u'no_declare': False,
     u'passive': False,
     u'type': u'direct'},
    u'exclusive': False,
    u'expires': None,
    u'max_length': None,
    u'max_length_bytes': None,
    u'max_priority': None,
    u'message_ttl': None,
    u'name': u'celery',
    u'no_ack': False,
    u'no_declare': None,
    u'queue_arguments': None,
    u'routing_key': u'celery'}]},
 'conf': {u'celery@ubuntu': {u'broker_url': u'amqp://test:********@192.168.205.169:5672/DynamicSchedule',
   u'include': [u'algorithmModel.algorithm_entry',
    u'celery.app.builtins',
    u'app_view'],
   u'result_backend': u'rpc:///'}},
 'registered': {u'celery@ubuntu': [u'algorithmModel.algorithm_entry.optimization',
   u'app_view.add']},
 'reserved': {u'celery@ubuntu': []},
 'revoked': {u'celery@ubuntu': []},
 'scheduled': {u'celery@ubuntu': []},
 'stats': {u'celery@ubuntu': {u'broker': {u'alternates': [],
    u'connect_timeout': 4,
    u'failover_strategy': u'round-robin',
    u'heartbeat': 120.0,
    u'hostname': u'192.168.205.169',
    u'insist': False,
    u'login_method': u'AMQPLAIN',
    u'port': 5672,
    u'ssl': False,
    u'transport': u'amqp',
    u'transport_options': {},
    u'uri_prefix': None,
    u'userid': u'test',
    u'virtual_host': u'DynamicSchedule'},
   u'clock': u'3062',
   u'pid': 5599,
   u'pool': {u'max-concurrency': 4,
    u'max-tasks-per-child': u'N/A',
    u'processes': [5608, 5609, 5610, 5613],
    u'put-guarded-by-semaphore': False,
    u'timeouts': [0, 0],
    u'writes': {u'all': u'',
     u'avg': u'0.00%',
     u'inqueues': {u'active': 0, u'total': 4},
     u'raw': u'',
     u'strategy': u'fair',
     u'total': 0}},
   u'prefetch_count': 16,
   u'rusage': {u'idrss': 0,
    u'inblock': 6104,
    u'isrss': 0,
    u'ixrss': 0,
    u'majflt': 0,
    u'maxrss': 53660,
    u'minflt': 21858,
    u'msgrcv': 0,
    u'msgsnd': 0,
    u'nivcsw': 664,
    u'nsignals': 0,
    u'nswap': 0,
    u'nvcsw': 16273,
    u'oublock': 8,
    u'stime': 6.916,
    u'utime': 4.228},
   u'total': {}}}}
    '''
    INSPECT_METHODS = ('stats', 'active_queues', 'registered', 'scheduled',
                       'active', 'reserved', 'revoked', 'conf')
    inspect = Inspect(app=celery)
    active_worker = inspect.active()
    if not active_worker:
        return "no worker active"
    result = dict()
    for methods in INSPECT_METHODS:
       result[methods] = getattr(inspect,methods)
    return json.dumps(result,ensure_ascii=False)


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
def tasks_info():
    '''
    获取所有task的基本信息，返回格式为：
    {
      "e42ceb2d-8730-47b5-8b4d-8e0d2a1ef7c9": {
          "args": "[3, 4]",
          "client": null,
          "clock": 1079,
          "eta": null,
          "exception": null,
          "exchange": null,
          "expires": null,
          "failed": null,
          "kwargs": "{}",
          "name": "tasks.add",
          "received": 1398505411.107885,
          "result": "'7'",
          "retried": null,
          "retries": 0,
          "revoked": null,
          "routing_key": null,
          "runtime": 0.01610181899741292,
          "sent": null,
          "started": 1398505411.108985,
          "state": "SUCCESS",
          "succeeded": 1398505411.124802,
          "timestamp": 1398505411.124802,
          "traceback": null,
          "uuid": "e42ceb2d-8730-47b5-8b4d-8e0d2a1ef7c9"
      },
      "f67ea225-ae9e-42a8-90b0-5de0b24507e0": {
          "args": "[1, 2]",
          "client": null,
          "clock": 1042,
          "eta": null,
          "exception": null,
          "exchange": null,
          "expires": null,
          "failed": null,
          "kwargs": "{}",
          "name": "tasks.add",
          "received": 1398505395.327208,
          "result": "'3'",
          "retried": null,
          "retries": 0,
          "revoked": null,
          "routing_key": null,
          "runtime": 0.012884548006695695,
          "sent": null,
          "started": 1398505395.3289,
          "state": "SUCCESS",
          "succeeded": 1398505395.341089,
          "timestamp": 1398505395.341089,
          "traceback": null,
          "uuid": "f67ea225-ae9e-42a8-90b0-5de0b24507e0"
      }
  }
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


