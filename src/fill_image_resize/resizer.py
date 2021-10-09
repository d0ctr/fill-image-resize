import math
import requests
from typing import Optional
from io import BytesIO

from PIL import Image, UnidentifiedImageError


class BadPathError(Exception):
    """Base class for errors connected with provided path."""
    
    def __init__(self, message = 'Can not get an image by provided path'):
        self.message = message
        super().__init__(self.message)

class BadLinkError(Exception):
    """Exception is raised for bad image URLs"""

    def __init__(self, message='Can not get an image by provided URL'):
        self.message = message
        super().__init__(self.message)

class BadImageError(Exception):
    """Exception is raised when can provided file is not an image"""
    
    def __init__(self, message='This is not an image'):
        self.message = message
        super().__init__(self.message)


def resize(path: str, resulting_width: int, resulting_height: int, save: Optional[str] = None) -> Image.Image:
    """
    Opens and resizes an image to the desired width and height

    This function uses Pillow to open a file or extract an image from bytes
    and resize it without distorting it.
    An example of such behaviour can be found in Figma, while managing an
    image you can select "Fill" type of transforming, thus your image
    wouldn't be stretched when altering aspect ratio, but resized and cropped.

    :param path: A filename (string) or URL. If it is an URL must start with 
        'HTTP' or 'HTTPS'.
    :param resulting_width: Must be > 0. The resulting width of returned image. 
        Should be an integer.
    :param resulting_height: Must be > 0. The resulting height of returned image. 
        Should be an integer.
    :param save: Optional filename (string) for saving file.
    :returns: A tuned :py:class:`~PIL.Image.Image` object (has a field `original`
        containing an original image of the same type).
    :exception BadPathError: If the file cannot be found. Or if the output
        format could not be determined from the file name.  Use the format
        option to solve this.
    :exception BadImageError: If the image cannot be opened and
        identified.
    :excpetion BadLinkError: If can not get an image from url.
    :exception ValueError: If a ``StringIO`` instance is used for ``fp``.
        Or if the output format could not be determined from the file name.
        Use the format option to solve this. Or if resulting_width or
        resulting_height is negative
    :exception OSError: If the file could not be written.  The file
        may have been created, and may contain partial data.
    """
    
    if resulting_width <= 0 or resulting_height <= 0:
        raise ValueError('resulting_width and resulting_height must be higher than zero')
    
    if path[0:4] == 'http':
        res = requests.get(path)
        if res.status_code == 200:
            path = BytesIO(res.content) # this is actually bad but never mind
        else:
            raise BadLinkError

    try:
        img_original = Image.open(path)
    except FileNotFoundError:
        raise BadPathError
    except UnidentifiedImageError:
        raise BadImageError

    width_original = img_original.width
    height_original = img_original.height

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

    left = math.floor((width_original - crop_width) / 2)
    top = math.floor((height_original - crop_height) / 2)
    right = math.floor((width_original + crop_width) / 2)
    bottom = math.floor((height_original + crop_height) / 2)
    
    img = img_original.copy().crop(box=(left, top, right, bottom))
    
    img = img.resize((resulting_width, resulting_height))

    if (save):
        img.save(save)
    img.original = img_original
    
    return img
