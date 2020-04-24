import json

from brainComputer.db import get_db_handler


class Saver:
    """ A class to handle saving to the DB and getting results from the message queue
        connects to a database, accepts a topic name and some data, as consumed from the message queue
    """
    def __init__(self, db_url):
        self.db_url = db_url
        self.handler = get_db_handler(self.db_url)

    def save(self, topic_name, enc_data):
        """ saves a dict of type 'user-snapshot' in the implemented DB.
        :param topic_name: name of the probe to be saved (unusable in this version)
        :param enc_data: a json object of the appropriate structure fetched from the message queue.
        """
        try:
            data = json.loads(enc_data)
            self.handler.save(topic_name, data)
            print("Save to db success")
        except Exception as e:
            print("Saving to DB failed")
            print(e)
