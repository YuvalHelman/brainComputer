from pathlib import Path


def get_saving_path(user, snap, is_proto=True):
    """ Creates a unique path for each user and snapshot for saving its content.
        arguments are protobuf objects sent from the client or json objects """
    p = Path("/tmp/brainComputer/")
    if p.exists() is False:
        p.mkdir()
    u_id = user.user_id if is_proto else user["user_id"]
    username = user.username if is_proto else user["username"]
    user = str(u_id) + "_" + username
    p = p / user
    if p.exists() is False:
        p.mkdir()
    date = snap.datetime if is_proto else snap["datetime"]
    p = p / str(date)
    if p.exists() is False:
        p.mkdir()
    return str(p)
