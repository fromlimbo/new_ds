# -*- coding: utf-8 -*-
import logging
import ConfigParser

cf = ConfigParser.ConfigParser()
#Configparser模块,操作文件格式为 ini,最好指定为绝对路径
filepath = r"E:\anji\DynamicSchedule-Flask\document.ini"
cf.read(filepath)

class AuthConfig:
    USER_NAME=cf.get("AuthConfig","USER_NAME")
    PASSWORD=cf.get("AuthConfig","PASSWORD")
    AUTH_URL=cf.get("AuthConfig","AUTH_URL")

    @staticmethod
    def __init__(cls):
        pass

    @staticmethod
    def save_modify(section, option, newname):
        '''
        保存对配置文件的修改
        :param section: ini文件中需要修改的section
        :param option:  ini文件中需要修改的option
        :param newname:  需要被修改的值
        :return:
        '''
        keys = cf.options(section)
        if option not in keys:
            raise (Exception("key error"))

        cf.set("AuthConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(AuthConfig, option, newname)
        return 0

    @staticmethod
    def getconf(section):
        '''
        获得指定的配置数据
        :param section: ini文件中指定的section
        :return: dict 格式，指定section的详细数据
        '''
        context = {}
        try:
            data = cf.items(section)
        except Exception as e:
            logging.debug("section is error")
            return -1
        for info in data:
            context[info[0]] = info[1]
        return context

class CeleryConfig(object):
    NAME = "name is CeleryConfig"
    BROKER_ADDRESS="amqp://test:test@192.168.205.169:5672/DynamicSchedule"
    CELERY_TASK_SERIALIZER='pickle'
    # please set this to the algorithm name
    MAIN_NAME="dynamic-schedule"

    @staticmethod
    def __init__(self):
        pass

class MQConfig:
    MQ_HOST_ADDRESS="localhost"
    MQ_PORT=""
    MQ_QUEUE_NAME="algorithm1_tasks"

    @staticmethod
    def __init__(self):
        pass


class LoggerConfig:
    CONFIG1=""

    @staticmethod
    def __init__(self):
        pass


class DataLoaderConfig:
    RESTFUL_ADDRESS=""

    @staticmethod
    def __init__(self):
        pass

class ReporterConfig:
    ADDRESS=""

    @staticmethod
    def __init__(self):
        pass

class AppConfig:
    PORT=""

    @staticmethod
    def __init__(self):
        pass

class CacheConfig:
    CACHE_HOST_ADDRESS=""
    CACHE_HOST_PORT=""

    @staticmethod
    def __init__(self):
        pass


class MongoConfig:
    #mongodb-server 配置参数
    MONGO_ADDRESS= "192.168.205.169"
    MONGO_PORT= 27017
    MONGO_DATABASE="DynamicSchedule"
    MONGO_USER_NAME="test"
    MONGO_USER_PASSWORD="test"
    MONGO_COLLECTION="results"

    @staticmethod
    def __init__(self):
        pass

class reportConfig:
    #连接请求配置参数(reporter模块)
    REPORT_SERVER = "http://127.0.0.1"
    REPORT_PORT = "5000"
    REPORT_ADDRESS = "/con"

    @staticmethod
    def __init__(self):
        pass


class MQLogConfig:
    #集中日志模块中rabbitmq-server初始化参数(logconsumer,mqlogginghandler)
    MQHOST = "localhost"
    MQPORT = 5672
    VIRTUAL_HOST = None
    USERNAME = None
    PASSWORD = None
    EXCHANGE = "log"
    EXCHANGE_TYPE = "topic"

    #Consumer 中routing_key参数
    BRIND_KEYS = {'DEBUG':'DEBUG',
                   'INFO':'INFO',
                   'CRITICAL':'CRITICAL',
                   'WARNING':'WARNING',
                   'ERROR':'ERROR'}
    #集中日志 中消息队列名称
    QUEUE_NAMES = {'DEBUG':'logging_debug_queue',
                   'INFO':'logging_info_queue',
                   'CRITICAL':'logging_critical_queue',
                   'WARNING':'logging_warning_queue',
                   'ERROR':'logging_error_queue'}
    @staticmethod
    def __init__(self):
        pass