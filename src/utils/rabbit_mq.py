import pika
import os
import logging

from urllib.parse import urlparse
import ssl

logger = logging.getLogger(__name__)

class RabbitMQ:
    def __init__(self):
        self.user = os.getenv('RABBITMQ_USER', os.getenv('RABBITMQ_USERNAME', 'user'))
        self.password = os.getenv('RABBITMQ_PASSWORD', 'password')
        raw_host = os.getenv('RABBITMQ_HOST', 'localhost')
        
        self.ssl_options = None
        if "://" in raw_host:
            parsed = urlparse(raw_host)
            self.host = parsed.hostname or 'localhost'
            # If scheme is https or amqps, configure SSL
            if parsed.scheme in ("https", "amqps"):
                self.ssl_options = pika.SSLOptions(context=ssl.create_default_context())
                self.port = parsed.port if parsed.port else 5671
            else:
                self.port = parsed.port if parsed.port else 5672
        else:
            self.host = raw_host
            self.port = int(os.getenv('RABBITMQ_PORT', 5672))
            
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host, 
            port=self.port, 
            credentials=credentials,
            ssl_options=self.ssl_options
        )
        try:
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logger.info(f"Successfully established connection to RabbitMQ at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to establish connection to RabbitMQ at {self.host}:{self.port}: {e}")
            raise

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume(self, queue_name, callback):
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def publish(self, queue_name, message):
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   ))
