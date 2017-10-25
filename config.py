# -*- coding: utf-8 -*-
import logging
import ConfigParser
import os

cf = ConfigParser.ConfigParser()
#Configparser模块,操作文件格式为 ini,最好指定为绝对路径
filepath = os.path.abspath("document.ini")
cf.read(filepath)

class AuthConfig:
    USER_NAME=cf.get("AuthConfig","USER_NAME")
    PASSWORD=cf.get("AuthConfig","PASSWORD")
    AUTH_URL=cf.get("AuthConfig","AUTH_URL")

    @staticmethod
    def __init__():
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
    NAME =cf.get("CeleryConfig","NAME")
    BROKER_ADDRESS=cf.get("CeleryConfig","BROKER_ADDRESS")
    CELERY_TASK_SERIALIZER=cf.get("CeleryConfig","CELERY_TASK_SERIALIZER")
    # please set this to the algorithm name
    MAIN_NAME=cf.get("CeleryConfig","MAIN_NAME")

    @staticmethod
    def __init__(self):
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

        cf.set("CeleryConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(CeleryConfig, option, newname)
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

class MQConfig:
    MQ_HOST_ADDRESS=cf.get("MQConfig","MQ_HOST_ADDRESS")
    MQ_PORT=cf.get("MQConfig","MQ_PORT")
    MQ_QUEUE_NAME=cf.get("MQConfig","MQ_QUEUE_NAME")

    @staticmethod
    def __init__(self):
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

        cf.set("MQConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(MQConfig, option, newname)
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


class LoggerConfig:
    CONFIG1=cf.get("LoggerConfig","CONFIG1")

    @staticmethod
    def __init__(self):
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

        cf.set("LoggerConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(LoggerConfig, option, newname)
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

class DataLoaderConfig:
    RESTFUL_ADDRESS=cf.get("DataLoaderConfig","RESTFUL_ADDRESS")

    @staticmethod
    def __init__(self):
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

        cf.set("DataLoaderConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(DataLoaderConfig, option, newname)
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


class ReporterConfig:
    ADDRESS=cf.get("ReporterConfig","ADDRESS")

    @staticmethod
    def __init__(self):
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

        cf.set("ReporterConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(ReporterConfig, option, newname)
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



class AppConfig:
    PORT=cf.get("AppConfig","PORT")

    @staticmethod
    def __init__(self):
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

        cf.set("AppConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(AppConfig, option, newname)
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


class CacheConfig:
    CACHE_HOST_ADDRESS=cf.get("CacheConfig","CACHE_HOST_ADDRESS")
    CACHE_HOST_PORT=cf.get("CacheConfig","CACHE_HOST_PORT")

    @staticmethod
    def __init__(self):
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

        cf.set("CacheConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(CacheConfig, option, newname)
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


class MongoConfig:
    #mongodb-server 配置参数
    MONGO_ADDRESS=cf.get("MongoConfig","MONGO_ADDRESS")
    MONGO_PORT= cf.getint("MongoConfig","MONGO_PORT")
    MONGO_DATABASE=cf.get("MongoConfig","MONGO_DATABASE")
    MONGO_USER_NAME=cf.get("MongoConfig","MONGO_USER_NAME")
    MONGO_USER_PASSWORD=cf.get("MongoConfig","MONGO_USER_PASSWORD")
    MONGO_COLLECTION=cf.get("MongoConfig","MONGO_COLLECTION")

    @staticmethod
    def __init__(self):
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

        cf.set("MongoConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(MongoConfig, option, newname)
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


class reportConfig:
    #连接请求配置参数(reporter模块)
    REPORT_SERVER = cf.get("reportConfig","REPORT_SERVER")
    REPORT_PORT = cf.get("reportConfig","REPORT_PORT")
    REPORT_ADDRESS = cf.get("reportConfig","REPORT_ADDRESS")

    @staticmethod
    def __init__(self):
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

        cf.set("reportConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(reportConfig, option, newname)
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

class MQLogConfig:
    #集中日志模块中rabbitmq-server初始化参数(logconsumer,mqlogginghandler)
    MQHOST = cf.get("MQLogConfig","MQHOST")
    MQPORT = cf.getint("MQLogConfig","MQPORT")
    VIRTUAL_HOST =cf.get("MQLogConfig","VIRTUAL_HOST")
    USERNAME = cf.get("MQLogConfig","USERNAME")
    PASSWORD = cf.get("MQLogConfig","PASSWORD")
    EXCHANGE = cf.get("MQLogConfig","EXCHANGE")
    EXCHANGE_TYPE = cf.get("MQLogConfig","EXCHANGE_TYPE")

    #Consumer 中routing_key参数
    BRKENDS = cf.items("BRIND_KEYS")
    DIC_KEYS = {}
    for data in BRKENDS:
        DIC_KEYS[data[0].upper()] = data[1].upper()
    BRIND_KEYS = DIC_KEYS

    #集中日志 中消息队列名称
    QUEUES = cf.items("QUEUE_NAMES")
    DIC_QUEUE = {}
    for data in QUEUES:
        DIC_QUEUE[data[0].upper()] = data[1].upper()
    QUEUE_NAMES = DIC_QUEUE
    @staticmethod
    def __init__(self):
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

        cf.set("MQLogConfig", option, newname)
        cf.write(open(filepath, "w"))

        setattr(MQLogConfig, option, newname)
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


