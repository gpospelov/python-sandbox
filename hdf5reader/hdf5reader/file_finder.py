"""
FileFinder class: finds files on disk corresponding to given pattern.
"""
import glob


class FileFinder:
    def __init__(self, file_name_pattern, max_file_count=None):
        """
        Finds files on disk corresponding to given pattern.
        :param file_name_pattern: File name pattern for glob expression.
        :param max_file_count: Maximum number of files to return to the user.
        """
        if max_file_count and max_file_count <= 0:
            raise ValueError("Max number of requested files should be positive")

        self.files = list(glob.glob(file_name_pattern))
        if not len(self.files):
            raise ValueError("No files found according to '{}' pattern".format(file_name_pattern))

        self.max_file_count = min(len(self.files), max_file_count) if max_file_count else len(self.files)

    def get_files(self):
        """
        Returns list of files found.
        :return: List of full file names.
        """
        return self.files[0:self.max_file_count]

    def __len__(self):
        return self.max_file_count
