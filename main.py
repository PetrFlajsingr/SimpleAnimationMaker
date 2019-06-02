from copy import copy

import cv2
import numpy as np

from AnimationMaker import AnimationMaker, TimeToFramesConverter
from TransformActionBuilders import TransformActionQueueBuilder
from Drawable2D import Drawable2D, Drawable2DGroup


def show_and_wait(img, delay=0):
    cv2.imshow('img', img)
    cv2.waitKey(delay)


def main():
    fps = 60
    img1 = cv2.imread("/Users/petr/Desktop/test.png", cv2.IMREAD_UNCHANGED)
    img1 = cv2.resize(img1, (400, 400))
    drawable1 = Drawable2D(img1)

    builder2 = TransformActionQueueBuilder(drawable1, TimeToFramesConverter(fps=fps))
    queue2 = builder2\
        .interpolate(1).fade_out()\
        .interpolate(2.5).fade_in()\
        .build()

    white = np.zeros([400, 400, 4], dtype=np.uint8)
    white.fill(255)
    white_obj = Drawable2D(white)

    config = {
        'length': 300,
        'fps': fps
    }
    maker = AnimationMaker('/Users/petr/Desktop/test.mp4', config, [queue2], [white_obj, drawable1])
    maker.create_and_save()


if __name__ == '__main__':
    main()
