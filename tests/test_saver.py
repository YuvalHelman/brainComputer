import pytest

from brainComputer.saver import Saver


def test_saver_sanity():
    s = Saver(database)
    s.save(topic_name, data)
