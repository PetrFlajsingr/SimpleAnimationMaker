import cv2
import numpy as np
import Matrices


class Drawable2D:
    def __init__(self, img: np.array):
        self.__img = img
        self.__model_matrix = Matrices.create_identity_matrix()

    def reset_model_matrix(self):
        self.__model_matrix = Matrices.create_identity_matrix()

    def translate(self, delta_x, delta_y):
        translation_matrix = Matrices.create_translation_matrix(delta_x, delta_y)
        self.__model_matrix = np.matmul(translation_matrix, self.__model_matrix)

    def __move_to_origin(self):
        cols, rows, _ = self.__img.shape
        translation_to_origin_matrix = Matrices.create_translation_matrix(-cols / 2, -rows / 2)
        self.__model_matrix = np.matmul(translation_to_origin_matrix, self.__model_matrix)

    def __move_back_from_origin(self):
        cols, rows, _ = self.__img.shape
        translation_from_origin_matrix = Matrices.create_translation_matrix(cols / 2, rows / 2)
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
        cols, rows, _ = self.__img.shape
        return cv2.warpPerspective(self.__img, self.__model_matrix, (cols, rows))

    def get_original_image(self):
        return self.__img.copy()


class Drawable2DGroup:
    def __init__(self, drawables):
        self.__drawables = drawables

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
