import pika
import json


if __name__ == "__main__":  # TODO: erase?
    def callback(ch, method, properties, body):
        parsed_data = body
        print('parsed data: ', parsed_data)
        return json.loads(parsed_data)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Set parameters for consuming snapshots from parsers
    saver_queue = 'saver-queue'
    channel.queue_declare(queue=saver_queue, durable=False)

    channel.basic_consume(queue=saver_queue,
                          on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
