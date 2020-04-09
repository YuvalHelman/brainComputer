import click
import requests


@click.group()
def cli():
    pass


@cli.command(name='get-users')
@click.option('--host', '-h', default='127.0.0.1', help="url of the server")
@click.option('--port', '-p', default='5000', help="url of the server")
def get_users_cli(host, port):
    r = requests.get(f'http://{host}:{port}/users')
    print(r.text)


@cli.command(name='get-user')
@click.option('--host', '-h', default='127.0.0.1', help="url of the server")
@click.option('--port', '-p', default='5000', help="url of the server")
@click.argument('user_id', type=int)
def get_user_cli(host, port, user_id):
    r = requests.get(f'http://{host}:{port}/users/{user_id}')
    print(r.text)


@cli.command(name='get-snapshots')
@click.option('--host', '-h', default='127.0.0.1', help="url of the server")
@click.option('--port', '-p', default='5000', help="url of the server")
@click.argument('user_id', type=int)
def get_snapshots_cli(host, port, user_id):
    r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
    print(r.text)


@cli.command(name='get-snapshot')
@click.option('--host', '-h', default='127.0.0.1', help="url of the server")
@click.option('--port', '-p', default='5000', help="url of the server")
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def get_snapshot_cli(host, port, user_id, snapshot_id):
    r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}')
    print(r.text)


@cli.command(name='get-result')
@click.option('--host', '-h', default='127.0.0.1', help="url of the server")
@click.option('--port', '-p', default='5000', help="url of the server")
@click.option('--save', '-s', help="A path for saving the result")
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('result_name')
def get_result_cli(host, port, save, user_id, snapshot_id, result_name):
    r = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}')
    print(r.text)

    try:
        if save is not None:
            with open(save, 'w') as f:
                f.write(r.text)
    except Exception as e:
        print(f"failed writing to file {save}: {e}")


if __name__ == "__main__":
    cli()
