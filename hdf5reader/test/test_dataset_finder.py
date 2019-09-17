"""
Unit tests for DatasetFinder class.
"""
import unittest
from hdf5reader.file_finder import FileFinder
from hdf5reader.dataset_finder import DatasetFinder
import h5py


class TestDatasetFinder(unittest.TestCase):
    """
    Unit tests for FileFinder class.
    """
    def test_dataset_finder(self):
        files = ["/mnt/space1/pospelov/data/d3hack/ver1/hdf5/datam_0000.h5"]
        dataset_finder = DatasetFinder(files)
        views = dataset_finder.get_datasets()
        self.assertEqual(len(views), 1000)
        self.assertTrue(isinstance(views[0], h5py.Dataset))


if __name__ == '__main__':
    unittest.main()
