import pytest
from brainComputer.utils.protocol import User, Snapshot, Config


@pytest.fixture
def example_snapshot():
    return Snapshot()


def example_user():
    return User(1, "yuval", )


def test_a():
    pass
