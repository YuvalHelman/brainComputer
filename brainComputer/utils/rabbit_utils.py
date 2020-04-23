import typing
import furl
import pika

SNAPSHOT_EXCHANGE = 'snapshot-exchange'


def publish_fanout(connection, exchange_name='', data=None):
    """ publish data to a dedicated exchange in rabbitmq"""
    try:
        ch = connection.channel()
        ch.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        ch.basic_publish(exchange=exchange_name,  # empty string is the default exchange
                         routing_key='',  # the queue name
                         body=data)
    except Exception as e:
        print(f"connecting to RabbitMq failed: {e}")


def consume_retrieve(publisher_url: furl.furl, consume_exchange_name, publish_exchange_name='', pre_publish_func=None):
    """ Consume from a single exchange with a dedicated queue. make a precomputation before with pre_publish_func
        before sending it back to the queue.
        used for the parsers module that consumes messages from the server parse them, and send them to be saved """

    def callback(ch, body, pre_publish_func):
        if pre_publish_func is not None:
            res = pre_publish_func(body)
        else:
            res = body

        ch.exchange_declare(exchange=publish_exchange_name, exchange_type='fanout')

        ch.basic_publish(exchange=publish_exchange_name,  # empty string is the default exchange
                         routing_key='',  # the queue name
                         body=res)

    con = None
    try:
        con = pika.BlockingConnection(pika.ConnectionParameters(publisher_url.host, publisher_url.port))
        ch = con.channel()

        ch.exchange_declare(exchange=consume_exchange_name, exchange_type='fanout')
        result = ch.queue_declare(queue='', exclusive=True)
        consume_queue_name = result.method.queue
        ch.queue_bind(exchange=consume_exchange_name, queue=consume_queue_name)

        print(' [*] Consuming from rabbitmq. To exit press CTRL+C')
        ch.basic_qos(prefetch_count=1)
        ch.basic_consume(queue=consume_queue_name,
                         on_message_callback=lambda ch, method, properties, body: callback(ch, body, pre_publish_func),
                         auto_ack=True)
        ch.start_consuming()
    except Exception as e:
        print(f"connecting to RabbitMq failed: {e}")
    finally:
        if con is not None:
            con.close()


def consume_topics(publisher_url: furl.furl, topics_dict: typing.Dict[str, typing.Callable], callback_func):
    """ Consume from various exchanges with a queue for each one and a function for each one.
        used for the saver module that consumes multiple parsers """
    con = None
    try:
        con = pika.BlockingConnection(pika.ConnectionParameters(publisher_url.host, publisher_url.port))
        ch = con.channel()
        ch.basic_qos(prefetch_count=1)

        for topic_name, func in topics_dict.items():
            ch.exchange_declare(exchange=topic_name, exchange_type='fanout')
            result = ch.queue_declare(queue='', exclusive=True)
            consume_queue_name = result.method.queue
            ch.queue_bind(exchange=topic_name, queue=consume_queue_name)
            ch.basic_consume(queue=consume_queue_name,
                             on_message_callback=lambda ch, method, properties, body: callback_func(topic_name, body),
                             auto_ack=True)
        print(' [*] Consuming from rabbitmq. To exit press CTRL+C')
        ch.start_consuming()
    except Exception as e:
        print(f"connecting to RabbitMq failed: {e}")
    finally:
        if con is not None:
            con.close()
