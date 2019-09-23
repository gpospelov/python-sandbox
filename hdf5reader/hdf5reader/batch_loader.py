"""
BatchLoader class: load hdf5 data in multi processing mode.
"""
from multiprocessing import cpu_count
from file_finder import FileFinder
from dataset_finder import DatasetFinder
from dataset_finder import DatasetFinderV2
from load_h5view_data import load_h5view_data
from multiprocessing.pool import ThreadPool as Pool
from threading import Lock
import time
import numpy as np
import sys
import traceback


class BatchBlock:
    def __init__(self, batch_id, images, labels):
        self.batch_id = batch_id
        self.images = images
        self.labels = labels


def load_batch_block(batch_id, dataset_views):
    images = [np.ndarray(x.shape, x.dtype) for x in dataset_views]
    labels = [dict(x.attrs) for x in dataset_views]

    for i, view in enumerate(dataset_views):
        view.read_direct(images[i])

    return BatchBlock(batch_id, images, labels)


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
        return load_batch_block(batch_id, views_to_load)

    def __len__(self):
        return self.steps_per_epoch

    def close(self):
        pass


class ParallelBatchLoader:
    def __init__(self, files, batch_size=32):
        self.batch_size = batch_size
        dataset_finder = DatasetFinderV2(files)
        self.datasets = dataset_finder.get_datasets()
        self.idx = list(range(len(self.datasets)))
        self.steps_per_epoch = len(self.idx) // self.batch_size
        self.max_workers = 4
        self.pool = Pool(self.max_workers)
        self.mutex = Lock()
        self.queue = []
        self.currentBatchBlock = None
        self.next_batch_to_process = 0
        self.load_func = load_batch_block

    def submit_batch(self):
        if self.next_batch_to_process >= self.steps_per_epoch:
            raise ValueError("Maximum number of batches reached, next_batch_to_process:{}. steps_per_epoch:{}".format(self.next_batch_to_process, self.steps_per_epoch))
        start_index = self.next_batch_to_process*self.batch_size
        end_index = start_index + self.batch_size
        views_to_load = self.datasets[start_index:end_index]
        args = (self.next_batch_to_process, views_to_load)
        print("submitting batch id {}, start_index {}, end_index {}, queue length {}.".format(self.next_batch_to_process, start_index, end_index, len(self.queue)))
        result = self.pool.apply_async(self.load_func, args=args)
        self.queue.append(result)
        self.next_batch_to_process += 1
        # print("...end of submit, queue len {}".format(len(self.queue)))

    def fill_queue(self):
        try:
            self.mutex.acquire()
            while len(self.queue) < self.max_workers and self.next_batch_to_process < self.steps_per_epoch:
                self.submit_batch()
        finally:
            self.mutex.release()

    def get_batch(self, batch_id):
        success = True

        try:
            self.mutex.acquire()

            while len(self.queue) < self.max_workers and self.next_batch_to_process < self.steps_per_epoch:
                self.submit_batch()

            result = self.queue[0]
            self.queue = self.queue[1:]
            batch_block = result.get()
            if batch_block.batch_id != batch_id:
                raise ValueError("Multiprocessing failure for {}".format(batch_id))

            return batch_block
        except:
            exc_info = sys.exc_info()
            print("Unexpected error:", exc_info[0])
            traceback.print_tb(exc_info[2])
            success = False
        finally:
            self.mutex.release()

        if not success:
            print("Encountered fatal exception")
            sys.exit(-1)

    def __len__(self):
        return self.steps_per_epoch

    def close(self):
        self.pool.close()


def test_batch_loader(batch_loader_class, file_pattern, nfiles, batch_size):
    file_finder = FileFinder(file_pattern, nfiles)

    start = time.time()
    print("Constructing batch loader for {} files ...".format(len(file_finder.get_files())))
    loader = batch_loader_class(file_finder.get_files(), batch_size)
    print("... done in {:.3f}. Steps per epoch {}.".format(time.time() - start, len(loader)))

    start = time.time()
    print("Starting data loader for {} batches".format(len(loader)))
    for i in range(len(loader)):
        result = loader.get_batch(i)
        if i%10 == 0:
            print("result for batch {}, block_id {}, len(images) {}, type {}".format(i, result.batch_id, len(result.images), type(result.images[0])))

    diff_time = time.time() - start
    print("... done in {:.3f}. batch_size {}, n_batches {}, n_files {}. Performance {} images/sec."
          .format(diff_time, batch_size, len(loader), len(file_finder.get_files()), (len(loader)*batch_size)//diff_time))
    loader.close()


def main():
    # test_batch_loader(BatchLoader, "/mnt/space2/pospelov/data/d3hack/ver1/hdf5_v2/datam_*.h5", 2, 128)
    test_batch_loader(ParallelBatchLoader, "/mnt/space2/pospelov/data/d3hack/ver1/hdf5_v2/datam_*.h5", 2, 128)


if __name__ == '__main__':
    main()
