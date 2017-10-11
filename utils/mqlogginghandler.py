import pika
from pika import credentials
from datetime import datetime
import logging
import json
import sys

class MQLoggingHandler(logging.Handler):
    """
        handler that send log to rabbitmq, using pika.
    """
    def __init__(self, config):
        logging.Handler.__init__(self)
        self.connection_para = dict(host=config.MQHOST)
        if config.MQPORT:
            self.connection_para['port'] = config.MQPORT
        if config.VIRTUAL_HOST:
            self.connection_para['virtual_host'] = config.VIRTUAL_HOST
        if config.USERNAME and config.PASSWORD:
            self.connection_para['credentials'] = credentials.PlainCredentials(config.USERNAME, config.PASSWORD)
        self.exchange = config.EXCHANGE
        self.exchange_type=config.EXCHANGE_TYPE
        self.connection, self.channel = None, None
        # make sure exchange only declared once.
        self.is_exchange_declared = False
        # init connection.
        self.connect()

    def connect(self):
        """connect to rabbitMq server, using topic exchange"""

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
        """
        clear when closing
        """
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