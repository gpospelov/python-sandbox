"""
DatasetFinder class: finds datasets in collection of hdf5 files.
"""
import h5py
from hdf5reader.file_finder import FileFinder
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
        self.hdf5_files = [h5py.File(filename, "r") for filename in hdf5_file_names]
        self.datasets = list()

    def load_dataset_views(self):
        for h5file in self.hdf5_files:
            for key in get_datasets(h5file):
                self.datasets.append(h5file[key])

    def get_datasets(self):
        if not len(self.datasets):
            self.load_dataset_views()

        return self.datasets


if __name__ == '__main__':
    file_finder = FileFinder("/mnt/space1/pospelov/data/d3hack/ver1/hdf5/datam_*.h5", 100)
    print()

    start = time.time()
    print("Constructing dataset...")
    dataset_finder = DatasetFinder(file_finder.get_files())
    print("Done. Time to construct dataset {:.3f}".format(time.time() - start))

    start = time.time()
    print("Loading views...")
    dataset_finder.load_dataset_views()
    print("Done. Time to load views {:.3f}".format(time.time() - start))

    start = time.time()
    views = dataset_finder.get_datasets()
    print("Time to get datasets {:.3f}, size {}".format(time.time() - start, len(views)))



