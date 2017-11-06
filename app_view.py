# -*- coding: utf-8 -*-
from app import flask
from flask import jsonify, request
from app import celery
from dataProcess.processing import GAVARP_Process_json
from algorithmModel.algorithm_entry import optimization


import time


from celery.app.control import Inspect

import json
from collections import OrderedDict


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
    worker_stats = worker_state()
    if not isinstance(worker_stats,dict):
        return worker_stats
    else:
        all_worker = list()
        for worker in worker_stats:
            dic = OrderedDict()
            dic["worker_name"] = worker
            dic["state"] = "online"
            dic["pid"] = worker_stats[worker]["pid"]
            dic["pool"] = worker_stats[worker]["pool"]["processes"]

            brok = worker_stats[worker]["broker"]
            dic["broker"] = dict(hostname=brok["hostname"],
                                 port = brok["port"],
                                 userid=brok["userid"],
                                 virtual = brok["virtual_host"],
                                 )
            all_worker.append(dic)
        return json.dumps(all_worker,ensure_ascii=False)



@flask.route('/api/workers/info/<worker_id>')
def workers_info(worker_id):
    worker_data = worker_state(worker_id)
    if isinstance(worker_data,dict):
        return json.dumps(worker_data,ensure_ascii=False)
    else:
        return worker_data


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
    ins = Inspect(app=celery)
    data_basic = ins.active()
    basic_info = list()
    for data in data_basic:
        if not data_basic[data]:
            return "no activate task"
        for info in data_basic[data]:
            basic_de = OrderedDict()
            basic_de["name"] = info["name"]
            basic_de["id"] = info["id"]
            basic_de["start_time"] = info["time_start"]
            basic_de["worker"] = info["hostname"]
            basic_info.append(basic_de)
    return json.dumps(basic_info,ensure_ascii=False)

@flask.route('/api/task/info/<task_id>')
def tasks_detail(task_id):
    inspect = Inspect(app=celery)
    detail_info = inspect.query_task(task_id)
    if not detail_info.values():
        return "no activate task"
    else:
        return json.dumps(detail_info,ensure_ascii=False)



def on_raw_message(body):
    print body

@celery.task()
def add(x,y):
    time.sleep(200)
    return x +y

def worker_state(worker_id=None):
    '''
    获取指定worker的详细信息

    :param worker_id: 列表类型的worker 名字，默认为空代表所有worker
    :return:
    '''
    if worker_id != None:
        inspect = Inspect(destination=[worker_id], app=celery)
    else:
        inspect = Inspect(app=celery)
    # test_ping 是字典格式 ,{u'ce@ubuntu': {u'ok': u'pong'},...}
    test_ping = inspect.ping()
    if test_ping != None:
        work_stats = inspect.stats()
        # work_info = json.dumps(work_stats, ensure_ascii=False)
        return work_stats
    else:
        return "can not connect to the worker {}".format(worker_id)

