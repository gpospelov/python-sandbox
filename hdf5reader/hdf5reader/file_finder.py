import glob


class FileFinder:
    def __init__(self, file_name_pattern, max_file_count=None):
        """
        Finds files on disk corresponding to given pattern.
        :param file_name_pattern: File name pattern for glob expression.
        :param max_file_count: Maximum number of files to return to the user.
        """
        self.file_name_pattern = file_name_pattern
        self.max_file_count = max_file_count
        pass

    def get_files(self):
        """
        Returns list of files found.
        :return: List of full file names.
        """
        files = list(glob.glob(self.file_name_pattern))
        if not len(files):
            raise ValueError("No files found according to '{}' pattern".format(self.file_name_pattern))
        max_length = max(len(files), self.max_file_count)
        return files[0:max_length]
