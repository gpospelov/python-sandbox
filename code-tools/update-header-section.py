"""
Updates header section in C++ source files
"""
from utils import get_files
from utils import different_elements_count
import os


# NEW_HEADER = [
#     u"// ************************************************************************** //",
#     u"//",
#     u"//  Operational Applications UI Foundation",
#     u"//",
#     u"// ************************************************************************** //"
#     ]

NEW_HEADER = [
    u"/******************************************************************************",
    u" *",
    u" * Project       : Operational Applications UI Foundation",
    u" *",
    u" * Description   : The model-view-viewmodel library of generic UI components",
    u" *",
    u" * Author        : Gennady Pospelov <gennady.pospelov@gmail.com>",
    u" *",
    u" *****************************************************************************/"
]


WORKDIR= "/home/pospelov/development/iter/sequencer-mvvm"
SOURCES = ["tests/libtestmachinery", "tests/testmvvm_model", "tests/testmvvm_viewmodel", "tests/testmvvm_sequencer", 
"source/libmvvm_model", "source/libmvvm_viewmodel", "source/libmvvm_sequencer", "examples"]

skip_files = ["AttributeMap.h", "AttributeMap.cpp",  "AttributeMap-tests.cpp", 
"TreeData.h", "TreeData.cpp", "TreeData-tests.cpp"]

APPLY_MODIFICATIONS = True

def get_current_header(lines):
    result = []
    for line in lines:
        print(line)
        if line.startswith("//") or line.startswith("/*") or line.startswith(" *"):
            result.append(line)
        else:
            break
    return result


def process_file(filename):
    for pattern in skip_files:
        if pattern in filename:
            return False

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


def fix_folder(dirname):
    sources = get_files(dirname, ".h") + get_files(dirname, ".cpp")
    files_to_fix = []
    for filename in sources:
        result = process_file(filename)
        if not result:
            files_to_fix.append(filename)
    print("Have to fix files ", files_to_fix)


def main():
    for dir in SOURCES:
        dirname = os.path.join(WORKDIR, dir)
        fix_folder(dirname)


if __name__ == '__main__':
    main()
