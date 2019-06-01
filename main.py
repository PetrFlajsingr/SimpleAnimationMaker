import cv2
import numpy as np

from AnimationMaker import AnimationMaker, TimeToFramesConverter
from TransformActionBuilders import TransformActionQueueBuilder
from Drawable2D import Drawable2D


def show_and_wait(img, delay=0):
    cv2.imshow('img', img)
    cv2.waitKey(delay)


def main():
    img1 = cv2.imread("/Users/petr/Desktop/test.png", cv2.IMREAD_UNCHANGED)
    img1 = cv2.resize(img1, (400, 400))
    drawable1 = Drawable2D(img1)

    builder1 = TransformActionQueueBuilder(drawable1, TimeToFramesConverter(fps=60))
    queue1 = builder1 \
        .each(5).translate(1, 0)\
        .interpolate(5).scale(0.5, 'y')\
        .build()

    img2 = cv2.imread("/Users/petr/Desktop/test2.png", cv2.IMREAD_UNCHANGED)
    img2 = cv2.resize(img2, (400, 400))
    drawable2 = Drawable2D(img2)

    builder2 = TransformActionQueueBuilder(drawable2, TimeToFramesConverter(fps=60))
    queue2 = builder2\
        .begin_loop(10)\
            .interpolate(1).scale(0.5, 'y')\
            .interpolate(1).scale(2, 'y')\
        .end_loop()\
        .build()

    white = np.zeros([400, 400, 4], dtype=np.uint8)
    white.fill(255)
    white_obj = Drawable2D(white)

    config = {
        'length': 600,
        'fps': 60
    }
    maker = AnimationMaker('/Users/petr/Desktop/test.mp4', config, [queue1, queue2], [white_obj, drawable1, drawable2])
    maker.create_animation()


if __name__ == '__main__':
    main()
