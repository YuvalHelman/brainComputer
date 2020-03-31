import json
from brainComputer.utils import formatted_encoded_one_data


def parse_feelings(json_snap_user):
    try:
        snap_user = json.loads(json_snap_user)

        return formatted_encoded_one_data(user=snap_user["user"], datetime=snap_user["snapshot"]["datetime"],
                                          item_key='feelings', item_val=snap_user["snapshot"]["feelings"])
    except Exception as e:
        print(f"parsing feelings failed: {e}")
        raise e


parse_feelings.field = 'feelings'
