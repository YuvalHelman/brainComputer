from .reader import User
import struct
from .binary_operations import read_from_binary_file


class Hello:
    def __init__(self, user):
        self.user = user

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

    def serialize(self, fields: iter):
        if 'translation' in fields:
            translation = self.translation
        else:
            translation = (0, 0, 0)

        if 'rotation' in fields:
            rotation = self.rotation
        else:
            rotation = (0, 0, 0, 0)

        if "color_image" in fields:
            col_w, col_h, col_data = self.color_image
        else:
            col_w, col_h, col_data = (0, 0, b'')

        if "depth_image" in fields:
            depth_w, depth_h, depth_data = self.depth_image
        else:
            depth_w, depth_h, depth_data = (0, 0, b'')

        if "feelings" in fields:
            feelings = self.feelings
        else:
            feelings = (0, 0, 0, 0)

        args = [self.timestamp, *translation, *rotation, col_w, col_h]
        if col_data:
            args.append(col_data)
        args.extend([depth_w, depth_h])
        if col_data:
            args.append(depth_data)
        args.append(*feelings)
        return struct.pack(f'<Q3d4d'  # timestamp, translation, rotation 
                           f'II{len(col_data)}s'  # color_image. len(col_data) bytes
                           f'II{len(depth_data)}f'  # width_image. len(depth_data) floats
                           f'4f', *args)

    @classmethod
    def deserialize(cls, bytes_stream, fields):
        timestamp, \
        translation_x, translation_y, translation_z, \
        rotation_x, rotation_y, rotation_z, rotation_w, \
        color_height, color_width = read_from_binary_file(bytes_stream, 'Q4d3dII')

        color_data = b''  # TODO: None ?
        if "color_image" in fields:
            color_data = bytes_stream.read(color_height * color_width * 3)

        depth_height, depth_width = read_from_binary_file(bytes_stream, "II")

        depth_data = b''  # TODO: None ?
        if "depth_image" in fields:
            depth_data = read_from_binary_file(bytes_stream, f"{depth_height * depth_width}f")

        feelings = (0.0, 0.0, 0.0, 0.0)
        if "feelings" in fields:
            feelings = read_from_binary_file(bytes_stream, "4f")

        return Snapshot(timestamp, (translation_x, translation_y, translation_z),
                        (rotation_x, rotation_y, rotation_z, rotation_w),
                        (color_height, color_width, color_data),
                        (depth_height, depth_width, depth_data),
                        feelings)
