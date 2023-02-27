import pika

# Provides the initial params (host, port, user, password) to create a new RabbitMQPublisher without having to pass them every time
class RabbitMQPublisherProvider:
    # host - RabbitMQ server IP
    # port - RabbitMQ server port
    # user - RabbitMQ server username
    # password - RabbitMQ server password
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    # exchange - RabbitMQ exchange name
    # queue_name - RabbitMQ queue name
    def new_publisher(self, exchange, queue_name):
        return RabbitMQPublisher(self.host, self.port, self.user, self.password, exchange, queue_name)

# handles sending messages to the RabbitMQ server, exchange, and queue define defined by the params
class RabbitMQPublisher:
    def __init__(self, host, port, user, password, exchange, queue_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.exchange = exchange
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    # initialize connection to RabbitMQ server
    def connect(self):
        # cred gen
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

    # send a message to the RabbitMQ server, blocks execution until the message is sent/received
    def publish(self, message):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue_name, body=message)

    def close(self):
        self.connection.close()

# Provides the initial params (host, port, user, password) to create a new RabbitMQConsumer without having to pass them every time
class RabbitMQConsumerProvider:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def new_consumer(self, exchange, queue_name):
        return RabbitMQConsumer(self.host, self.port, self.user, self.password, exchange, queue_name)
    
class RabbitMQConsumer:
    def __init__(self, host, port, user, password, exchange, queue_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.exchange = exchange
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=self.queue_name)

    def consume(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()