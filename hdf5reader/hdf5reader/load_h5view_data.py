"""
Collection of functions to load/process hdf5 dataset data
"""
import numpy as np
from hdf5reader.dataset_finder import DatasetFinder
from hdf5reader.file_finder import FileFinder
import time


def load_h5view_data(dataset_views):
    # images = [np.ndarray(x.shape, x.dtype) for x in dataset_views]
    # labels = [dict(x.attrs) for x in dataset_views]

    # for i, view in enumerate(dataset_views):
    #     view.read_direct(images[i])
    images = []
    for i, view in enumerate(dataset_views):
        images.append(np.array(view))

    return images


if __name__ == '__main__':
    file_finder = FileFinder("/mnt/space1/pospelov/data/d3hack/ver1/hdf5/datam_*.h5", 20)

    print("Constructing dataset...")
    start = time.time()
    datasets = DatasetFinder(file_finder.get_files())
    print("... done in {:.3f}.".format(time.time() - start))

    print("Loading views...")
    start = time.time()
    views = datasets.get_datasets()
    print("... done in {:.3f}. Total views {}.".format(time.time() - start, len(views)))

    # label = np.array([raw_data.attrs[param] for param in self.parameters])

    print("Processing images in batches...")
    start = time.time()
    batch_size = 128
    n_batches = len(views)//batch_size
    for batch_id in range(n_batches):
        start_index = batch_id*batch_size
        end_index = start_index + batch_size
        print("batch_id {}/{}, start_index {}, end_index {}"
              .format(batch_id, n_batches, start_index, end_index))
        images = load_h5view_data(views[start_index:end_index])
        print(len(images), images[0].dtype, type(images[0]))

    print("... done in {:.3f}.".format(time.time() - start))
