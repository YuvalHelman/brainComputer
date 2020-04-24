from brainComputer.db.mongo import Mongo
import furl


def get_db_handler(db_url: str):
    """ Returns the DB handler object from a url from what's supported.
    :param db_url: the url connection info the the DB (Example: mongodb://127.0.0.1:27017)
    """
    url = furl.furl(db_url)
    if url.scheme == 'mongodb':
        return Mongo(db_url)
    else:
        raise Exception("given database scheme is not supported.")
