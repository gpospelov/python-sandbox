"""
DatasetFinder class: finds datasets in collection of hdf5 files.
"""
import h5py
from file_finder import FileFinder
import time


def get_datasets(group):
    """
    Iteratively going through hdf5 file and collecting all data set keys.
    """
    datasets = []

    if not hasattr(group, "keys"):
        return []

    keys = group.keys()

    for key in keys:
        items = get_datasets(group[key])

        if not items:
            datasets.append(key)

        for item in items:
            datasets.append("{}/{}".format(key, item))

    return datasets


class DatasetFinder:
    """
    Finds hdf5 datasets in collection of hdf5 files. Files remains open for later dataset usage.
    """
    def __init__(self, hdf5_file_names):
        print("DatasetFinder> Starting initialization ...")
        start = time.time()
        self.hdf5_files = [h5py.File(filename, "r") for filename in hdf5_file_names]
        self.datasets = list()
        print("DatasetFinder> ... done in {:.3f}, {} file(s) total."
              .format(time.time() - start, len(self.hdf5_files)))

    def load_dataset_views(self):
        """
        Load all views to hdf5 datasets into the list.
        """
        print("DatasetFinder> Loading dataset views ...")
        start = time.time()
        for h5file in self.hdf5_files:
            for key in get_datasets(h5file):
                self.datasets.append(h5file[key])
        print("DatasetFinder> ... done in {:.3f}, {} datasets total."
              .format(time.time() - start, len(self.datasets)))

    def get_datasets(self):
        """
        Returns list of existing views to hdf5 datasets.
        """
        if not len(self.datasets):
            self.load_dataset_views()

        return self.datasets


class DatasetFinderV2:
    """
    Finds hdf5 datasets in collection of hdf5 files. Files remains open for later dataset usage.
    """
    def __init__(self, hdf5_file_names):
        print("DatasetFinderV2> Starting initialization ...")
        start = time.time()
        self.hdf5_files = [h5py.File(filename, "r") for filename in hdf5_file_names]
        self.datasets = list()
        print("DatasetFinderV2> ... done in {:.3f}, {} file(s) total."
              .format(time.time() - start, len(self.hdf5_files)))

    def load_dataset_views(self):
        """
        Load all views to hdf5 datasets into the list.
        """
        print("DatasetFinderV2> Loading dataset views ...")
        start = time.time()
        for h5file in self.hdf5_files:
            for key in h5file.keys():
                self.datasets.append(h5file[key])
        print("DatasetFinderV2> ... done in {:.3f}, {} datasets total."
              .format(time.time() - start, len(self.datasets)))

    def get_datasets(self):
        """
        Returns list of existing views to hdf5 datasets.
        """
        if not len(self.datasets):
            self.load_dataset_views()

        return self.datasets


def test_finder(dataset_finder_class, file_pattern, maxfiles):
    file_finder = FileFinder(file_pattern, maxfiles)

    start = time.time()
    print("Constructing dataset...")
    dataset_finder = dataset_finder_class(file_finder.get_files())
    print("Done. Time to construct dataset {:.3f}".format(time.time() - start))

    start = time.time()
    print("Loading views...")
    dataset_finder.load_dataset_views()
    print("Done. Time to load views {:.3f}".format(time.time() - start))

    start = time.time()
    views = dataset_finder.get_datasets()
    print("Time to get datasets {:.3f}, size {}".format(time.time() - start, len(views)))


if __name__ == '__main__':
    # test_finder(DatasetFinder, "/mnt/space1/pospelov/data/d3hack/ver1/hdf5/datam_*.h5", 50)
    test_finder(DatasetFinderV2, "/mnt/space1/pospelov/data/d3hack/ver1/hdf5_v2/datam_*.h5", 50)
