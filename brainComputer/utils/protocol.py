import struct
import io
import json
from .binary_operations import read_from_binary_file


class User:
    def __init__(self, uid, name, birth_date, gender):
        self.id = uid
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    def __repr__(self):
        return \
            f"User(id={self.id}, " \
            f"name={self.name}, " \
            f"birth_date={self.birth_date}, " \
            f"gender={self.gender})"


class Hello:
    def __init__(self, user):
        self.user = user

    def __repr__(self):
        return f"Hello(user_id={self.user.id}, " \
               f"user_name={self.user.name}, " \
               f"birth={self.user.birth_date}, " \
               f"gender={self.user.gender})"

    def to_json(self):
        return dict(
            user_id=self.user.id,
            user_name=self.user.name,
            birth=self.user.birth_date,
            gender=self.user.gender
            )

    @classmethod
    def from_json(self, binary_json):
        data_dict = json.loads(binary_json)
        return Hello(User(data_dict['user_id'], data_dict['user_name'], data_dict['birth'], data_dict['gender']))

    def serialize(self):
        try:
            ret = struct.pack(f"<QI{len(self.user.name)}sIc",
                              self.user.id, len(self.user.name), self.user.name.encode(),
                              self.user.birth_date, self.user.gender.encode())
            return ret
        except Exception as e:
            print("Hello message serialize failed:", e)
            raise e

    @classmethod
    def deserialize(cls, bytes_stream):
        uid, name_len = read_from_binary_file(bytes_stream, "<QI")
        name = read_from_binary_file(bytes_stream, f"<{name_len}s")[0].decode()
        birth_date, gender = read_from_binary_file(bytes_stream, "<Ic")
        gender = gender.decode()
        return Hello(User(uid, name, birth_date, gender))


class Config:
    def __init__(self, fields):
        self.fields = fields

    def serialize(self):
        """ Serialize the config into:
        The number of fields followed by a sequence of uint32 field_len and then the field"""
        args = [len(self.fields)]
        args_format = "<I"
        for field in self.fields:
            args_format += f"I{len(field)}s"
            args.extend([len(field), field.encode()])
        return struct.pack(args_format, *args)

    @classmethod
    def deserialize(cls, bytes_stream):
        fields_list = []
        num_of_fields, *_ = read_from_binary_file(bytes_stream, "<I")
        for i in range(num_of_fields):
            field_len, *_ = read_from_binary_file(bytes_stream, "<I")
            field, *_ = read_from_binary_file(bytes_stream, f"<{field_len}s")
            fields_list.append(field.decode())
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
        # date = datetime.datetime.fromtimestamp(self.timestamp)
        # date = date.strftime('%Y-%m-%d_%H:%M:%S')

        return \
            f"Snapshot from {self.timestamp}, " \
            f"on translation={self.translation}, " \
            f'rotation={self.rotation}, ' \
            f'with a {self.color_image[0]}x{self.color_image[1]} color image ' \
            f"and a {self.depth_image[0]}x{self.depth_image[1]} depth. " \
            f'feelings={self.feelings}'

    # def to_json(self):
    #     return dict(
    #         timestamp=self.user.id,
    #         user_name=self.user.name,
    #         birth=self.user.birth_date,
    #         gender=self.user.gender
    #         )
    #
    # @classmethod
    # def from_json(self, binary_json):
    #     data_dict = json.loads(binary_json)
    #     return Hello(User(data_dict['user_id'], data_dict['user_name'], data_dict['birth'], data_dict['gender']))


    def serialize(self, fields: iter) -> bytes:
        translation = (0, 0, 0)
        if 'translation' in fields:
            translation = self.translation

        rotation = (0, 0, 0, 0)
        if 'rotation' in fields:
            rotation = self.rotation

        col_w, col_h, col_data = (0, 0, b'')
        if "color_image" in fields:
            col_w, col_h, col_data = self.color_image

        depth_w, depth_h, depth_data = (0, 0, b'')
        if "depth_image" in fields:
            depth_w, depth_h, depth_data = self.depth_image

        feelings = (0, 0, 0, 0)
        if "feelings" in fields:
            feelings = self.feelings

        args = [self.timestamp, *translation, *rotation, col_w, col_h]
        if col_data:
            args.append(col_data)
        args.extend([depth_w, depth_h])
        if depth_data:
            args.append(depth_data)
        args.extend([*feelings])

        return struct.pack(f'<Qddddddd'  # timestamp, translation, rotation 
                           f'II{len(col_data)}s'  # color_image. len(col_data) bytes
                           f'II{len(depth_data)}f'  # width_image. len(depth_data) floats
                           f'ffff', *args)

    @classmethod
    def deserialize(cls, bytes_stream: io.BytesIO, fields):
        timestamp, \
        translation_x, translation_y, translation_z, \
        rotation_x, rotation_y, rotation_z, rotation_w, \
        color_width, color_height = read_from_binary_file(bytes_stream, '<QdddddddII')

        color_data = b''  # TODO: None ?
        if "color_image" in fields:
            color_data = bytes_stream.read(color_height * color_width * 3)

        depth_w, depth_h = read_from_binary_file(bytes_stream, "<II")

        depth_data = b''  # TODO: None ?
        if "depth_image" in fields:
            depth_data, *_ = read_from_binary_file(bytes_stream, f"<{depth_w * depth_h}f")

        feelings = read_from_binary_file(bytes_stream, "<4f")

        return Snapshot(timestamp,
                        (translation_x, translation_y, translation_z),
                        (rotation_x, rotation_y, rotation_z, rotation_w),
                        (color_width, color_height, color_data),
                        (depth_w, depth_h, depth_data),
                        feelings)
