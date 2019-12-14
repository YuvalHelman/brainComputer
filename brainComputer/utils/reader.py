import struct
import click
from datetime import datetime

class aaa:

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
        self.user_info = self.get_user_info()

    def get_user_info(self):
        id, name_len = read_from_binary_file(self.file, "QI")
        name = read_from_binary_file(self.file, "%ds" % name_len)[0].decode("ASCII")
        birth_date, gender = read_from_binary_file(self.file, "Ic")
        gender = gender.decode("ASCII")
        return User(id, name, birth_date, gender)

    def get_snapshot(self):
        timestamp = read_from_binary_file(self.file, "Q")
        translation_tuple = read_from_binary_file(self.file, "3d")
        rotation_tuple = read_from_binary_file(self.file, "4d")
        color_height, color_width = read_from_binary_file(self.file, "II")
        color_bgr = self.file.read(color_height * color_width * 3)
        depth_height, depth_width = read_from_binary_file(self.file, "II")
        depth_vals = read_from_binary_file(self.file, f"{depth_height * depth_width}f")
        hunger, thirst, exhaustion, happiness = read_from_binary_file(self.file, "4f")

        return Snapshot(timestamp, translation_tuple, rotation_tuple,
                        (color_height, color_width, color_bgr),
                        (depth_height, depth_width, depth_vals),
                        (hunger, thirst, exhaustion, happiness))

    def __iter__(self):
        return self.get_snapshot()

    def __repr__(self):
        return f"A reader Object for the file {self.file}"


def read_from_binary_file(file, unpack_format_string):
    # Returns a tuple, even if one item returned
    size = struct.calcsize(unpack_format_string)
    messageInBytes = file.read(size)
    return struct.unpack(unpack_format_string, messageInBytes)


class User:
    def __init__(self, uid, name, birth_date, gender):
        self.id = uid
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    def __repr__(self):
        return f"id={self.id}"


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
        f"Snapshot from {datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d_%H-%M-%S')}, " \
        f"on translation={self.translation}, / " \
        f'rotation={self.rotation}, ' \
        f'with a {self.color_image[0]}x{self.color_image[1]} color image ' \
        f"and a {self.depth_image[0]}x{self.depth_image[1]}. " \
        f'feelings={self.feelings})'


@click.command(name='read_minds')
@click.option('--data_path', '-d', help="path to the data file to read from")
def read_messages_to_cli(data_path):
    pass


if __name__ == '__main__':
    r = ReaderBinary('')
