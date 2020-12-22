"""
Update header guards in large C++ project basic on folder location.
"""
from utils import get_files
from utils import different_elements_count
from pathlib import Path
import os


#SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/source"
SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/DaRefl/DaRefl/source/darefl"
APPLY_MODIFICATIONS = True


def count_occurrences(lines, pattern):
    result = 0
    for line in lines:
        if pattern in line:
            result = result + 1
    return result


def is_valid_header_file(lines):
    """
    Returns true if header file has simple layout and can be processed automatically.
    """
    if count_occurrences(lines, "#ifndef") == 1 and \
            count_occurrences(lines, "#define") == 1 and \
            count_occurrences(lines, "#endif"):
        return True
    return False


def construct_header_guard_name(filename):
    """
    Returns name of header guard file basing on file name and location.
    """
    parts = Path(os.path.dirname(filename)).parts
    name = os.path.splitext(os.path.basename(filename))[0].replace('-', '')

    result = '{0}_{1}_{2}_H'.format(parts[-2].upper(), parts[-1].upper(), name.upper())
    return result


def fix_include_guard(line, new_guard_name):
    statements = ["#ifndef", "#define", "#endif"]
    for statement in statements:
        if statement in line:
            if "endif" in line:
                return '{} // {}'.format(statement, new_guard_name)
            else:
                return '{} {}'.format(statement, new_guard_name)
    return line


def process_file(filename):
    with open(filename, 'r') as fd:
        lines = [line.rstrip('\n') for line in fd]
        if not is_valid_header_file(lines):
            print("File {0} should be fixed manually.".format(construct_header_guard_name(filename)))
            return False
        guard_name = construct_header_guard_name(filename)
        modified_lines = [fix_include_guard(line, guard_name) for line in lines]
        print("File {0}, guard {1} ".format(filename, construct_header_guard_name(filename)))

    print(lines)
    print(modified_lines)

    fixed_lines = different_elements_count(lines, modified_lines)
    if APPLY_MODIFICATIONS and fixed_lines > 0:
        with open(filename, 'w') as fd:
            for line in modified_lines:
                fd.write(line + "\n")

    print("Processing {}, fixed {} lines".format(filename, fixed_lines))
    return True


def main():
    sources = get_files(SOURCE_DIR_TO_MODIFY, ".h")
    files_to_fix = []
    for filename in sources:
        result = process_file(filename)
        if not result:
            files_to_fix.append(filename)
    print("Have to fix files ", files_to_fix)


if __name__ == '__main__':
    main()
