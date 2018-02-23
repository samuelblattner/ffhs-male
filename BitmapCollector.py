from os.path import basename, join

import math
import matplotlib.pyplot as plt

from utils.BitmapCSVExporter import BitmapCSVExporter
from utils.PNGImageIntake import PNGImageIntake
from utils.ImageProcessor import ImageProcessor


class BitmapCollector:
    __dest_dir = '.'
    __source_dir = './images'
    __output_res = 10

    __plot_dim_per_page = (5, 6)

    def __show_plot(self, bitmaps):
        """
        Simple 5x6 plot matrix to show image results.
        :param bitmaps: {list} list of bitmaps to plot.
        """

        plots_per_page = self.__plot_dim_per_page[0] * self.__plot_dim_per_page[1]

        for page in range(0, int(math.ceil(len(bitmaps) / plots_per_page))):

            page_plot_offset = page * plots_per_page

            fig, axes = plt.subplots(ncols=self.__plot_dim_per_page[0], nrows=self.__plot_dim_per_page[1], figsize=(10, 10))
            ax = axes.ravel()

            for b in range(page_plot_offset, page_plot_offset + max(len(bitmaps) - page_plot_offset, page_plot_offset)):
                ax[b - page_plot_offset].imshow(bitmaps[b][0], cmap=plt.cm.gray)
                ax[b - page_plot_offset].set_title(bitmaps[b][1], fontsize=8)

            for a in ax:
                a.axis('off')

            plt.show()

    def process(self, plot=False):
        """
        Main processing loop.
        :param plot: {bool} Set to true if image result should be plotted with mathplotlib.
        """

        bitmaps = []
        run = True
        intake = PNGImageIntake(source_dir=self.__source_dir).get_file_generator()
        image_processor = ImageProcessor(target_res=self.__output_res)
        csv_exporter = BitmapCSVExporter(filename=join(self.__dest_dir, 'export.csv'))

        print('Processing', end='', flush=True )
        while run:
            try:
                file = next(intake)
            except StopIteration:
                run = False
                continue

            bitmap = image_processor.process(file)
            bitmaps.append((bitmap, basename(file.name)))
            csv_exporter.append_bitmap(bitmap, basename(file.name))

            print('.', end='', flush=True)

        print('done.\n', flush=True)

        if plot:
            self.__show_plot(sorted(bitmaps, key=lambda b: b[1]))


bc = BitmapCollector()
bc.process(True)
