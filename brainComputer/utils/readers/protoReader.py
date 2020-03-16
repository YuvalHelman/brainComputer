import struct
import gzip
from ..brain_pb2 import User as PbUser
from ..brain_pb2 import Snapshot as PbSnapshot


class ReaderProtobuf:
    """ A Reader of Snapshot's objects from the hardware file.
        data read is being converted into the protocol's objects """

    def __init__(self, path):
        self.file = gzip.open(path, 'rb')
        self.user = self.read_user_info()

    def read_user_info(self):
        pb_user = PbUser()
        if self.read_message_from_file(pb_user) == -1:
            print("parsing User failed")
            return None
        return pb_user
        # return User(pb_user.user_id, pb_user.username, pb_user.birthday,
        #             'f' if pb_user.gender == 1 else 'm')

    def read_next_snapshot(self):
        pb_snapshot = PbSnapshot()
        if self.read_message_from_file(pb_snapshot) == -1:
            print("parsing Snapshot failed")
            return None

        return pb_snapshot

    def read_message_from_file(self, protoObject):
        """ Reads a 'message' from the file given from the hardware specifications for exercise 7
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
    pass
