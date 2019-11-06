"""
Collection of common utils for bulc code processing.
"""
import os


def find_files(dir_name):
    """
    Yield recursive list of files in given path
    """
    for subdir, dirs, files in os.walk(dir_name):
        for filename in files:
            yield os.path.join(subdir, filename)


def get_files(dir_name, extension=".h"):
    """
    Returns list of files with given extension.
    """
    result = list()
    for filename in find_files(dir_name):
        if os.path.splitext(filename)[1] == extension:
            result.append(filename)
    return result


def different_elements_count(list1, list2):
    """
    Compares two lists element wise and return number of different entries.
    Length of lists should be the same.
    """
    diff_count = 0
    for x, y in zip(list1, list2):
        if x != y:
            diff_count += 1
    return diff_count
