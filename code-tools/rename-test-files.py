"""
Rename test files
TestSessionModel.cpp -> sessionmodel.test.cpp
"""
from utils import get_files
from utils import different_elements_count
import os

SOURCE_LOCATION = "/home/pospelov/development/qt-mvvm/qt-mvvm/source"
TESTS_LOCATION = "/home/pospelov/development/qt-mvvm/qt-mvvm/tests/viewmodel"


def get_base_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def get_simplified_test_name(filename):
    """
    path/TestViewModel.cpp -> viewmodel
    """
    return get_base_name(filename).replace('Test', '').lower()


def is_valid_test_file(filename, sources):
    if not get_base_name(filename).startswith("Test"):
        return False

    simplified_test_name = get_simplified_test_name(filename)

    # checks if there is source file with same name
    for src in sources:
        srcbase = get_base_name(src)
        if simplified_test_name == srcbase:
            return True

    return False


def process_file(filename, sources):
    if not is_valid_test_file(filename, sources):
        return False

    newname = os.path.join(os.path.dirname(filename), get_simplified_test_name(filename)+".test.cpp")
    print(filename, get_simplified_test_name(filename), newname)
    os.rename(filename, newname)
    return True


def main():
    sources = get_files(SOURCE_LOCATION, ".h")
    tests = get_files(TESTS_LOCATION, ".cpp")
    files_to_fix = []
    for filename in tests:
        result = process_file(filename, sources)
        if not result:
            files_to_fix.append(filename)
    print("Have to fix files ", files_to_fix)


if __name__ == '__main__':
    main()
