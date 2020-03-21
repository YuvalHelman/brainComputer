import pika
import furl

SNAPSHOT_EXCHANGE = 'snapshot-exchange'


def publish_fanout(connection, exchange_name='', data=None):
    ch = connection.channel()

    ch.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    ch.basic_publish(exchange=exchange_name,  # empty string is the default exchange
                     routing_key='',  # the queue name
                     body=data)

    print(f" [x] Sent '{data}'")


def consume_retrieve(rabmq_url, consume_exchange_name, publish_exchange_name='', pre_publish_func=None):
    def parse_callback(ch, method, properties, body):
        if pre_publish_func is not None:
            res = pre_publish_func(body)
        else:
            res = body

        ch.exchange_declare(exchange=publish_exchange_name, exchange_type='fanout')

        ch.basic_publish(exchange=publish_exchange_name,  # empty string is the default exchange
                         routing_key='',  # the queue name
                         body=res)

    publisher_url = furl.furl(rabmq_url)
    con = None
    try:
        con = pika.BlockingConnection(pika.ConnectionParameters(publisher_url.host, publisher_url.port))
        ch = con.channel()

        # Set parameters for consuming snapshots from the server
        ch.exchange_declare(exchange=consume_exchange_name, exchange_type='fanout')
        result = ch.queue_declare(queue='', exclusive=True)
        consume_queue_name = result.method.queue
        ch.queue_bind(exchange=consume_exchange_name, queue=consume_queue_name)

        print(' [*] Consuming from rabbitmq. To exit press CTRL+C')
        ch.basic_qos(prefetch_count=1)
        ch.basic_consume(queue=consume_queue_name, on_message_callback=parse_callback, auto_ack=True)
        ch.start_consuming()
    finally:
        con.close()


if __name__ == "__main__":
    pass
