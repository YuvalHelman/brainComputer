from brainComputer.api.app import app


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

@app.route('/users', methods=['GET'])
def get_users_list():
    """ Returns the list of all the supported users, including their IDs and names only. """
    try:
        user_list = app.config['db_handler'].get_users()
        res = dict()
        for user in user_list:
            res.update({user['user_id']: user['username']})
        return res
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    """ Returns the specified user's details: ID, name, birthday and gender. """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
        return user_dict['user']
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_user_snapshot_ids(user_id):
    """ Returns the list of the specified user's snapshot IDs and datetimes only. """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
        return ", ".join(user_dict['snapshots'].keys())
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>/snapshots/<snapshot_id>', methods=['GET'])  # example: 1575446887339
def get_user_snapshot_details(user_id, snapshot_id):
    """ Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose). """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
        return ", ".join(user_dict['snapshots'][snapshot_id].keys())
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>', methods=['GET'])
def get_snapshot_result(user_id, snapshot_id, result_name):
    """ Returns the specified snapshot's result. currently supports pose, color-image, depth-image and feelings.
        """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
        results = user_dict['snapshots'][snapshot_id].keys()
        return ", ".join('')
    except Exception as e:
        return "operation failed", 404
