from pymongo import MongoClient


class Mongo:
    def __init__(self, url: str):
        client = MongoClient(url)
        db = client['brain_db']
        collection = db['users']

    def save(self, topic_name: str, data: dict):
        pass
