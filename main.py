import cv2
import numpy as np

from AnimationMaker import AnimationMaker
from DrawEvents import TransformQueueActionBuilder
from Drawable2D import Drawable2D


def show_and_wait(img, delay=0):
    cv2.imshow('img', img)
    cv2.waitKey(delay)


def main():
    img = cv2.imread("/Users/petr/Desktop/test.png", cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (100, 100))
    obj = Drawable2D(img)

    builder2 = TransformQueueActionBuilder(obj)
    queue2 = builder2 \
        .begin_loop(10) \
            .each(10).translate(1, 0) \
            .each(10).translate(-1, 0) \
            .begin_loop(90) \
                .once().rotate(1, 'z') \
            .end_loop() \
        .end_loop() \
        .build()

    white = np.zeros([100, 100, 4], dtype=np.uint8)
    white.fill(255)
    white_obj = Drawable2D(white)

    config = {
        'length': 600,
        'fps': 60
    }
    maker = AnimationMaker('/Users/petr/Desktop/test.mp4', config, [queue2], [white_obj, obj])
    maker.create_animation()


if __name__ == '__main__':
    main()
