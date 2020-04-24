from brainComputer.db import get_db_handler
from brainComputer.gui.app import app


def run_server(host='127.0.0.1', port: int = 8080, database_url='mongodb://127.0.0.1:27017'):
    """ run the GUI server indefinitely until stopped manually
    :param host: Network IP Address or Hostname to connect to.
    :param port: Network Port to bind
    :param database_url: database to connect to for data fetch
    """
    try:
        db_handler = get_db_handler(database_url)
        app.config.update(db_handler=db_handler)
        app.run(host=host, port=port, use_reloader=False)
    except Exception as e:
        print(f"run_server failed: {e}")


if __name__ == '__main__':
    run_server()
