

if __name__ == "__main__":
    def callback(ch, method, properties, body):
        parsed_data = body
        print('parsed data: ', parsed_data)
        saver_queue = 'saver-queue'



    queue_name = 'task_queue'

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()