import struct


def read_from_binary_file(bytes_stream, unpack_format_string):
    """ Returns a tuple, even if one item returned """
    size = struct.calcsize(unpack_format_string)
    messageInBytes = bytes_stream.read(size)
    return struct.unpack(unpack_format_string, messageInBytes)
