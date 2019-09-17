"""
Unit tests for FileFinder class.
"""
import unittest
from hdf5reader.file_finder import FileFinder

TEST_FILE_NAMES = ["test_01.tmp", "test_02.tmp", "test_03.tmp"]


def generate_files():
    """
    Generates temporary files on disk.
    """
    for name in TEST_FILE_NAMES:
        open(name, 'a').close()


class TestFileFinder(unittest.TestCase):
    """
    Unit tests for FileFinder class.
    """
    def setUp(self):
        generate_files()

    def test_wrong_max_files(self):
        self.assertRaises(ValueError, FileFinder, "test_pattern", -1)

    def test_wrong_pattern(self):
        self.assertRaises(ValueError, FileFinder, "non-esixting-pattern")

    def test_find_files(self):
        finder = FileFinder("test_*.tmp")
        files = finder.get_files()
        self.assertEqual(files, TEST_FILE_NAMES)
        self.assertEqual(len(finder), 3)

    def test_find_files_subset(self):
        finder = FileFinder("test_*.tmp", 2)
        files = finder.get_files()
        self.assertEqual(files, TEST_FILE_NAMES[0:2])
        self.assertEqual(len(finder), 2)


if __name__ == '__main__':
    unittest.main()
