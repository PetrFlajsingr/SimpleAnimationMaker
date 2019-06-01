import cv2
import imageio as imageio
import numpy as np


def alpha_blend(fg, bg, alpha):
    fg = fg.astype("float")
    bg = bg.astype("float")
    alpha = alpha.astype("float") / 255

    fg = cv2.multiply(alpha, fg)
    bg = cv2.multiply(1 - alpha, bg)

    output = cv2.add(fg, bg)

    return output.astype("uint8")


def transparent_overlay(bg, fg):
    height, width = fg.shape[:2]

    overlay = np.zeros(bg.shape, dtype="uint8")
    overlay[:height, :width] = fg[:, :, :3]

    alpha = np.zeros(bg.shape[:2], dtype="uint8")
    alpha[:height, :width] = fg[:, :, 3]
    alpha = np.dstack([alpha] * 3)

    output = alpha_blend(overlay, bg, alpha)

    return output


class AnimationMaker:
    def __init__(self, path_to_save: str, config, queues, drawables):
        self.__config = config
        self.__queues = queues
        self.__drawables = drawables
        extension = path_to_save.split('.')[-1]
        frame_width, frame_height, _ = self.__drawables[0].get_original_image().shape
        if extension == 'gif':
            self.__video_writer = imageio.get_writer(path_to_save, mode='I')
        elif extension == 'mp4':
            self.__video_writer = cv2.VideoWriter(path_to_save, cv2.VideoWriter_fourcc(*'mp4v'), config['fps'],
                                                  (frame_width, frame_height))
        else:
            raise AttributeError('Invalid extension: ' + extension)
        self.__format = extension

    def __apply_actions(self):
        for queue in self.__queues:
            if not queue.is_done():
                queue.do_action()

    def __draw_drawables(self):
        out_img = None
        for drawable in self.__drawables:
            img = drawable.get_transformed_image()
            if out_img is None:
                width, height, _ = img.shape
                out_img = np.zeros((width, height, 3), dtype=img.dtype)

            out_img = transparent_overlay(out_img, img)
        return out_img

    def __save_frame(self):
        out_img = self.__draw_drawables()
        if self.__format == 'mp4':
            self.__video_writer.write(cv2.cvtColor(out_img, cv2.COLOR_RGBA2RGB))
        elif self.__format == 'gif':
            self.__video_writer.append_data(cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB))

    def create_animation(self):
        for i in range(0, self.__config['length']):
            self.__apply_actions()
            self.__save_frame()
            print("Frame:", i, "done")
        if self.__format == 'mp4':
            self.__video_writer.release()
