"""
Searches C++ include directives and adds prefix to them

#include "model.h"
will become
#include <mvvm/model/model.h>
"""
import os
from collections import defaultdict
from pathlib import Path
from utils import get_files
from utils import different_elements_count
import re

#SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/source/"
#SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/examples"
SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/tests"

APPLY_MODIFICATIONS = True


def get_source_files(dir_name):
    """
    Returns list of cpp and header files in given dir_name and its sub-folders.
    """
    return get_files(dir_name, ".h") + get_files(dir_name, ".cpp")


def find_include_statement(line):
    """
    Checks if line contains angle-like include statement and parse and returns file name from it.
    #include "modelview.h" ==> modelview.h
    """
    if "#include <mvvm" in line:
        matches = re.findall(r'\<(.+?)\>', line)
        if len(matches) == 1:
            return matches[0]
    return None


def fix_include_statement(line):
    """
    Replaces angle-based header statement with quote based.
    #include "<mvvm/model/path.h>" ==> #include "mvvm/model/path.h"
    """
    name_to_include = find_include_statement(line)
    if name_to_include:
        str = '#include \"{0}\"'.format(name_to_include)
        print(line)
        print(str)
        print("---")
        return str
    return line


def process_file(filename):
    with open(filename, 'r') as fd:
        lines = [line.rstrip('\n') for line in fd]
        modified_lines = [fix_include_statement(line) for line in lines]

    fixed_lines = different_elements_count(lines, modified_lines)
    if APPLY_MODIFICATIONS and fixed_lines > 0:
        with open(filename, 'w') as fd:
            for line in modified_lines:
                fd.write(line + "\n")

    print("Processing {}, fixed {} lines".format(filename, fixed_lines))


def process_source_code(source_dir):
    """
    Processes all *.h and *.cpp files from given source directory. Fix all header statement.
    """
    sources = get_source_files(source_dir)
    for filename in sources:
        process_file(filename)


def main():
    process_source_code(SOURCE_DIR_TO_MODIFY)


if __name__ == '__main__':
    main()
