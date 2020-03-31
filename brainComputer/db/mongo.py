from pymongo import MongoClient
import json

from brainComputer.utils import formatted_encoded_one_data


class Mongo:
    def __init__(self, url: str):
        client = MongoClient(url)
        db = client['brain_db']
        self.users = db['users']

    def save(self, topic_name: str, data: dict):
        """
        { 'user': {'user_id': '...' , '...' }
          'snapshots'= [
                 {'datetime': '..',
                  'pose': '...'
                 }
                ]
}
        """
        try:
            user_id = data['user']['user_id']

            user = self.users.find_one({'_id': user_id})
            extracted_new_key = data["snapshots"][0].keys()
            extracted_new_key.remove('datetime')
            extracted_new_key = extracted_new_key[0]
            probe = None
            if user is None:
                # TODO: if user doesn't exist, create a formatted json with '_id: user_id' and push it in
                json_to_insert = formatted_encoded_one_data(data['user']['user_id'], data["snapshots"][0]["datetime"],
                                                  extracted_new_key, data["snapshots"][0][extracted_new_key])
                probe = json.loads(json_to_insert)
                probe['_id'] = data['user']['user_id']
                # TODO: Insert the probe into the DB

            else:
                # TODO: if the user exists, update his
                pass
        except KeyError as e:
            print(f"db can't save this data format: {e}")
            return

    @classmethod
    def convert_to_save_format(cls, data: dict):
        pass