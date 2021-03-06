# -*- coding: utf-8 -*-
import pika
from pika import credentials
from datetime import datetime
import logging
import json
import sys

class MQLoggingHandler(logging.Handler):
    '''
     handler that send log to rabbitmq, using pika.
    '''

    def __init__(self, config):
        '''
        初始化需要连接的rabbitmq server

        :param config: 要连接的rabbitmq server 配置信息，config.py模块导入
        '''
        logging.Handler.__init__(self)
        self.connection_para = dict(host=config["mqhsot"])
        if config["mqhsot"]:
            self.connection_para['port'] = config["mqport"]
        if config["virtual_host"]:
            self.connection_para['virtual_host'] = config["virtual_host"]
        if config["username"] and config["password"]:
            self.connection_para['credentials'] = credentials.PlainCredentials(config["username"], config["password"])
        self.exchange = config["exchange"]
        self.exchange_type=config["exchange_type"]
        self.connection, self.channel = None, None
        # make sure exchange only declared once.
        self.is_exchange_declared = False
        # init connection.
        self.connect()

    def connect(self):
        '''
        connect to rabbitMq server, using topic exchange
        '''
        # emit pika to stdout, avoid RecursionError when connecting.
        pika_logger = logging.getLogger('pika')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s'))
        pika_logger.addHandler(handler)
        pika_logger.propagate = False
        pika_logger.setLevel(logging.WARNING)
        # forbidden heartbeat.
        self.connection_para['heartbeat_interval'] = 0
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.connection_para))
        self.channel = self.connection.channel()
        sys.stdout.write('%s - stdout - [mq] Connect success.\n' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if not self.is_exchange_declared:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type,
                                          durable=True, auto_delete=False)
            sys.stdout.write(
                '%s - stdout - [mq] Declare exchange success.\n' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.is_exchange_declared = True


    def emit(self, record):
        try:
            if not self.connection or not self.channel:
                self.connect()
            routing_key = "{name}.{level}".format(name=record.name, level=record.levelname)
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key=routing_key,
                                       #传入到rabbitmq队列中的日志信息，还可传入，pathname,lineno,args,exc_info
                                       #func,例如：record.pathname
                                       body=json.dumps({'name':record.name,
                                                        'level':record.levelname,
                                                         'mesg':record.msg}),
                                       properties=pika.BasicProperties(
                                           delivery_mode=2
                                       ))

        except Exception:
            # for the sake of reconnect
            self.channel, self.connection = None, None
            self.handleError(record)

    def close(self):
        '''
        clear when closing
        '''
        self.acquire()
        try:
            logging.Handler.close(self)
            if self.channel:
                self.channel.close()
            if self.connection:
                self.connection.close()
            sys.stdout.write('%s - stdout - [mq] Clean up success.\n' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        finally:
            self.release()