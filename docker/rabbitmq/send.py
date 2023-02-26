import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.queue_declare(queue='task_queue', durable=True)


channel.basic_publish(exchange='', 
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                            delivery_mode= pika.spec.PERSISTENT_DELIVERY_MODE
                      )
                    )

print(f" [x] Sent {message}")
connection.close()