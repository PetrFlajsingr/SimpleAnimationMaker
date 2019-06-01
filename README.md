# SimpleAnimationMaker
A simple module to create animations.

This is a practice project for builder pattern. The entire animation is created using builders.

TODOs: 
* support for images of different sizes

Images are drawn in the order they are passed into the `AnimationMaker`. Multiple queues and drawable objects can be created.

Usage:
```python
import cv2
import numpy as np

from AnimationMaker import AnimationMaker
from Drawable2D import Drawable2D
from TransformActionBuilders import TransformQueueActionBuilder

image = cv2.imread('path/to/image.gif') # or .mp4
drawable = Drawable2D(image)

builder = TransformQueueActionBuilder(drawable)
queue = builder \
    .interpolate(10).scale(2, 'x')\ # interpolate scaling by the factor of 2 over 10 frames
    .begin_loop(10) \ # loop over next section 10 times
        .each(10).translate(1, 0) \ # do translation for 10 frames
        .each(10).translate(-1, 0) \ # do translation for 10 frames
        .begin_loop(90) \ # inner loop repeated 90 times
            .once().rotate(1, 'z') \ # rotate image by 1 degree
        .end_loop() \
    .end_loop() \
    .each(10).combine_start()\ #create combined transformation and run it 10 times
        .scale(0.4, 'z')\
        .translate(10, -1)\
    .combine_end()\
    .build()
    
white = np.zeros([100, 100, 4], dtype=np.uint8)
white.fill(255)
background = Drawable2D(white)
    
config = {
    'length': 600,
    'fps': 60
}
maker = AnimationMaker('path/to/save', config, [queue], [background, drawable])
maker.create_animation()
```
