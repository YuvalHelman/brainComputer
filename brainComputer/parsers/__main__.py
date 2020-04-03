import click
import furl

import brainComputer.utils.rabbitmq as rabmq
from . import run_parser
from .utils import get_parser_function


@click.group()
def cli():
    pass


@cli.command(name='parse')
@click.argument('parser_name')
@click.argument('data_path')
def parse_cli(parser_name, data_path):
    """  accepts a parser name and some raw data and prints the result.
         This way of invocation runs the parser exactly once            """
    with open(data_path, 'r') as f:
        data = f.read()

    run_parser(parser_name, data)


@cli.command(name='run-parser')
@click.argument('parser_name')
@click.argument('publish_url')
def run_parser_cli(parser_name, publish_url):
    """ running the parser as a service, which works with a message queue indefinitely """
    publisher_url = furl.furl(publish_url)

    try:
        parser_func = get_parser_function(parser_name)
    except KeyError:
        print(f"{parser_name} isn't a valid parser name")
        return 1

    if publisher_url.scheme == 'rabbitmq':
        rabmq.consume_retrieve(publisher_url=publisher_url, consume_exchange_name=rabmq.SNAPSHOT_EXCHANGE,
                               publish_exchange_name=parser_name, pre_publish_func=parser_func)


if __name__ == "__main__":
    cli()
