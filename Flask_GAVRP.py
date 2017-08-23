# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
from io import StringIO
from dataProcess import GAVRP_Process

from algorithmModel import optimization
from multiprocessing import Process
from datetime import datetime
from flask import jsonify

app = Flask(__name__)
api = Api(app)


class TaskManager():
    """
        TaskManager 是一个任务容器，可以对所控制的任务进行启动、停止、查看状态等操作。
        todo:
            1. 增加共享变量，使得任务能在运行时反馈更细致的状态
        :var
            1. info,为当前任务信息，包含pid，启动时间，是否正在运行
            2. log, 为操作记录
            3. p, Manager所管理的task，为一个函数
    """
    def __init__(self):
        self.dataProcessed = None
        self.p = Process(target=optimization, args=(self.dataProcessed,))
        self.info = {}
        self.info['isrunning'] = False
        self.info['pid'] = ""
        self.info['starttime'] = ""
        self.log = []
        self.log.append({'operation': 'initiate', 'time': datetime.now()})

    def uploadData(self):
        # 上传数据
        self.dataProcessed = 0
        self.log.append({'operation': 'upload data', 'time': datetime.now()})
        return 0

    def start(self):
        # 开始任务
        if self.dataProcessed == None:
            return -1
        if self.p.is_alive():
            return "process has already been running."
        self.p.start()
        self.info['starttime'] = datetime.now()
        self.info['pid'] = self.p.pid
        self.info['isrunning'] = self.p.is_alive()
        self.log.append({'operation': 'start', 'time': datetime.now()})
        return "process starts"

    def showInfo(self):
        # 返回当前任务信息
        return self.info

    def terminate(self):
        self.p.terminate()
        self.info['isrunning'] = False
        self.info['pid'] = ""
        self.info['starttime'] = ""
        self.log.append({'operation': 'terminate', 'time': datetime.now()})
        return "process terminated"

    def showLog(self):
        return self.log


# Flask视图函数，用于暴露web调用接口
@app.route('/view')
def view():
    return jsonify(tm.showInfo())


@app.route('/')
def index():
    return "hello world!"


@app.route('/uploaddata')
def uploadData():
	var_dict = GAVRP_Process(request)
    tm.uploadData()
    return "data uploaded"

@app.route('/start')
def startTask():
    return tm.start()


@app.route('/terminate')
def terminateTask():
    return tm.terminate()


@app.route('/log')
def showlog():
    return jsonify(tm.showLog())

if __name__ == '__main__':
    tm = TaskManager()
    app.run(debug=True)
