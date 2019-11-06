"""
Updates header section in C++ source files
"""
from utils import get_files
from utils import different_elements_count


NEW_HEADER = [
    u"// ************************************************************************** //",
    u"//",
    u"//  Model-view-view-model framework for large GUI applications",
    u"//",
    u"//! @license   GNU General Public License v3 or higher (see COPYING)",
    u"//! @authors   see AUTHORS",
    u"//",
    u"// ************************************************************************** //"
    ]

SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/examples"
# SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/tests"
APPLY_MODIFICATIONS = True


def get_current_header(lines):
    result = []
    for line in lines:
        print(line)
        if line.startswith("//"):
            result.append(line)
        else:
            break
    return result


def process_file(filename):
    with open(filename, 'r') as fd:
        lines = [line.rstrip('\n') for line in fd]
        current_header = get_current_header(lines)
        # if len(current_header) != 8:
        #     print(len(current_header), filename)
        #     return False

    new_content = list(NEW_HEADER)
    if len(current_header) == 0:
        new_content.append("")
    new_content = new_content + lines[len(current_header):]
    print(lines)
    print(new_content)

    fixed_lines = different_elements_count(lines, new_content)
    if APPLY_MODIFICATIONS and fixed_lines > 0:
        with open(filename, 'w') as fd:
            for line in new_content:
                fd.write(line + "\n")

    return True


def main():
    sources = get_files(SOURCE_DIR_TO_MODIFY, ".h") + get_files(SOURCE_DIR_TO_MODIFY, ".cpp")
    files_to_fix = []
    for filename in sources:
        result = process_file(filename)
        if not result:
            files_to_fix.append(filename)
    print("Have to fix files ", files_to_fix)


if __name__ == '__main__':
    main()
