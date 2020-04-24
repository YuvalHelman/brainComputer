import struct
import gzip
from brainComputer.utils.brain_pb2 import User as PbUser
from brainComputer.utils.brain_pb2 import Snapshot as PbSnapshot


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

    def read_next_snapshot(self):
        pb_snapshot = PbSnapshot()
        if self.read_message_from_file(pb_snapshot, True) == -1:
            print("parsing Snapshot failed")
            return None

        return pb_snapshot

    def read_message_from_file(self, protoObject, is_write=False):
        """ Reads a 'message' from the file given from the hardware specifications """
        try:
            len_raw = self.file.read(4)
            message_length, *_ = struct.unpack('I', len_raw)
            msg_raw = self.file.read(message_length)
            if is_write:
                with open('/tmp/snapshot.bin', 'wb') as f:
                    f.write(msg_raw)
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
