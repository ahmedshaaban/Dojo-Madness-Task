# -*-  coding: utf-8 -*-
import logging
import pika
import json
from pika.adapters import TornadoConnection

pika.log = logging.getLogger(__name__)

class PikaClient(object):
    INPUT_QUEUE_NAME = 'in_queue'

    def __init__(self, io_loop, db):
        self.db = db
        self.io_loop = io_loop
        self.connected = False
        self.connecting = False
        self.connection = None
        self.in_channel = None
        self.websockets = {}
        self.connect()

    def connect(self):
        if self.connecting:
            return
        self.connecting = True

        cred = pika.PlainCredentials('guest', 'guest')
        param = pika.ConnectionParameters(
            host='rabbitmq', port=5672, virtual_host='/', credentials=cred)

        self.connection = TornadoConnection(
            param, on_open_callback=self.on_connected)

    def on_connected(self, connection):
        self.connected = True
        self.connection = connection
        self.in_channel = self.connection.channel(self.on_conn_open)

    def on_conn_open(self, channel):
        self.in_channel.exchange_declare(
            exchange='tornado_input', exchange_type='fanout')
        channel.queue_declare(
            callback=self.on_input_queue_declare, queue=self.INPUT_QUEUE_NAME)
        self.in_channel.queue_bind(
            callback=None,
            exchange='tornado_input',
            queue=self.INPUT_QUEUE_NAME,
            routing_key="#")

    def on_input_queue_declare(self, queue):
        self.in_channel.basic_consume(
            self.on_message, queue=self.INPUT_QUEUE_NAME)

    def on_message(self, channel, method, header, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        document = json.loads(body)
        document['_id'] = method.routing_key.split(".")[1]
        collection = method.routing_key.split(".")[0]
        self.db[collection].insert_one(document, callback=None)
        for sess in self.websockets:    
            self.websockets[sess].write_message(body)

    def register_websocket(self, sess_id, ws):
        self.websockets[sess_id] = ws

    def unregister_websocket(self, sess_id):
        del self.websockets[sess_id]