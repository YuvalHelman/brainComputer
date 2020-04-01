from pathlib import Path
import json


def get_saving_path(user, snap, dir_path: str, is_proto=True):  # TODO: erase ?
    """ Creates a unique path for each user and snapshot for saving its content.
        arguments are protobuf objects from the client-server protocol or json objects """
    snapshots_path = Path("dir_path")
    if snapshots_path.exists() is False:
        snapshots_path.mkdir()
    u_id = user.user_id if is_proto else user["user_id"]
    username = user.username if is_proto else user["username"]
    user = str(u_id) + "_" + username
    snapshots_path = snapshots_path / user
    if snapshots_path.exists() is False:
        snapshots_path.mkdir()
    date = snap.datetime if is_proto else snap["datetime"]
    snapshots_path = snapshots_path / str(date)
    if snapshots_path.exists() is False:
        snapshots_path.mkdir()
    return str(snapshots_path)


def formatted_encoded_one_data(user, datetime, item_key, item_val):
    """ Given a single data probe builds the agreed format for json data transfered in the queue """
    return json.dumps(dict(user=user, snapshots={
                                                datetime: {item_key: item_val}
                                                }
                           ))
