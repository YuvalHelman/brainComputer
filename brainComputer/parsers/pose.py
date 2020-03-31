import json
from brainComputer.utils import formatted_encoded_one_data


def parse_pose(json_snap_user):
    try:
        snap_user = json.loads(json_snap_user)

        return formatted_encoded_one_data(user=snap_user["user"], datetime=snap_user["snapshot"]["datetime"],
                                          item_key='pose', item_val=snap_user["snapshot"]["pose"])
    except Exception as e:
        print(f"parsing pose failed: {e}")
        raise e


parse_pose.field = 'pose'

if __name__ == '__main__':
    pass
