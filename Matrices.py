import numpy as np


def calculate_sin_cos(angle):
    cosinus = np.cos(np.deg2rad(angle))
    sinus = np.sin(np.deg2rad(angle))
    return sinus, cosinus


def create_identity_matrix():
    return np.float32([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def create_translation_matrix(delta_x, delta_y):
    return np.float32([[1, 0, delta_x], [0, 1, delta_y], [0, 0, 1]])


def create_x_rotation_matrix(angle):
    sinus, cosinus = calculate_sin_cos(angle)
    return np.float32([[1, 0, 0], [0, cosinus, -sinus], [0, sinus, cosinus]])


def create_y_rotation_matrix(angle):
    sinus, cosinus = calculate_sin_cos(angle)
    return np.float32([[cosinus, 0, sinus], [0, 1, 0], [-sinus, 0, cosinus]])


def create_z_rotation_matrix(angle):
    sinus, cosinus = calculate_sin_cos(angle)
    return np.float32([[cosinus, -sinus, 0], [sinus, cosinus, 0], [0, 0, 1]])


def create_x_scale_matrix(scaling_factor):
    return np.float32([[scaling_factor, 0, 0], [0, 1, 0], [0, 0, 1]])


def create_y_scale_matrix(scaling_factor):
    return np.float32([[1, 0, 0], [0, scaling_factor, 0], [0, 0, 1]])


def create_z_scale_matrix(scaling_factor):
    return np.float32([[1, 0, 0], [0, 1, 0], [0, 0, 1 / scaling_factor]])


def create_scale_matrix(scaling_factor, axis):
    if axis == 'z':
        return create_x_scale_matrix(scaling_factor)
    elif axis == 'x':
        return create_y_scale_matrix(scaling_factor)
    elif axis == 'y':
        return create_z_scale_matrix(scaling_factor)
    else:
        raise AttributeError("Invalid axis")


def create_rotation_matrix(angle, axis='z'):
    if axis == 'z':
        return create_z_rotation_matrix(angle)
    elif axis == 'x':
        return create_x_rotation_matrix(angle)
    elif axis == 'y':
        return create_y_rotation_matrix(angle)
    else:
        raise AttributeError("Invalid axis")
