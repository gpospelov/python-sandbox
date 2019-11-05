"""
Searches C++ include directives and adds prefix to them

#include "model.h"
will become
#include <mvvm/model/model.h"
"""
import os
from collections import defaultdict
from pathlib import Path
import re


HEADER_LOCATION = "/home/pospelov/development/qt-mvvm/qt-mvvm/mvvm"
SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/examples"


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


def get_source_files(dir_name):
    """
    Returns list of cpp and header files in given dir_name and its sub-folders.
    """
    return get_files(dir_name, ".h") + get_files(dir_name, ".cpp")


def get_header_file_map(dir_name):
    """
    Return multi map of headers in given dir_name. Key contain header file name, value
    contains list of dirs where this file was found.
    {'setvaluecommand.h': ['mvvm/commands'], 'removeitemcommand.h': ['mvvm/commands']}
    """
    result = defaultdict(list)
    for filename in get_files(dir_name, ".h"):
        parts = Path(os.path.dirname(filename)).parts
        include_prefix = os.path.join(parts[-2], parts[-1])
        result[os.path.basename(filename)].append(include_prefix)
    return result


def find_include_statement(line):
    """
    Checks if line contains quotes-like include statement and parse and returns file name from it.
    #include "modelview.h" ==> modelview.h
    """
    if "#include" in line:
        matches = re.findall(r'\"(.+?)\"', line)
        if len(matches) == 1:
            return matches[0]
    return None


def fix_include_statement(line, header_map):
    """
    Replaces quote-based header statement with full-path-braced based statement.
    #include "path.h" ==> #include <mvvm/model/path.h>
    """
    name_to_include = find_include_statement(line)
    if name_to_include:
        header_folders = header_map[name_to_include]
        if len(header_folders) == 1:  # require that file exist only in single folder
            str = '#include <{0}/{1}>'.format(header_folders[0], name_to_include)
            # print(line)
            # print(str)
            # print("---")
            return str
    return line


def different_lines_count(list1, list2):
    """
    Returns true if two lists are the same element wise, otherwise returns False.
    """
    diff_count = 0
    for x, y in zip(list1, list2):
        if x != y:
            diff_count += 1
    return diff_count


def process_file(filename, header_map):
    with open(filename, 'r') as fd:
        lines = [line.rstrip('\n') for line in fd]
        modified_lines = [fix_include_statement(line, header_map) for line in lines]

    fixed_lines = different_lines_count(lines, modified_lines)
    if fixed_lines > 0:
        with open(filename, 'w') as fd:
            for line in modified_lines:
                fd.write(line + "\n")

    print("Processing {}, fixed {} lines".format(filename, fixed_lines))


def process_source_code(source_dir, header_map):
    """
    Processes all *.h and *.cpp files from given source directory. Fix all header statement.
    """
    sources = get_source_files(source_dir)
    for filename in sources:
        process_file(filename, header_map)


def main():
    header_map = get_header_file_map(HEADER_LOCATION)
    print("{} header files have been found".format(len(header_map)))
    print(header_map)
    process_source_code(SOURCE_DIR_TO_MODIFY, header_map)


if __name__ == '__main__':
    main()
