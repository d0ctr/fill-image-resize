# Package overview
This package is dedicated to solve problem of resizing images from one size and aspect ration to another in fancier way. This was inspired by Figma, where you can resize image using "Fill" type, so that image is not stretched.

## What happenes



## How to use
```python
from fill-image-resize import resize

path = 'image.png'
desired_width = 1020
desired_height = 1000
resized_image = resize(path, desired_width, desired_height)
resized_image.save('resized_image.png')