import struct
import gzip
import click
from binary_operations import read_from_binary_file
from protocol import Snapshot, User
from brain_pb2 import User as ProtoUser
from brain_pb2 import Snapshot as ProtoSnapshot


class ReaderProtobuf:
    """ A Reader of Snapshot's objects using the protobuf module """

    def __init__(self, path):
        self.file = gzip.open(path, 'rb')
        self.user = self.read_user_info()

    def read_user_info(self):
        proto_user = ProtoUser()
        if self.read_message_from_protobuf(proto_user) == -1:
            print("parsing User failed")
            return None
        return User(proto_user.user_id, proto_user.username, proto_user.birthday,
                    'f' if proto_user.gender == 1 else 'm')

    def read_next_snapshot(self):
        proto_snapshot = ProtoSnapshot()
        if self.read_message_from_protobuf(proto_snapshot) == -1:
            print("parsing User failed")
            return None

        return Snapshot(proto_snapshot.datetime,
                        (proto_snapshot.pose.translation.x, proto_snapshot.pose.translation.y,
                         proto_snapshot.pose.translation.z),
                        (proto_snapshot.pose.rotation.x, proto_snapshot.pose.rotation.y,
                         proto_snapshot.pose.rotation.z, proto_snapshot.pose.rotation.w),
                        (proto_snapshot.color_image.width, proto_snapshot.color_image.height,
                         proto_snapshot.color_image.data),
                        (proto_snapshot.depth_image.width, proto_snapshot.depth_image.height,
                         proto_snapshot.depth_image.data),
                        (proto_snapshot.feelings.hunger, proto_snapshot.feelings.thirst,
                         proto_snapshot.feelings.exhaustion, proto_snapshot.feelings.happiness))

    def read_message_from_protobuf(self, protoObject):
        """ Reads a 'message' which could be the user's info, or a snapshot with the appropriate
            hardware specifications for exercise 7
        :return:
        """
        try:
            UINT_32_LEN_IN_BYTES = 4
            len_raw = self.file.read(UINT_32_LEN_IN_BYTES)
            message_length, *_ = struct.unpack('I', len_raw)
            msg_raw = self.file.read(message_length)
            protoObject.ParseFromString(msg_raw)
            return 0
        except Exception as e:
            return -1

    def __next__(self):
        return self.read_next_snapshot()

    def __iter__(self):
        return self

    def __repr__(self):
        return f"A reader Object for the file {self.file}"





if __name__ == '__main__':
    r = ReaderProtobuf('../../../dataFiles/sample.mind')
    print(r.user)
    for snapshot in r:
        print(snapshot)
    # pass
