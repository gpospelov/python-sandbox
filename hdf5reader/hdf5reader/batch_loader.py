"""
BatchLoader class: load hdf5 data in multi processing mode.
"""
from multiprocessing import cpu_count
from hdf5reader.file_finder import FileFinder
from hdf5reader.dataset_finder import DatasetFinder
from hdf5reader.dataset_finder import DatasetFinderV2
from hdf5reader.load_h5view_data import load_h5view_data
import time


class BatchLoader:
    def __init__(self, files, batch_size=32):
        self.batch_size = batch_size
        dataset_finder = DatasetFinderV2(files)
        self.datasets = dataset_finder.get_datasets()
        self.idx = list(range(len(self.datasets)))
        self.steps_per_epoch = len(self.idx) // self.batch_size

    def get_batch(self, batch_id):
        start_index = batch_id*self.batch_size
        end_index = start_index + self.batch_size
        # print("get_batch {} {}".format(start_index, end_index))
        views_to_load = self.datasets[start_index:end_index]
        return load_h5view_data(views_to_load)

    def __len__(self):
        return self.steps_per_epoch


def test_batch_loader(batch_loader_class, file_pattern, nfiles, batch_size):
    file_finder = FileFinder(file_pattern, nfiles)

    start = time.time()
    print("Constructing batch loader for {} files ...".format(len(file_finder.get_files())))
    loader = batch_loader_class(file_finder.get_files(), batch_size)
    print("... done in {:.3f}. Steps per epoch {}.".format(time.time() - start, len(loader)))

    print("Starting data loader for {} batches".format(len(loader)))
    for i in range(len(loader)):
        if i%10 == 0:
            print(i)
        loader.get_batch(i)

    print("... done in {:.3f}. batch_size {}, n_batches {}, n_files {}."
          .format(time.time() - start, batch_size, len(loader), len(file_finder.get_files())))


if __name__ == '__main__':
    test_batch_loader(BatchLoader, "/mnt/space2/pospelov/data/d3hack/ver1/hdf5_v2/datam_*.h5", 20, 128)

