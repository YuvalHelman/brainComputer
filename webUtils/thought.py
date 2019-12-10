from datetime import datetime
import struct


class Thought:

    def __init__(self, user_id, timestamp: datetime, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        timeString = self.timestamp.strftime('[%Y-%m-%d %H:%M:%S]')  # YYYY-mm-dd HH:MM:SS
        return f"{timeString} user {self.user_id}: {self.thought}"

    def __eq__(self, other):
        """ return true only for other thought instances with similar attributes. """
        if id(self) == id(other):
            return True
        if not isinstance(other, Thought):
            return False
        if self.user_id != other.user_id or \
                self.thought != other.thought or \
                self.timestamp != other.timestamp:
            return False

        return True

    def __ne__(self, other):
        return not (self.__eq__(other))

    def serialize(self):
        thoughtEncoded = self.thought.encode("utf-8")
        thoughtSize = len(self.thought)
        return struct.pack("<QQI%ds" % thoughtSize, self.user_id, int(self.timestamp.timestamp()),
                           thoughtSize, thoughtEncoded)

    @classmethod
    def deserialize(cls, data_bytes):
        _MESSAGE_PREFIX_NUM_OF_BYTES = 20
        user_id, sec_time, thoughtSize = struct.unpack("<QQI", data_bytes[:_MESSAGE_PREFIX_NUM_OF_BYTES])
        timestamp = datetime.fromtimestamp(sec_time)
        thoughtEncoded = struct.unpack("<%ds" % thoughtSize, data_bytes[_MESSAGE_PREFIX_NUM_OF_BYTES:])

        thought = thoughtEncoded[0].decode("utf-8")
        return Thought(user_id, timestamp, thought)
    #
    # def __bool__(self):
    #     return True if self.data_dict else False
    #
    # def __getitem__(self, key):
    #     if self.data_dict.get(key) is None:
    #         raise KeyError(key)  # TODO: check if this is valid
    #     return self.data_dict[key][0]
    #
    # def __setitem__(self, key, value):
    #     if self.data_dict.get(key) is None:
    #         self.data_dict[key] = []
    #     self.data_dict[key].append(value)
    #
    # def __delitem__(self, key):
    #     if self.data_dict.get(key) is None:
    #         raise KeyError(key)  # TODO: check if this is valid
    #     self.data_dict[key].pop(0)
    #     if not self.data_dict[key]:  # list is empty
    #         self.data_dict.pop(key, None)
    #
    # def __len__(self):
    #     return len(self.data_dict)
    #
    # def __contains__(self, key):
    #     return key in self.data_dict
    #
    # def __iter__(self):
    #     for key in self.data_dict:
    #         yield key


if __name__ == '__main__':
    t1 = Thought(1, datetime(2000, 1, 1, 12, 1), "Hello")
    t2 = Thought(1, datetime(2000, 1, 1, 12, 1), "Hello")
    data = t1.serialize()
    print(data[:20])
    print(data[20:].decode())
    t3 = t1.deserialize(data)
    print( t1 == t3)
    # print(f"{t1!r}")
    # print(t1)
