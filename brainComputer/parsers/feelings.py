import json


def parse_feelings(json_snap_user):
    snap_user = json.loads(json_snap_user)

    return json.dumps({'user': snap_user["user"],
                       'datetime': snap_user["snapshot"]["datetime"],
                       'feelings': snap_user["snapshot"]["feelings"],
                       }
                      )


parse_feelings.field = 'feelings'



