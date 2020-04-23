import os
import json
import datetime


def user_snap_pb_to_json(pb_user, pb_snapshot, data_path):
    """ Converts User and Snapshots between protobuf objects to json. """
    user_dict = pbuser_to_dict(pb_user)
    snap_dict = pbsnapshot_to_dict(pb_snapshot, pb_user, data_path)
    return json.dumps(dict(user=user_dict, snapshot=snap_dict))


def pbuser_to_dict(pb_user):
    """ Converts the user object from binary protobuf protocol to json with interpretation of strings """
    gender = 'o'
    if pb_user.gender == 0:
        gender = 'm'
    elif pb_user.gender == 1:
        gender = 'f'
    birthday = datetime.datetime.fromtimestamp(pb_user.birthday)

    return dict(
        user_id=pb_user.user_id,
        username=pb_user.username,
        birthday=birthday.strftime("%m/%d/%Y, %H:%M:%S"),
        gender=gender
    )


def get_data_dir(data_path, user_id, username, datetime):
    """ Returns a string that conforms to the valid path structure for saving a data file. """
    return str(data_path) + str(user_id) + "_" + str(username) + "/" + str(datetime) + '/'  # /42_Ron Dan/15423/


def pbsnapshot_to_dict(pb_snapshot, pb_user, data_path):
    """ Converts the snapshot object from binary protobuf protocol to json with interpretation of strings.
        Large binary files are saved to disk and being converted from data to absolute files paths on disk.
     """
    try:
        p = get_data_dir(data_path, pb_user.user_id, pb_user.username, pb_snapshot.datetime)
        os.makedirs(p, exist_ok=True)

        color_data_p = p + 'color_data'
        color_image_p = p + 'color_image.png'
        depth_data_p = p + 'depth_data'
        depth_image_p = p + 'depth_image.png'

        with open(color_data_p, 'wb') as f:
            f.write(pb_snapshot.color_image.data)

        with open(depth_data_p, 'w') as f:
            f.write('\n'.join(str(num) for num in pb_snapshot.depth_image.data))
    except Exception as e:
        print(f"writing color or depth data failed: {e}")
        raise e

    return dict(
        datetime=pb_snapshot.datetime,
        pose=dict(
            translation=dict(
                x=pb_snapshot.pose.translation.x,
                y=pb_snapshot.pose.translation.y,
                z=pb_snapshot.pose.translation.z,
            ),
            rotation=dict(
                x=pb_snapshot.pose.rotation.x,
                y=pb_snapshot.pose.rotation.y,
                z=pb_snapshot.pose.rotation.z,
                w=pb_snapshot.pose.rotation.w,
            ),
        ),
        color_image=dict(
            width=pb_snapshot.color_image.width,
            height=pb_snapshot.color_image.height,
            data_path=str(color_data_p),
            color_image_path=str(color_image_p)
        ),
        depth_image=dict(
            width=pb_snapshot.depth_image.width,
            height=pb_snapshot.depth_image.height,
            data_path=str(depth_data_p),
            depth_image_path=str(depth_image_p),

        ),
        feelings=dict(
            hunger=pb_snapshot.feelings.hunger, thirst=pb_snapshot.feelings.thirst,
            exhaustion=pb_snapshot.feelings.exhaustion, happiness=pb_snapshot.feelings.happiness
        )
    )
