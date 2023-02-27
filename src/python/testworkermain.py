import rabbitmq.rabbitclasses as rabbitclasses
import yaml

def print_msg(msg):
    print(msg)

def main():
    # parse yaml file into object from /usr/etc/config/worker.yaml using the yaml module

    with open("/usr/etc/config/worker.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # create rabbitmq publisher manager
    rabbitmq_host = config["rabbitmq_host"]
    rabbitmq_port = config["rabbitmq_port"]
    rabbitmq_username = config["rabbitmq_user"]
    rabbitmq_password = config["rabbitmq_pass"]

    rabbitmq_consumer_provider = rabbitclasses.RabbitMQConsumerProvider(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password)

    rabbitmq_consumer = rabbitmq_consumer_provider.new_consumer("", "test_queue")
    rabbitmq_consumer.connect()

    rabbitmq_consumer.consume(print_msg)
