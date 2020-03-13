from brainComputer.utils.brain_pb2 import Snapshot as PbSnapshot
from brainComputer.utils.brain_pb2 import User as PbUser


def convert_to_protocol_user(hw_user):
    """ Converts between the user in the format of the Hardware into the format of the protocol.
        Current implementation is the same in both """
    user = PbUser()
    user.user_id = hw_user.user_id
    user.username = hw_user.username
    user.birthday = hw_user.birthday
    user.gender = hw_user.gender
    return user


def convert_to_protocol_snapshot(hw_snap):
    """ Converts between the snapshot in the format of the Hardware into the format of the protocol.
        Current implementation is the same in both """
    snap = PbSnapshot()
    snap.CopyFrom(hw_snap)
    return snap
