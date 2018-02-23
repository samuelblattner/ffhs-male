import csv
from itertools import chain


class BitmapCSVExporter:
    """
    Exporter that appends bitmap rows to a CSV file.
    """

    # Settings
    __csv_file_name = None

    # References
    __csv_file = None
    __csv_writer = None

    def __init__(self, filename):
        """
        Init.
        :param filename: {str} Name of the export file.
        """
        self.__csv_file_name = filename

    def __del__(self):
        """
        Del, cleanup.
        """
        self.__close_csv()

    @staticmethod
    def __convert_boolean_list(boolean_list):
        """
        Convert a list of booleans to '1's and '0's.
        1 - Character, foreground
        0 - Background
        :param boolean_list: {List} Input list.
        :return: {List} List of '1's and '0's
        """
        return ['0' if b else '1' for b in boolean_list]

    def __open_csv(self):
        """
        Open the CSV-file and create a writer.
        """
        self.__csv_file = open(self.__csv_file_name, 'w', encoding='utf-8')
        self.__csv_writer = csv.writer(self.__csv_file, delimiter=',', )

    def __close_csv(self):
        """
        Close the opened CSV-file.
        :return:
        """
        if self.__csv_file is not None:
            try:
                self.__csv_file.close()
            except IOError:
                pass
        self.__csv_file = None

    def append_bitmap(self, bitmap, bitmap_name):
        """
        Append a row with bitmap information according to task specification.
        :param bitmap: {Numpy.nparray} Bitmap to write to CSV.
        :param bitmap_name: {str} Name of source file.
        """

        if self.__csv_file is None:
            self.__open_csv()

        self.__csv_writer.writerow([bitmap_name] + self.__convert_boolean_list(list(chain(*bitmap))))
