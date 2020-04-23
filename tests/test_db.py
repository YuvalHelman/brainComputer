import pytest

from brainComputer.db import get_db_handler


@pytest.mark.skip(reason="Mongo has to be up for this to work. Should be only run manually")
def test_save_to_mongo(json_db_document_user43):
    """  """
    mong = get_db_handler('mongodb://127.0.0.1:27017')

    mong.insert_doc(json_db_document_user43)

    db_res = mong.get_user_id(43)

    assert db_res == json_db_document_user43
