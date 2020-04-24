from brainComputer.db import get_db_handler
from brainComputer.api.app import app


def run_api_server(host='127.0.0.1', port=5000, database_url='mongodb://127.0.0.1:27017'):
    """ run the API server indefinitely until stopped manually
    :param host: Network IP Address or Hostname to connect to.
    :param port: Network Port to bind
    :param database_url: database to connect to for data fetch
    """
    try:
        app.config.update(db_handler=get_db_handler(database_url))
        app.run(host=host, port=port, use_reloader=False)
    except Exception as e:
        print(f"run_api_server failed: {e}")


if __name__ == '__main__':
    run_api_server()
