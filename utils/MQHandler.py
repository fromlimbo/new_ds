import pika

class MQHandler(object):

    def __init__(self, config=None):
        self.MQ_HOST_ADDRESS=config.MQ_HOST_ADDRESS
        self.MQ_QUEUE_NAME=config.MQ_QUEUE_NAME

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.MQ_HOST_ADDRESS))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.MQ_QUEUE_NAME)

    def sendmessage(self,msg):
        self.channel.basic_publish(exchange='',
                              routing_key=self.MQ_QUEUE_NAME,
                              body='Hello World!')
