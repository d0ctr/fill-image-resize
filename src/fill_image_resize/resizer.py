import math
from typing import Type

from PIL import Image


def resize(path: str, resulting_width: int, resulting_height: int) -> Image.Image:
    """
    Opens and resizes an image to the desired width and height

    This function uses Pillow to open file and resize it without distorting it.
    An example of such behaviour can be found in Figma, while managing an
    image you can select "Fill" type of transforming, thus your image
    wouldn't be stretched when altering aspect ratio, but resized and cropped.

    :param path: A filename (string), pathlib.Path object or a file object.
        The file object must implement ``file.read``, ``file.seek``,
        and ``file.tell`` methods, and be opened in binary mode.
    :param resulting_width: Must be > 0. The resulting width of returned image.
        Should be an integer.
    :param resulting_height: Must be > 0. The resulting height of returned image. 
        Should be an integer.
    :returns: An :py:class:`~PIL.Image.Image` object.
    :exception FileNotFoundError: If the file cannot be found. Or if the output
        format could not be determined from the file name.  Use the format
        option to solve this.
    :exception PIL.UnidentifiedImageError: If the image cannot be opened and
        identified.
    :exception ValueError: If a ``StringIO`` instance is used for ``fp``.
        Or if the output format could not be determined from the file name.
        Use the format option to solve this. Or if resulting_width or
        resulting_height is negative
    :exception OSError: If the file could not be written.  The file
        may have been created, and may contain partial data.
    """
    
    if resulting_width <= 0 or resulting_height <= 0:
        raise ValueError('resulting_width and resulting_height must be higher than zero')
    
    img = Image.open(path)

    width_original = img.width
    height_original = img.height

    scaling_factor = math.gcd(resulting_width, resulting_height)
    new_width_ratio = resulting_width / scaling_factor
    new_height_ratio = resulting_height / scaling_factor

    width_diff = width_original / new_width_ratio
    height_diff = height_original / new_height_ratio

    if width_diff >= height_diff:
        ratio_multiplier = height_diff
    else:
        ratio_multiplier = width_diff

    crop_width = ratio_multiplier * new_width_ratio
    crop_height = ratio_multiplier * new_height_ratio

    left = math.floor((img.width - crop_width) / 2)
    top = math.floor((img.height - crop_height) / 2)
    right = math.floor((img.width + crop_width) / 2)
    bottom = math.floor((img.height + crop_height) / 2)
    
    img = img.crop(box=(left, top, right, bottom))
    
    img = img.resize((resulting_width, resulting_height))
    
    return img
