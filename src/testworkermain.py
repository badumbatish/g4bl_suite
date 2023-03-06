import rabbitmq.rabbitclasses as rabbitclasses
import rabbitmq.dataqueuer as dataqueuer
from rabbitmq.testcommand import Command, parse_from_json
import time
import yaml

def main():
    # parse yaml file into object from /usr/etc/config/worker.yaml using the yaml module

    with open("/usr/etc/config/worker.yaml", "r") as f:
        config = yaml.safe_load(f)
        f.close()
    
    # create rabbitmq publisher manager
    rabbitmq_host = config["rabbitmq_host"]
    rabbitmq_port = config["rabbitmq_port"]
    rabbitmq_username = config["rabbitmq_user"]
    rabbitmq_password = config["rabbitmq_pass"]

    rabbitmq_provider = rabbitclasses.RabbitMQProvider(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password)

    rabbitmq_consumer = rabbitmq_provider.new_consumer("test", "test_queue")
    rabbitmq_consumer.connect()

    def callback(ch, method, properties, body):
      item = dataqueuer.queue_item_from_json(body)
      cmd = parse_from_json(item.data)
      if cmd:
          cmd.execute()
    time.sleep(5)
    rabbitmq_consumer.consume(callback)
    
  
if __name__ == "__main__":
    main()
