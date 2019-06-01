import cv2
import numpy as np

from AnimationMaker import AnimationMaker
from TransformActionBuilders import TransformQueueActionBuilder
from Drawable2D import Drawable2D


def show_and_wait(img, delay=0):
    cv2.imshow('img', img)
    cv2.waitKey(delay)


def main():
    img = cv2.imread("/Users/petr/Desktop/test.png", cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (400, 400))
    obj = Drawable2D(img)

    builder2 = TransformQueueActionBuilder(obj)
    queue2 = builder2 \
        .begin_loop(100)\
            .begin_loop(10)\
                .once()\
                    .combine_start()\
                        .translate(1, 0)\
                        .translate(0, 1)\
                    .combine_end()\
            .end_loop()\
            .once()\
                .rotate(1, 'z')\
        .end_loop()\
        .build()

    white = np.zeros([400, 400, 4], dtype=np.uint8)
    white.fill(255)
    white_obj = Drawable2D(white)

    config = {
        'length': 600,
        'fps': 60
    }
    maker = AnimationMaker('/Users/petr/Desktop/test.gif', config, [queue2], [white_obj, obj])
    maker.create_animation()


if __name__ == '__main__':
    main()
