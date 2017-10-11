import logging
class AuthConfig:
    USER_NAME="admin"
    PASSWORD="admin"
    AUTH_URL="http://localhost:8090/api/ai/gateway/security/authenticate"

class CeleryConfig(object):

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
    REPORT_SERVER = "http://127.0.0.1"
    REPORT_PORT = "5000"
    REPORT_ADDRESS = "/con"

    @staticmethod
    def __init__(self):
        pass


class MQLogConfig:
    MQHOST = "localhost"
    MQPORT = 5672
    VIRTUAL_HOST = None
    USERNAME = None
    PASSWORD = None
    EXCHANGE = "log"
    EXCHANGE_TYPE = "topic"
    BRIND_KEYS = {'DEBUG':'DEBUG',
                   'INFO':'INFO',
                   'CRITICAL':'CRITICAL',
                   'WARNING':'WARNING',
                   'ERROR':'ERROR'}

    QUEUE_NAMES = {'DEBUG':'logging_debug_queue',
                   'INFO':'logging_info_queue',
                   'CRITICAL':'logging_critical_queue',
                   'WARNING':'logging_warning_queue',
                   'ERROR':'logging_error_queue'}
    @staticmethod
    def __init__(self):
        pass