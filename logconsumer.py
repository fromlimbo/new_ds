# -*- coding: utf-8 -*-
import sys
import pika
import logging
from datetime import datetime
from pika import credentials
from config import *

#rabbitmq server 队列中的消息写到文件中
def filecallback(ch, method, properties, body):
    with open("log", "a") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "::" + body + "\n")

#rabbitmq server 队列中的消息打印到屏幕
def printcallback(ch, method, properties, body):
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "::" + body + "\n"

class Consumer:
    '''
    集中日志管理模块，传入到rabbitmq的消息进行处理
    '''
    def __init__(self, config, type, callback=None):
        '''
        初始化需要连接的rabbitmq server
        :param config: 要连接的rabbitmq server 配置信息，config.py模块导入
        :param type: 需要接收的日志等级
        :param callback: 对接收到的日志信息进行的处理
        '''
        self.connection_para = dict(host=config.MQHOST)
        if config.MQPORT:
            self.connection_para['port'] = config.MQPORT
        if config.VIRTUAL_HOST:
            self.connection_para['virtual_host'] = config.VIRTUAL_HOST
        if config.USERNAME and config.PASSWORD:
            self.connection_para['credentials'] = credentials.PlainCredentials(config.USERNAME,config.PASSWORD)
        self.exchange = config.EXCHANGE
        self.exchange_type = config.EXCHANGE_TYPE
        self.connection, self.channel = None, None

        #连接到指定的rabbitmq server
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.connection_para))
        except Exception as e:
            print "connect to rabbitmq is error"
        else:
            self.channel = self.connection.channel()

        #创建rabbitmq server 的exchange，并使该机制持久化存储在rabbitmq中
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True, auto_delete=False)
        sys.stdout.write(
            '%s - stdout - [mq] Declare exchange success.\n' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        #创建需要监听的消息队列
        result = self.channel.queue_declare(queue=config.QUEUE_NAMES[type])
        queue_name = result.method.queue

        #exchange和需要监听的queue进行绑定
        self.channel.queue_bind(exchange=MQLogConfig.EXCHANGE,
                                queue=config.QUEUE_NAMES[type],
                                routing_key="#." + config.BRIND_KEYS[type])

        #对rabbitmq server 队列中的消息进行处理，默认把消息打印到console，可自己指定xxxcallback
        if callback==None:
            self.channel.basic_consume(printcallback,
                                       queue=queue_name,
                                       no_ack=True)
        else:
            self.channel.basic_consume(callback,
                                       queue=queue_name,
                                       no_ack=True)

    def start_consuming(self):
        self.channel.start_consuming()

if __name__ == "__main__":
    consumer = Consumer(MQLogConfig, 'CRITICAL')
    print ' [*] Waiting for logs. To exit press CTRL+C'
    consumer.start_consuming()









