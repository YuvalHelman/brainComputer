from brainComputer.api.app import app


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

@app.route('/users')
def get_users_list():
    """ Returns the list of all the supported users, including their IDs and names only. """
    # res = self.handler.get_users()
    # return res
    return 'Hello, World!'


@app.route('/users/<int:user_id>')
def get_user_id(user_id):
    """ Returns the specified user's details: ID, name, birthday and gender. """
    # res = self.handler.get_user_id(user_id)
    # return res
    return 'Hello, World!'


@app.route('/users/<int:user_id>/snapshots')
def get_user_snapshot_ids(user_id):
    """ Returns the list of the specified user's snapshot IDs and datetimes only. """
    # res = self.handler.get_user_snapshot_ids(self, user_id)
    # return res
    return 'Hello, World!'


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_user_snapshot_details(user_id, snapshot_id):
    """ Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose). """
    return 'Hello, World!'


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_snapshot_result(user_id, snapshot_id):
    """ Returns the specified snapshot's result. currently supports pose, color-image, depth-image and feelings.
        """
    return 'Hello, World!'
