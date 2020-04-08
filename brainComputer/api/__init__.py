from flask import Flask

from brainComputer.db import get_db_from_url

app = Flask(__name__)

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
class Api:

    def __init__(self, db_url):
        self.db_url = db_url
        self.handler = get_db_from_url(self.db_url)

    @app.route('/users')
    def get_users(self):
        """ Returns the list of all the supported users, including their IDs and names only. """
        res = self.handler.get_users()
        return res

    @app.route('/users/<int:user_id>')
    def get_user_id(self, user_id):
        """ Returns the specified user's details: ID, name, birthday and gender. """
        res = self.handler.get_user_id(user_id)
        return res

    @app.route('/users/<int:user_id>/snapshots')
    def get_user_snapshot_ids(self, user_id):
        """ Returns the list of the specified user's snapshot IDs and datetimes only. """
        res = self.handler.get_user_snapshot_ids(self, user_id)
        return res

    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
    def get_user_snapshot_details(self, user_id, snapshot_id):
        """ Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose). """
        return 'Hello, World!'

#    @app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
#    def get_users(self, user_id, snapshot_id):
#        """ Returns the specified snapshot's result. currently supports pose, color-image, depth-image and feelings.
#            """
#        return 'Hello, World!'

    def run(self):
        app.run(use_reloader=False)


def run_api_server(host, port, database_url):
    print(f"listen on {host:port} and serve data from {database_url}")
    pass


if __name__ == '__main__':
    a = Api('mongodb://127.0.0.1:27017')
    a.run()

