import pika
import furl


def publish_snapshots(connection, exchange_name='', exchange_type='fanout', data=None):
    ch = connection.channel()

    ch.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    ch.basic_publish(exchange=exchange_name,  # empty string is the default exchange
                     routing_key='',  # the queue name
                     body=data,
                     properties=pika.BasicProperties(delivery_mode=2, ))  # make message persistent

    print(f" [x] Sent '{data}'")


def consume_retrieve(rabmq_url, is_retrieve, consume_exchange_name, consume_exchange_type,
                     publish_exchange_name='', pre_publish_func=None):
    def parse_callback(ch, method, properties, body):
        retriever_func(ch, method, properties, body,
                       publish_exchange_name, pre_publish_func)

    publisher_url = furl.furl(rabmq_url)
    con = None
    try:
        con = pika.BlockingConnection(pika.ConnectionParameters(publisher_url.host, publisher_url.port))
        ch = con.channel()

        # Set parameters for consuming snapshots from the server
        ch.exchange_declare(exchange=consume_exchange_name, exchange_type=consume_exchange_type)
        result = ch.queue_declare(queue='', exclusive=True)
        consume_queue_name = result.method.queue
        ch.queue_bind(exchange=consume_exchange_name, queue=consume_queue_name)

        print(' [*] Consuming from rabbitmq. To exit press CTRL+C')
        ch.basic_qos(prefetch_count=1)
        if is_retrieve is True:
            ch.basic_consume(queue=consume_queue_name, on_message_callback=parse_callback, auto_ack=True)
        else:
            ch.basic_consume(queue=consume_queue_name, on_message_callback=parse_callback, auto_ack=True)
        ch.start_consuming()
    finally:
        con.close()


def retriever_func(ch, method, properties, body,
                   publish_queue_name='', pre_publish_func=None):
    if pre_publish_func is not None:
        res = pre_publish_func(body)
    else:
        res = body

    # TODO: this..
    ch.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    ch.queue_declare(queue=publish_queue_name, durable=False)
    ch.basic_publish(exchange='',
                     routing_key=publish_queue_name,
                     body=res)


if __name__ == "__main__":
    pass
