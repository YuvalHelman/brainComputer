import furl

from brainComputer.db import Mongo


class Saver:

    def __init__(self, db_url):
        self.db_url = db_url
        self.handler = get_db_from_url(self.db_url)

    def save(self, topic_name, data):
        self.handler.save(topic_name, data)


def get_db_from_url(db_url: str):
    """ Get DB from url from what's supported
    """
    url = furl.furl(db_url)
    if url.scheme == 'mongodb':
        return Mongo(db_url)
    else:
        raise Exception("given database scheme is not supported.")
