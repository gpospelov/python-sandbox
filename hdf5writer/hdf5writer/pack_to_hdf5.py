"""
Bundle multiple *.npy  and *.json files into single hdf5 file.

Resulting file will contain single group '/' and collection of datasets
with name, corresponding to npy file.
"""
import h5py
import click
import glob
import os
import numpy as np
import json

INPUTDIR = "/mnt/space1/pospelov/data/d3hack/ver1/val"
OUTPUTDIR = "/mnt/space1/pospelov/data/d3hack/ver1/hdf5_v2"
CHUNKSIZE = 1000
MAXINPUTFILES = 100000
OUTPUTNAME = "val_datam_"

def get_run_number(full_file_name):
    name = os.path.basename(full_file_name)
    run_number = ''.join(c for c in name if c.isdigit())
    return int(run_number)


def find_files(inputdir, maxinputfiles):
    """
    Find *.npy and *.json files in given directory.
    :param inputdir: Directory to look for files.
    :return: Two lists with *.npy and *.json file names.
    """
    npy_files = glob.glob(inputdir+"/*.npy")
    json_files = glob.glob(inputdir+"/*.json")

    npy_files = sorted(npy_files)
    json_files = sorted(json_files)

    if maxinputfiles and maxinputfiles > 0:
        npy_files = npy_files[0:maxinputfiles]
        json_files = json_files[0:maxinputfiles]

    if not len(npy_files):
        raise ValueError("No files found in directory '{}'.".format(inputdir))

    if len(npy_files) != len(json_files):
        raise ValueError("Number of npy files {} doesn't match number of json files {}".format(npy_files, json_files))

    last_npy_run_number = get_run_number(npy_files[-1])
    last_json_run_number = get_run_number(json_files[-1])
    if last_npy_run_number != last_json_run_number:
        raise ValueError("Seems run numbers are different npy:{}, json:{}.".format(last_npy_run_number, last_json_run_number))

    print("First pair : '{}', '{}'".format(npy_files[0], json_files[0]))
    print("Last pair  : '{}', '{}'".format(npy_files[-1], json_files[-1]))
    print("{} pairs in total.".format(len(npy_files)))

    return npy_files, json_files


def create_dataset(h5_file, numpy_file_name, json_file_name):
    """
    Create dataset in existing hdf5 file.
    :param h5_file: HDF5 file opened for writing.
    :param numpy_file_name: Name of file with numpy array.
    :param json_file_name: Name of file with json attributes.
    """
    arr = np.load(numpy_file_name).astype('float32')
    jattr = json.load(open(json_file_name))
    dset_name = os.path.basename(numpy_file_name)

    dset = h5_file.create_dataset(dset_name, data=arr, compression=None, shuffle=False)
    for key, value in jattr.items():
        if isinstance(value, type(str())):
            dset.attrs.create(key, value, None, dtype=f"<S{len(value)}")
        else:
            dset.attrs.create(key, value)


def process_files(npy_files, json_files, chunksize, outputdir, outputname):
    """
    Main function to process numpy/json files.
    :param npy_files: List of numpy files.
    :param json_files: List of json files.
    :param chunksize: Number of numpy/json pair to put into single output file (i.e. 1000)
    :param outputdir: Directory for output files.
    :param outputname: Name of output file (index and extention will be added).
    """
    file_count = len(npy_files)
    chunk_count = file_count // chunksize
    print("Processing {} chunks, {} files per chunk.".format(chunk_count, chunksize))

    for chunk in range(0, chunk_count):
        start_index = chunk*chunksize
        end_index = start_index+chunksize
        filename = os.path.join(outputdir, outputname+"{:06d}".format(chunk)+".h5")
        print("Chunk {}, filename {}, start_index {}, end_index {}.".format(chunk, filename, start_index, end_index))
        with h5py.File(filename, "w") as f:
            for idx in range(start_index, end_index):
                create_dataset(f, npy_files[idx], json_files[idx])


@click.command()
@click.option('--inputdir', required=False, type=str, default=INPUTDIR, help='Input directory.')
@click.option('--outputdir', required=False, type=str, default=OUTPUTDIR, help='Output directory.')
@click.option('--chunksize', required=False, type=int, default=CHUNKSIZE, help='Number of input pairs per one output file.')
@click.option('--maxinputfiles', required=False, type=int, default=MAXINPUTFILES, help='Maximum number of input files to process.')
@click.option('--outputname', required=False, default=OUTPUTNAME, type=str)
def run_pack(inputdir, outputdir, chunksize, maxinputfiles, outputname):
    print("inputdir      : {}".format(inputdir))
    print("outputdir     : {}".format(outputdir))
    print("chunksize     : {}".format(chunksize))
    print("maxinputfiles : {}".format(maxinputfiles))
    print("outputname    : {}".format(outputname))

    npy_files, json_files = find_files(inputdir, maxinputfiles)
    process_files(npy_files, json_files, chunksize, outputdir, outputname)


if __name__ == '__main__':
    run_pack()
