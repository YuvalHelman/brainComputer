from pymongo import MongoClient


class Mongo:
    def __init__(self, url: str):
        client = MongoClient(url)
        db = client['brain_db']
        self.users = db['users']

    def save(self, topic_name: str, data: dict):
        """
            dict(user=snap_user["user"],
                 datetime=snap_user["snapshot"]["datetime"],
                 data=dict(
                     pose=snap_user["snapshot"]["pose"] ))
        """
        try:
            user_id = data['user']['user_id']
        except KeyError as e:
            print(f"db can't save this data format: {e}")
            return
        self.users.find_one({'_id': user_id})

