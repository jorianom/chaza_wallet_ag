#!/usr/bin/env python
import pika

# Define los parámetros de conexión a RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

class Producer:
    connection = None
    channel = None
    RABBITMQ_QUEUE = ''

    def connect(self, queue):  # 'recharges'
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
        self.channel = self.connection.channel()
        self.RABBITMQ_QUEUE = queue
        self.channel.queue_declare(queue=self.RABBITMQ_QUEUE, durable=True)
        # self.channel.basic_publish(exchange='',
        #                            routing_key='hello',
        #                            body='Hello World!')
        # print(" [x] Sent 'Hello World!'")

    def publish(self, request_json):
        self.channel.basic_publish(
            exchange='', routing_key=self.RABBITMQ_QUEUE, body=request_json)

        self.connection.close()