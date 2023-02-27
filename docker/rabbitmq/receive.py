import pika
import sys
import os
import time
def main():
    
    url = os.environ.get('CLOUDAMQP_URL','amqp://guest:guest@localhost/%2f')
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='pdfprocess') # Declare a queue
    
    def callback(ch, method, properties, body):
        
        print(f" [x] Received {body.decode()}" )
        sleep_time = 10
        print(f"Sleep for {sleep_time} to simulate work")
        time.sleep(sleep_time)
        print(f" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='pdfprocess',
                        on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)