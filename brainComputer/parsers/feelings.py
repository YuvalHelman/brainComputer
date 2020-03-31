import json


def parse_feelings(json_snap_user):
    try:
        snap_user = json.loads(json_snap_user)

        return json.dumps(
            dict(user=snap_user["user"],
                 snapshots=[
                     dict(datetime=snap_user["snapshot"]["datetime"], feelings=snap_user["snapshot"]["feelings"], ),
                 ]
            )
        )
    except Exception as e:
        print(f"parsing feelings failed: {e}")
        raise e


parse_feelings.field = 'feelings'
