"""
Fix BornAgain documentation.
- Looks for markdown files recursively in given directory and changes shortcode: replace "{{%"  with "{{<"
"""
from utils import get_files
from utils import different_elements_count

# SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/BornAgain/BornAgain-website/content"
SOURCE_DIR_TO_MODIFY = "/home/pospelov/development/qt-mvvm/qt-mvvm/source/libmvvm_view"


def fix_highlight_line(line):
    if "highlightfile" in line:
        line = line.replace("{{%", "{{<")
        line = line.replace("%}}", ">}}")
    return line


def fix_cookbook_line(line):
    if "cookbook" in line:
        line = line.replace("cookbook", "examples")
    return line


def fix_word_line(line):
    pattern = "<mvvm_view_export.h>"
    if pattern in line:
        line = line.replace(pattern, "<mvvm/view_export.h>")
    return line

def process_file(filename, func):
    with open(filename, 'r') as fd:
        lines = [line.rstrip('\n') for line in fd]
        modified_lines = [func(line) for line in lines]
        if different_elements_count(lines, modified_lines) > 0:
            print(filename)
            with open(filename, 'w') as fd:
                for line in modified_lines:
                    fd.write(line + "\n")


def fix_highlight_shortcode():
    sources = get_files(SOURCE_DIR_TO_MODIFY, ".md")
    for filename in sources:
        process_file(filename, fix_highlight_line)


def fix_cookbook():
    sources = get_files(SOURCE_DIR_TO_MODIFY, ".md")
    for filename in sources:
        process_file(filename, fix_cookbook_line)


def fix_word():
    sources = get_files(SOURCE_DIR_TO_MODIFY, ".h")
    for filename in sources:
        process_file(filename, fix_word_line)


if __name__ == '__main__':
    # fix_highlight_shortcode()
#    fix_cookbook()
    fix_word()

