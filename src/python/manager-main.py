import rabbitmq.rabbitclasses as rabbitclasses
import rabbitmq.dataqueuer as dataqueuer
from rabbitmq.testcommand import Command, parse_from_json
import yaml
import time

def main():
    # parse yaml file into object from /usr/etc/config/worker.yaml using the yaml module

    with open("/usr/etc/config/manager.yaml", "r") as f:
        config = yaml.safe_load(f)
        f.close()
    
    # create rabbitmq publisher manager
    rabbitmq_host = config["rabbitmq_host"]
    rabbitmq_port = config["rabbitmq_port"]
    rabbitmq_username = config["rabbitmq_user"]
    rabbitmq_password = config["rabbitmq_pass"]

    rabbitmq_provider = rabbitclasses.RabbitMQProvider(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password)

    rabbitmq_publisher = rabbitmq_provider.new_publisher("test", "test_queue")
    rabbitmq_publisher.connect()

    data_queuer = dataqueuer.DataQueuer(rabbitmq_publisher)
    i = 1
    while i < 30:
        test_queue_item = Command("test", {"test": i})
        queue_item = dataqueuer.QueueItem(test_queue_item)
        data_queuer.queue_item(queue_item)
        i += 1

if __name__ == "__main__":
    main()
