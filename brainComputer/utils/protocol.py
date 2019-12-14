from .reader import User
import struct
from .binary_operations import read_from_binary_file


class Hello:
    def __init__(self, user_id, user_name, user_birth_date, user_gender):
        self.user = User(user_id, user_name, user_birth_date, user_gender)

    def __repr__(self):
        return f"Hello(user_id={self.user.id}, " \
               f"user_name={self.user.name}, " \
               f"birth={self.user.birth_date}, " \
               f"gender={self.user.gender})"

    def serialize(self):
        return struct.pack(f"QI{len(self.user.name)}sIc", self.user.id, self.user.name.encode(),
                           self.user.birth_date, self.user.gender.encode())

    @classmethod
    def deserialize(cls, bytes_stream):
        uid, name_len = read_from_binary_file(bytes_stream, "QI")
        name = read_from_binary_file(bytes_stream, f"{name_len}s")[0].decode()
        birth_date, gender = read_from_binary_file(bytes_stream, "Ic")
        gender = gender.decode()
        return Hello(User(uid, name, birth_date, gender))


class Config:
    def __init__(self, fields):
        self.fields = fields

    def serialize(self):
        """ Serialize the config into:
        The number of fields followed by a sequence of uint32 field_len and then the field"""
        args = [len(self.fields)]
        args_format = "I"
        for field in self.fields:
            args_format += f"I%ds" % len(field)
            args.append(len(field))
            args.append(field)
        return struct.pack(args_format, *args)

    @classmethod
    def deserialize(cls, bytes_stream):
        fields_list = []
        num_of_fields = read_from_binary_file(bytes_stream, "I")[0]
        for i in range(num_of_fields):
            field_len = read_from_binary_file(bytes_stream, "I")[0]
            field = read_from_binary_file(bytes_stream, f"{field_len}s")[0]
            fields_list.append(field)
        return Config(fields_list)


class Snapshot:
    """ Represents a Snapshot of a client's mind """

    def __init__(self, timestamp, translation, rotation, color_image, depth_image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self):
        return \
            f"Snapshot from {self.timestamp}, " \
            f"on translation={self.translation}, / " \
            f'rotation={self.rotation}, ' \
            f'with a {self.color_image[0]}x{self.color_image[1]} color image ' \
            f"and a {self.depth_image[0]}x{self.depth_image[1]}. " \
            f'feelings={self.feelings})'

    def serialize(self, fields):
        pass  # TODO

    @classmethod
    def deserialize(cls, fields):
        pass  # TODO
