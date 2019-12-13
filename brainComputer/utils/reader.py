import struct


class Snapshot:
    """ Represents a Snapshot of a client's mind """

    def __init__(self):
        self.user_id = None

    def __next__(self):
        return_value = self.a
        self.a, self.b = self.b, self.a + self.b
        return return_value

    def __iter__(self):
        return self


class ReaderBinary:
    """ A Reader of Snapshot's objects """

    def __init__(self, path):
        self.file = open(path, 'rb')

        self.curr_snapshot = Snapshot()

    def get_user_info(self):
        user_id = read_from_binary_file(self.file, "Q")
        user_name_len = read_from_binary_file(self.file, "I")
        user_name = read_from_binary_file(self.file, "%ds" % user_name_len)[0].decode("utf-8")
        user_birth_date = read_from_binary_file(self.file, "I")
        user_gender = read_from_binary_file(self.file, "c").decode("ASCII")
        return User(user_id)

    # 1. Read from the file and use a generator to generate snapshots!
    #

    def __repr__(self):
        return f'Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'


def read_from_binary_file(file, unpack_format_string):
    size = struct.calcsize(unpack_format_string)
    messageInBytes = file.read(size)
    return struct.unpack(unpack_format_string, messageInBytes)


class User:
    def __init__(self, id, name, birth_date, gender):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.gender = gender


class Snapshot:
    def __init__(self, timestamp, translationTup, rotation):
        self.timestamp = timestamp


class Translation3D:
    def __init__(self, translation_x, translation_y, translation_z):
        self.translation_x = translation_x
        self.translation_y = translation_y
        self.translation_z = translation_z
