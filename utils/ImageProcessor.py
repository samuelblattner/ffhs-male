from skimage import io
from skimage.filters import threshold_mean
from skimage.transform import resize


class ImageProcessor:
    """
    Reads an image file and applies the following operations according to task requirements:
    1. Convert image to a Numpy array
    2. Convert image to gray scale
    3. Resize image to 10 by 10 Pixels
    4. Apply a threshold to convert gray scale to bitmap
    """

    # Settings
    __target_res = 10

    def __init__(self, target_res=10):
        """
        Init
        :param {int} target_res: Targeted resolution for the output bitmap
        """
        self.__target_res = target_res

    @staticmethod
    def __convert_to_array(image_file):
        """
        Convert a given image file to a Numpy array
        :param {file object} image_file: Pointer to an opened image file
        :return: {Numpy.ndarray} Array containing the color values of the individual image pixels
        """
        return io.imread(image_file)

    @staticmethod
    def __convert_to_grayscale(image_array):
        """
        Convert a given image array to grayscale (i.e. only one 'color' value).
        Note: Since rgb2gray ignores the alpha (transparency) channel, some images with black drawing (especially
        circles) will end up rendering the whole image black (since transparency is interpreted as 'nothing').
        We will set any transparent pixel to a white color, so that the black drawing can be recognized.
        :param {Numpy.ndarray} image_array: Input array to be converted
        :return: {Numpy.ndarray} Converted grayscale image array
        """
        # return rgb2gray(image_array)
        return [
            [255 if pixel[3] == 0 else sum(pixel[:3])/3 for pixel in row]
            for row in image_array
        ]

    @staticmethod
    def __apply_threshold(image_array):
        """
        Apply a mean threshold to the image information so that
        every mid-tones are converted to either black or white.
        :param {Numpy.ndarray} image_array: Input image array
        :return: {Numpy.ndarray} Bitmap containing only boolean values
        """
        return image_array > threshold_mean(image_array)

    def __scale_to_output_res(self, image_array):
        """
        Resize a given image array to a target resolution (default 10 Pixel)
        :param {Numpy.ndarray} image_array: Input image array to be resized
        :return: {Numpy.ndarray} Resized image
        """
        return resize(image_array, (self.__target_res, self.__target_res), mode='reflect')

    def process(self, image_file):
        """
        Main image processing routine.
        :param {file object} A file pointer to an opened image file to be processed.
        :return: {Numpy.ndarray} Resulting image
        """

        return self.__apply_threshold(
            self.__convert_to_grayscale(
                self.__scale_to_output_res(
                    self.__convert_to_array(image_file)
                )
            )
        )
