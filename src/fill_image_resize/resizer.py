import math
from PIL import Image

def resize(path, resulting_width, resulting_height):
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

  left = (img.width - crop_width) / 2
  top = (img.height - crop_height) / 2
  right = (img.width + crop_width) / 2
  bottom = (img.height + crop_height) / 2
  
  img = img.crop(box=(left, top, right, bottom))
  
  img = img.resize((resulting_width, resulting_height))
  
  return img
