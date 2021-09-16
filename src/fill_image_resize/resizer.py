import math
from typing import Type

from PIL import Image


def resize(path: str, resulting_width: int, resulting_height: int) -> Image.Image:
    """
    Opens and resized an image to the desired width and height

    This function uses Pillow to open file and resize it without distring it.
    An example of such behaviour can be found in Figma, while managing an
    image you can select "Fill" type of transforming, thus your image
    wouldn't be stretched when altering aspect ratio, but resized and cropped.

    :param path: A filename (string), pathlib.Path object or a file object.
       The file object must implement ``file.read``,
       ``file.seek``, and ``file.tell`` methods,
       and be opened in binary mode.
    :param resulting_width: The resulting width of returned image. Should be 
        an integer.
    :param resulting_height: The resulting height of returned image. Should be 
        an integer.
    :returns: An :py:class:`~PIL.Image.Image` object.
    :exception FileNotFoundError: If the file cannot be found.
    :exception PIL.UnidentifiedImageError: If the image cannot be opened and
       identified.
    :exception ValueError: If the ``mode`` is not "r", or if a ``StringIO``
       instance is used for ``fp``.
    :exception TypeError: If ``formats`` is not ``None``, a list or a tuple.
    """
    
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
