import pika


def publish_snapshots(connection, message):
    ch = connection.channel()
    snapshots_exchange = 'snapshot_exchange'
    ch.exchange_declare(exchange=snapshots_exchange, exchange_type='fanout')
    ch.basic_publish(exchange=snapshots_exchange,
                     routing_key='',  # ignored for 'fanout' exchanges
                     body=message,
                     properties=pika.BasicProperties(delivery_mode=2, ))  # make message persistent

    print(f" [x] Sent '{message}'")
