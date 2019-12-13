import struct
import click

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
        return self


    def __repr__(self):
        return f'Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'


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

@click.command(name='read_minds')
@click.option('--address', '-a', default='127.0.0.1:5000', help="path to the data file")
def read_messages_to_cli(data_path):




if __name__ == '__main__':
    pass