from brainComputer.db.mongo import Mongo
import furl


def get_db_handler(db_url: str):
    """ Get DB from url from what's supported
    """
    url = furl.furl(db_url)
    if url.scheme == 'mongodb':
        return Mongo(db_url)
    else:
        raise Exception("given database scheme is not supported.")
