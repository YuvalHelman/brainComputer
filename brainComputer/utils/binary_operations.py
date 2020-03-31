import struct


def read_from_binary_file(bytes_stream, unpack_format_string):  # TODO: erase ?
    """ Returns a tuple, even if one item returned """
    try:
        size = struct.calcsize(unpack_format_string)
        messageInBytes = bytes_stream.read(size)
        if messageInBytes is None:
            return None
        return struct.unpack(unpack_format_string, messageInBytes)
    except Exception as e:
        print(f'Error reading from binary: {e}')
        return None
