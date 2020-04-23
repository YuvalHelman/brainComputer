import json

from brainComputer.saver import Saver


def test_saver_sanity(capsys, db_mock_mongo):
    s = Saver('mongodb://127.0.0.1:27017')
    data = json.dumps({'_id': 1, })
    s.save('pose', data)
    captured = capsys.readouterr()
    assert "Save to db success" in captured.out
    assert "Saving to DB failed" not in captured.out
