import click
import furl

import brainComputer.utils.rabbitmq as rabmq
from brainComputer.parsers import load_parsers
from . import Saver


@click.group()
def cli():
    pass


@cli.command(name='save')
@click.option('--database', '-d', default='mongodb://127.0.0.1:27017', help="url of the database")
@click.argument('topic_name')
@click.argument('data_path')
def save_cli(database, topic_name, data_path):
    """  accepts a parser name and a path to some raw data and prints the result.
         This way of invocation runs the parser exactly once """
    with open(data_path, 'r') as f:
        data = f.read()

    s = Saver(database)
    s.save(topic_name, data)


@cli.command(name='run-saver')
@click.argument('db_url')
@click.argument('publish_url')
def run_saver_cli(db_url, publish_url):
    """ running the parser as a service, which works with a message queue indefinitely """
    publisher_url = furl.furl(publish_url)

    s = Saver(db_url)

    if publisher_url.scheme == 'rabbitmq':
        rabmq.consume_topics(publisher_url=publisher_url, topics_dict=load_parsers(), callback_func=s.save)


if __name__ == "__main__":
    cli()
