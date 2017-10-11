# -*- coding: utf-8 -*-
import sys
import pika
import logging
from datetime import datetime
from pika import credentials
from config import *


class Consumer:

    def __init__(self, config):
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
        self.is_exchange_declared = False

        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.connection_para))
        except Exception as e:
            print e
        else:
            self.channel = self.connection.channel()

def callback(ch,method,properties,body):
    with open("log","a") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"::"+body+"\n")



if __name__ == "__main__":
    consumer = Consumer(LogMQ)
    result = consumer.channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for bind_key in LogMQ.BRIND_KEYS:
        consumer.channel.queue_bind(exchange=LogMQ.EXCHANGE,
                                   queue=queue_name,
                                   routing_key="#."+bind_key)


    consumer.channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    consumer.channel.start_consuming()









