import json
from .utils import formatted_encoded_one_data


def parse_pose(json_snap_user):
    try:
        snap_user = json.loads(json_snap_user)

        ret = formatted_encoded_one_data(user=snap_user["user"], datetime=snap_user["snapshot"]["datetime"],
                                          item_key='pose', item_val=snap_user["snapshot"]["pose"])
        print(f"parser {parse_pose.field} finished")
        return ret
    except Exception as e:
        print(f"parsing pose failed: {e}")
        raise e


parse_pose.field = 'pose'
