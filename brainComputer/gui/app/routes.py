from brainComputer.gui.app import app
from flask import render_template
from collections import OrderedDict


@app.route('/users', methods=['GET'])
def get_users_list():
    """ Returns the list of all the supported users, including their IDs and names only. """
    try:
        user_list = app.config['db_handler'].get_users()
        res = dict()
        for user in user_list:
            res.update({user['user_id']: user['username']})
        res = OrderedDict(res)
        return render_template('users.html', data=res)
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    """ Returns the specified user's details: ID, name, birthday and gender. """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
        return render_template('user_id.html', user=user_dict['user'])
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_user_snapshot_ids(user_id):
    """ Returns the list of the specified user's snapshot IDs and datetimes only. """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
        return render_template('snapshots.html', snapshots=user_dict['snapshots'], user=user_dict['user'])
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>/snapshots/<snapshot_id>', methods=['GET'])  # example: 1575446887339
def get_user_snapshot_details(user_id, snapshot_id):
    """ Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose). """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
      #  import pdb; pdb.set_trace()
        return render_template('snapshots_details.html', snapshots=user_dict['snapshots'], user=user_dict['user'], snapshot_id=snapshot_id, snapid_dict=user_dict['snapshots'][snapshot_id])
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>', methods=['GET'])
def get_snapshot_result(user_id, snapshot_id, result_name):
    """ Returns the specified snapshot's result. currently supports pose, color-image, depth-image and feelings.
        """
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
      #  import pdb; pdb.set_trace()
        return render_template('snapshot_result.html', snapshots=user_dict['snapshots'], user=user_dict['user'], snapshot_id=snapshot_id, snapid_dict=user_dict['snapshots'][snapshot_id], res_dict=user_dict['snapshots'][snapshot_id][result_name] )
    except Exception as e:
        return "operation failed", 404


@app.route('/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>/data', methods=['GET'])
def get_snapshot_result_data(user_id, snapshot_id, result_name):
    """ Returns the specified snapshot's result image data. currently supports color-image, depth-image.
        """
    if result_name != 'color_image' and result_name != 'depth_image':
        raise Exception
    path_key_str = result_name + '_path'
    try:
        user_dict = app.config['db_handler'].get_user_id(user_id)
        image_path = user_dict['snapshots'][snapshot_id][result_name][path_key_str]

        return flask.send_file(image_path, mimetype='image/png')
    except Exception as e:
        return f"operation failed: {e}", 404

