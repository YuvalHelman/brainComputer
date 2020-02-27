from pathlib import Path
import json
from brainComputer.utils.parser import ParserContext
import pika


def parse_pose(context: ParserContext, snapshot):
    x, y, z = snapshot.translation
    a, b, c, d = snapshot.rotation

    context.save('pose.json',
                 (json.dumps({'translation': {"x": x, "y": y, "z": z},
                              'rotation': {"x": a, "y": b, "z": c, "w": d}
                              })
                  ))


parse_pose.field = 'pose'


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


if __name__ == "__main__":
    queue_name = 'hello'

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
