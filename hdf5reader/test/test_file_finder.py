import unittest
from hdf5reader.file_finder import FileFinder


class TestFileFinder(unittest.TestCase):
    def test_wrong_pattern(self):
        finder = FileFinder("wrong_pattern*")
        self.assertRaises(ValueError, finder.get_files)


if __name__ == '__main__':
    unittest.main()
