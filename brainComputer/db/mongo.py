import pymongo
from pymongo import errors as mongoErrors


class Mongo:
    def __init__(self, url: str):
        client = pymongo.MongoClient(url)
        db = client['brain_db']
        self.users = db['users']

    def save(self, topic_name: str, data: dict):
        """
        { 'user': {'user_id': '...' , '...' }
          'snapshots'= {
                        datetime: {'pose': '...'}
                       }
        }
        """
        db_p = self.users
        try:
            user_id = data['user']['user_id']

            datetime_val = list(data["snapshots"].keys())[0]
            datetime_data_key = list(data["snapshots"][datetime_val].keys())[0]
            datetime_data_val = data["snapshots"][datetime_val][datetime_data_key]
            # import pdb; pdb.set_trace()  # DEBUG

            user = db_p.find_one({'_id': user_id})
            if user is None:
                item = {'_id': data['user']['user_id']}
                item.update(data)
                db_p.insert_one(item)
            else:
                update_key = "snapshots." + datetime_val + "." + datetime_data_key
                db_p.update_one({'_id': user_id}, {'$set': {update_key: datetime_data_val}})

            print(db_p.find_one({'_id': user_id}))  # See this probe in the DB.

        except KeyError as e:
            print(f"db can't save this data format: {e}")
            raise e
        except TypeError as e:
            print(f"unauthorised access to data: {e}")
            raise e
        except mongoErrors.ConnectionFailure as e:
            print(f"Connection to DB failed: {e}")
            raise e
        except mongoErrors.PyMongoError as e:
            print(f"Mongo operation failed: {e}")
            raise e

    def get_users(self):
        try:
            return self.users.find().distinct('_id')
        except mongoErrors.ConnectionFailure as e:
            print(f"Connection to DB failed: {e}")
            raise e
        except mongoErrors.PyMongoError as e:
            print(f"Mongo operation failed: {e}")
            raise e

