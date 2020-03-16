# from ..binary_operations import read_from_binary_file
# from ..protocol import Snapshot, User
#
#
# class ReaderBinary:
#     """ A Reader of Snapshot's objects
#         Once initialized, the user's info is automatically read from the path given, and consecutive
#         snapshots are read using an iterator or with the read_next_snapshot() function.
#         """
#
#     def __init__(self, path):
#         self.file = open(path, 'rb')
#         self.user = self.read_user_info()
#
#     def read_user_info(self):
#         id, name_len = read_from_binary_file(self.file, "QI")
#         name = read_from_binary_file(self.file, "%ds" % name_len)[0].decode()
#         birth_date, gender = read_from_binary_file(self.file, "Ic")
#         gender = gender.decode()
#         return User(id, name, birth_date, gender)
#
#     def read_next_snapshot(self):
#         timestamp, *_ = read_from_binary_file(self.file, "Q")
#
#         if timestamp is None:
#             raise StopIteration
#
#         translation_tuple = read_from_binary_file(self.file, "3d")
#         rotation_tuple = read_from_binary_file(self.file, "4d")
#         color_height, color_width = read_from_binary_file(self.file, "II")
#         color_bgr = self.file.read(color_height * color_width * 3)
#         depth_height, depth_width = read_from_binary_file(self.file, "II")
#         depth_vals = read_from_binary_file(self.file, f"{depth_height * depth_width}f")
#         hunger, thirst, exhaustion, happiness = read_from_binary_file(self.file, "4f")
#
#         return Snapshot(timestamp, translation_tuple, rotation_tuple,
#                         (color_height, color_width, color_bgr),
#                         (depth_height, depth_width, depth_vals),
#                         (hunger, thirst, exhaustion, happiness))
#
#     def __next__(self):
#         return self.read_next_snapshot()
#
#     def __iter__(self):
#         return self
#
#     def __repr__(self):
#         return f"A reader Object for the file {self.file}"
#
#
# if __name__ == '__main__':
#     r = ReaderBinary('../../../dataFiles/sample.mind')
#     print(r.user)
#     for snapshot in r:
#         print(snapshot)
#         txt = input()
