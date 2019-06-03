import cv2
import numpy as np
import Matrices


class Drawable2D:
    def __init__(self, img: np.array):
        self.__img = img
        self.__model_matrix = Matrices.create_identity_matrix()
        self.alpha = 1.0

    def add_to_alpha(self, value):
        self.alpha += value
        if self.alpha < 0:
            self.alpha = 0
        elif self.alpha > 1.0:
            self.alpha = 1.0

    def reset_model_matrix(self):
        self.__model_matrix = Matrices.create_identity_matrix()

    def translate(self, delta_x, delta_y):
        translation_matrix = Matrices.create_translation_matrix(delta_x, delta_y)
        self.__model_matrix = np.matmul(translation_matrix, self.__model_matrix)

    def __move_to_origin(self):
        cols, rows, _ = self.__img.shape
        translation_to_origin_matrix = Matrices.create_translation_matrix(-rows / 2, -cols / 2)
        self.__model_matrix = np.matmul(translation_to_origin_matrix, self.__model_matrix)

    def __move_back_from_origin(self):
        cols, rows, _ = self.__img.shape
        translation_from_origin_matrix = Matrices.create_translation_matrix(rows / 2, cols / 2)
        self.__model_matrix = np.matmul(translation_from_origin_matrix, self.__model_matrix)

    def rotate(self, angle, axis):
        rotation_matrix = Matrices.create_rotation_matrix(angle, axis)
        self.__move_to_origin()
        self.__model_matrix = np.matmul(rotation_matrix, self.__model_matrix)
        self.__move_back_from_origin()

    def scale(self, scaling_factor, axis):
        scale_matrix = Matrices.create_scale_matrix(scaling_factor, axis)
        self.__move_to_origin()
        self.__model_matrix = np.matmul(scale_matrix, self.__model_matrix)
        self.__move_back_from_origin()

    def get_transformed_image(self):
        img_copy = self.__img.copy()
        height, width, _ = img_copy.shape
        img_copy[:, :, 3] = (img_copy[:, :, 3] * self.alpha).astype(np.uint8)
        return cv2.warpPerspective(img_copy, self.__model_matrix, (width, height))

    def get_original_image(self):
        return self.__img.copy()


class Drawable2DGroup:
    def __init__(self, drawables):
        self.__drawables = drawables

    def add_to_alpha(self, value):
        for drawable in self.__drawables:
            drawable.add_to_alpha(value)

    def reset_model_matrix(self):
        for drawable in self.__drawables:
            drawable.reset_model_matrix()

    def translate(self, delta_x, delta_y):
        for drawable in self.__drawables:
            drawable.translate(delta_x, delta_y)

    def rotate(self, angle, axis):
        for drawable in self.__drawables:
            drawable.rotate(angle, axis)

    def scale(self, scaling_factor, axis):
        for drawable in self.__drawables:
            drawable.scale(scaling_factor, axis)
