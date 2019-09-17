"""
Collection of functions to load/process hdf5 dataset data
"""
import numpy as np
from hdf5reader.dataset_finder import DatasetFinder
import time


def load_h5view_data(dataset_views):
    images = [np.ndarray(x.shape, x.dtype) for x in dataset_views]
    labels = [dict(x.attrs) for x in dataset_views]

    for i, view in enumerate(dataset_views):
        view.read_direct(images[i])

    return images, labels


if __name__ == '__main__':
    files = ["/mnt/space1/pospelov/data/d3hack/ver1/hdf5/datam_0000.h5"]

    dataset_finder = DatasetFinder(files)

    start = time.time()
    print("Constructing dataset...")
    datasets = DatasetFinder(files)
    print("Done. Time to construct dataset {:.3f}".format(time.time() - start))

    start = time.time()
    print("Loading views...")
    views = datasets.get_datasets()

    # label = np.array([raw_data.attrs[param] for param in self.parameters])

    images, labels = load_h5view_data(views[0:8])
    # print(len(images))
    print(images)
    print(labels, len(labels))


    # arrs = list()
    # arrs.append(np.ndarray((10, 20), dtype=float))
    # arrs.append(np.ndarray((10, 20), dtype=float))
    # print(type(arrs[0]))
    # x = np.array(arrs)
    # print(x[0])

    # a1 = np.array([1, 2, 3])
    # a2 = np.array([1, 2, 3])
    # print(a1, type(a1))
    # print(a2, type(a2))
    #
    # xx = [a1, a2]
    # print(xx, type(xx))
    # zz = np.array(xx)
    # print(zz, type(zz))
