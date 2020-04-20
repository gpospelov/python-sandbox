"""
Replace specific line in whole code base.
"""
from .utils import get_files
from .utils import different_elements_count


CONTENT_TO_REPLACE = "#include <mvvm/model/mvvm_export.h>"
REPLACEMENT = "#include <mvvm/core/export.h>"
SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/source"
APPLY_MODIFICATIONS = True


def replace_line(line):
    if CONTENT_TO_REPLACE in line:
        return REPLACEMENT
    return line


def process_file(filename):
    """
    Reads a file and replaces all specific lines.
    """
    with open(filename, 'r') as fd:
        lines = [line.rstrip('\n') for line in fd]
        modified_lines = [replace_line(line) for line in lines]

    fixed_lines = different_elements_count(lines, modified_lines)
    if APPLY_MODIFICATIONS and fixed_lines > 0:
        with open(filename, 'w') as fd:
            for line in modified_lines:
                fd.write(line + "\n")

    print("Processing {}, fixed {} lines".format(filename, fixed_lines))


def main():
    sources = get_files(SOURCE_DIR_TO_MODIFY, ".h")
    for filename in sources:
        process_file(filename)


if __name__ == '__main__':
    main()
