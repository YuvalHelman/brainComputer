import json


def parse_pose(json_snap_user):
    try:
        snap_user = json.loads(json_snap_user)

        return json.dumps(
            dict(user=snap_user["user"],
                 snapshots=[
                     dict(datetime=snap_user["snapshot"]["datetime"], pose=snap_user["snapshot"]["pose"],),
                 ]
            )
        )
    except Exception as e:
        print(f"parsing pose failed: {e}")
        raise e


parse_pose.field = 'pose'

if __name__ == '__main__':
    pass
