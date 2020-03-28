import click
import furl

import brainComputer.utils.rabbitmq as rabmq
from . import Saver


@click.group()
def cli():
    pass


@cli.command(name='save')
@click.option('--database', '-d', default='mongodb://127.0.0.1:27017', help="url of the database")
@click.argument('topic_name')
@click.argument('data')
def save_cli(database, topic_name, data):
    """  accepts a parser name and a path to some raw data and prints the result.
         This way of invocation runs the parser exactly once """
    s = Saver(database)
    s.save(topic_name, data)


@cli.command(name='run-saver')
@click.argument('db_url')
@click.argument('publish_url')
def run_saver_cli(db_url, publish_url):
    """ running the parser as a service, which works with a message queue indefinitely """
    publisher_url = furl.furl(publish_url)

    # TODO

    # if publisher_url.scheme == 'rabbitmq':
    #     rabmq.consume_topic(publisher_url=publisher_url, topic_exchange_name=rabmq.SNAPSHOT_EXCHANGE,
    #                            publish_exchange_name=parser_name, pre_publish_func=parser_func)


if __name__ == "__main__":
    cli()
