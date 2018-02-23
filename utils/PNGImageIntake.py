from os import walk
import re
from os.path import join, abspath


class PNGImageIntake:
    """
    Simple directory walker implementation to
    provide a PNG-File generator.
    """

    # Settings
    __filename_pattern = r'\.png$'

    # State
    __file_walker = None

    def __init__(self, source_dir='.'):
        """
        Init.
        :param source_dir: {str} Directory in which to iterate over PNG-files.
        """
        self.__file_walker = walk(source_dir)

    def get_file_generator(self):
        """
        Creates a generator to return PNG-files one by one.
        :return: {generator} File generator
        """

        def file_generator():
            root, dirs, files = next(self.__file_walker)
            for file in files:
                if re.search(self.__filename_pattern, file, re.IGNORECASE):
                    with open(abspath(join(root, file)), 'rb') as f:
                        yield f

        return file_generator()
