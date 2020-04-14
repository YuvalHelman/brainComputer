import json

from brainComputer.db import get_db_handler


class Saver:

    def __init__(self, db_url):
        self.db_url = db_url
        self.handler = get_db_handler(self.db_url)

    def save(self, topic_name, enc_data):
        data = json.loads(enc_data)
        self.handler.save(topic_name, data)
        print("data probe saved to DB")

