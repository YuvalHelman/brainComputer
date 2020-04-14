from pathlib import Path
import json


def formatted_encoded_one_data(user, datetime, item_key, item_val):
    """ Given a single data probe builds the agreed format for json data transfered in the queue """
    return json.dumps(dict(user=user, snapshots={
                                                datetime: {item_key: item_val}
                                                }
                           ))
