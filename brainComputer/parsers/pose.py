from pathlib import Path
import json
import pika


def parse_pose(json_snap_user):
    try:
        snap_user = json.loads(json_snap_user)

        return json.dumps({'user': snap_user["user"],
                           'datetime': snap_user["snapshot"]["datetime"],
                           'pose': snap_user["snapshot"]["pose"],
                           }
                          )
    except Exception as e:
        print(f"parsing pose failed: {e}")
        raise e


parse_pose.field = 'pose'

if __name__ == "__main__":
    def parse_retrieve(ch, method, properties, body):
        # parsed_data = parse_pose(None, json.loads(body))
        parsed_data = body
        print('parsed data: ', parsed_data)

        saver_queue = 'saver-queue'
        ch.queue_declare(queue=saver_queue, durable=False)
        ch.basic_publish(exchange='',
                         routing_key=saver_queue,
                         # body=json.dumps(parsed_data))  # TODO: add this back after testing
                         body=parsed_data)


    # Connect to rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = connection.channel()

    # Set parameters for consuming snapshots from the server
    snapshots_exchange = 'snapshot_exchange'
    ch.exchange_declare(exchange=snapshots_exchange, exchange_type='fanout')
    result = ch.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    ch.queue_bind(exchange=snapshots_exchange, queue=queue_name)

    # Set parameters for publishing back to the queue into the saver queue
    saver_queue = 'saver-queue'
    # TODO: each parser should have a different queue (not sure if same Exchange..)
    ch.queue_declare(queue=saver_queue, durable=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    ch.basic_consume(queue=queue_name, on_message_callback=parse_retrieve, auto_ack=True)
    ch.start_consuming()
