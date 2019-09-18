"""
BatchLoader class: load hdf5 data in multi processing mode.
"""
from multiprocessing import cpu_count
from hdf5reader.file_finder import FileFinder
from hdf5reader.dataset_finder import DatasetFinder
from hdf5reader.load_h5view_data import load_h5view_data
import time

class BatchLoader:
    def __init__(self, files, batch_size=32):
        self.batch_size = batch_size
        dataset_finder = DatasetFinder(files)
        self.datasets = dataset_finder.get_datasets()
        self.idx = list(range(len(self.datasets)))
        self.steps_per_epoch = len(self.idx) // self.batch_size
        self.x = None
        self.y = None

    def get_batch(self, batch_id):
        start_index = batch_id*self.batch_size
        end_index = start_index + self.batch_size
        # print("get_batch {} {}".format(start_index, end_index))
        views_to_load = self.datasets[start_index:end_index]
        self.x, self.y = load_h5view_data(views_to_load)
        pass

    def __len__(self):
        return self.steps_per_epoch


if __name__ == '__main__':
    n_files = 90
    batch_size = 32

    file_finder = FileFinder("/mnt/space1/pospelov/data/d3hack/ver1/hdf5/datam_*.h5", n_files)
    print(file_finder.get_files())


    start = time.time()
    loader = BatchLoader(file_finder.get_files(), batch_size)
    print("Starting data loader for {} batches".format(len(loader)))
    for i in range(len(loader)):
        if i%10 == 0:
            print(i)
        loader.get_batch(i)

    print("... done in {:.3f}. batch_size {}, n_batches {}, n_files {}."
          .format(time.time() - start, batch_size, len(loader), len(file_finder.get_files())))


