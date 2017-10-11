# -*- coding: utf-8 -*-
import sys
import pika
import logging
from datetime import datetime
from pika import credentials
from config import *


def filecallback(ch, method, properties, body):
    with open("log", "a") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "::" + body + "\n")

def printcallback(ch, method, properties, body):
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "::" + body + "\n"

class Consumer:

    def __init__(self, config, type, callback=None):
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
        # make sure exchange only declared once.

        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.connection_para))
        except Exception as e:
            print e
        else:
            self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type=config.EXCHANGE_TYPE, durable=True, auto_delete=False)
        sys.stdout.write(
            '%s - stdout - [mq] Declare exchange success.\n' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


        result = self.channel.queue_declare(exclusive=True,queue=config.QUEUE_NAMES[type])
        queue_name = result.method.queue

        self.channel.queue_bind(exchange=MQLogConfig.EXCHANGE,
                                        queue=config.QUEUE_NAMES[type],
                                        routing_key="#." + config.BRIND_KEYS[type])
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
    consumer = Consumer(MQLogConfig, 'DEBUG')
    print ' [*] Waiting for logs. To exit press CTRL+C'
    consumer.start_consuming()









