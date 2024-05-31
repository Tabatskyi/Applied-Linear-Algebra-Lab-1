import math
import cv2
import numpy as np
from matplotlib import pyplot as plt


def show_matrices(matrices: list, labels: list, save=False):
    fig = plt.figure()
    max_value = np.max(matrices)
    min_value = np.min(matrices)

    if all(matrix.shape[1] == 3 for matrix in matrices):
        axis = fig.add_subplot(111, projection='3d')
        for i, matrix in enumerate(matrices):
            xs, ys, zs = matrix[:, 0], matrix[:, 1], matrix[:, 2]
            axis.plot(xs, ys, zs, label=labels[i])

        axis.set_xlabel('X')
        axis.set_ylabel('Y')
        axis.set_zlabel('Z')
        axis.set_xlim(min_value, max_value)
        axis.set_ylim(min_value, max_value)
        axis.set_zlim(min_value, max_value)
    elif all(matrix.shape[1] == 2 for matrix in matrices):
        axis = fig.add_subplot(111)
        for i, matrix in enumerate(matrices):
            xs, ys = matrix[:, 0], matrix[:, 1]
            axis.plot(xs, ys, label=labels[i])
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xlim(min_value, max_value)
        plt.ylim(min_value, max_value)
    else:
        raise ValueError("Impossible to show this matrices.")

    if not save:
        plt.grid(True)
        plt.legend()
    else:
        plt.axis('off')
        plt.savefig('plot.png', bbox_inches='tight')
    plt.show()


def transform_by_matrix(original_matrix: np.array, transform_matrix: np.array, operation_label='Transformed'):
    if original_matrix.shape[1] == transform_matrix.shape[0]:
        transformed_matrix = np.dot(original_matrix, transform_matrix)
    elif original_matrix.shape[0] == transform_matrix.shape[1]:
        transformed_matrix = np.dot(transform_matrix, original_matrix)
    else:
        raise ValueError("Impossible to multiply this matrices.")

    show_matrices([original_matrix, transformed_matrix], ['Original', operation_label])


def scale_matrix(original_matrix: np.array, scales: list):
    trans_matrix = np.diag(scales)
    transform_by_matrix(original_matrix, trans_matrix, f"Scaled by {scales}")


def rotate_matrix(original_matrix: np.array, angle: float, axis='y'):
    angle_rad = math.radians(angle)
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)

    if original_matrix.shape[1] == 2:
        trans_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    elif original_matrix.shape[1] == 3:
        match axis:
            case 'x':
                trans_matrix = np.array([[1, 0, 0], [0, cos_a, -sin_a], [0, sin_a, cos_a]])
            case 'y':
                trans_matrix = np.array([[cos_a, 0, sin_a], [0, 1, 0], [-sin_a, 0, cos_a]])
            case 'z':
                trans_matrix = np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]])
    else:
        raise ValueError("Rotation only supports 2D or 3D matrices.")

    transform_by_matrix(original_matrix, trans_matrix, f"Rotated by {angle}º around axis {axis}")


def reflect_matrix(original_matrix: np.array, axes: list):
    axes_names = np.array(['x', 'y', 'z'])
    reflect_vector = [-1 if axis else 1 for axis in axes]
    if len(axes) == 2:
        axes.append(False)
    trans_matrix = np.diag(reflect_vector)
    transform_by_matrix(original_matrix, trans_matrix, f"Reflected across {axes_names[axes]}")


def angle_matrix(original_matrix: np.array, k: float, fixed_axis: int, variable_axis: int):
    trans_matrix = np.eye(original_matrix.shape[1])
    trans_matrix[variable_axis, fixed_axis] = k
    transform_by_matrix(original_matrix, trans_matrix, f"Angled by {k} along {fixed_axis} axis")


def show_image(image):
    plt.imshow(image)
    plt.show()

def rotate_image(image, angle):
    (height, width) = image.shape[:2]
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (width, height), borderMode=cv2.BORDER_REPLICATE)


def scale_image(image, scale_x, scale_y):
    height, width = image.shape[:2]
    new_width = int(width * scale_x)
    new_height = int(height * scale_y)

    return cv2.resize(image, (new_width, new_height))


def reflect_image(image, axis):
    if axis == 'x':
        return cv2.flip(image, 0)
    elif axis == 'y':
        return cv2.flip(image, 1)
    else:
        raise ValueError("Axis must be 'x' or 'y'.")


def angle_image(image, k, axis):
    (height, width) = image.shape[:2]
    if axis == 'x':
        src_points = np.float32([[0, 0], [width, 0], [0, height]])
        dst_points = np.float32([[0, 0], [width, 0], [k * height, height]])
    else:
        src_points = np.float32([[0, 0], [width, 0], [0, height]])
        dst_points = np.float32([[0, 0], [width, k * width], [0, height]])

    matrix = cv2.getAffineTransform(src_points, dst_points)
    return cv2.warpAffine(image, matrix, (width, height), borderMode=cv2.BORDER_REPLICATE)


def rotate_matrix_opencv(image, angle, scale=1.0):
    matrix = cv2.getRotationMatrix2D((0, 0), angle, scale)
    return cv2.transform(np.array([image]), matrix)[0]


def scale_matrix_opencv(image, scale):
    return rotate_matrix_opencv(image, 0, scale)


def reflect_matrix_opencv(image, axis):
    if axis == 'x':
        return cv2.flip(image, 0)
    elif axis == 'y':
        return cv2.flip(image, 1)
    else:
        raise ValueError("Axis must be 'x' or 'y'.")


def angle_matrix_opencv(image, k, axis):
    (height, width) = image.shape[:2]

    if axis == 'x':
        src_points = np.float32([[0, 0], [width, 0], [0, height]])
        dst_points = np.float32([[0, 0], [width, 0], [k * height, height]])
    else:
        src_points = np.float32([[0, 0], [width, 0], [0, height]])
        dst_points = np.float32([[0, 0], [width, k * width], [0, height]])

    matrix = cv2.getAffineTransform(src_points, dst_points)

    transformed_image = cv2.transform(np.array([image]), matrix)[0]
    return transformed_image


batman = np.array([[0, 0], [1, 0.2], [0.4, 1], [0.5, 0.4], [0, 0.8], [-0.5, 0.4], [-0.4, 1], [-1.5, 0.5], [0, 0]])
rotate_matrix(batman, 45)
scale_matrix(batman, [2, 2])
reflect_matrix(batman, [False, True])
angle_matrix(batman, 2, 0, 1)

trans_matrix = np.array([[0, 1], [1, 0]])
transform_by_matrix(batman, trans_matrix, f"Transformed by {trans_matrix} matrix")

cube = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 1], [1, 1, 1], [0, 1, 1], [0, 0, 1]])

rotate_matrix(cube, 45, 'x')
rotate_matrix(cube, 45, 'y')
rotate_matrix(cube, 45, 'z')
scale_matrix(cube, [1, 2, 1])
reflect_matrix(cube, [True, True, False])
angle_matrix(cube, 1, 2, 1)

# plot = cv2.imread('plot.png')
rotated = rotate_matrix_opencv(batman, 45)
show_matrices([batman, rotated], ['Original', f"Rotated by 45º (OpenCV)"])

scaled = scale_matrix_opencv(batman, 2)
show_matrices([batman, scaled], ['Original', f"Scaled by [2, 2] (OpenCV)"])

reflected = reflect_matrix_opencv(batman, 'y')
show_matrices([batman, reflected], ['Original', f"Reflected by y (OpenCV)"])

angled = angle_matrix_opencv(batman, 1, 'x')
show_matrices([batman, angled], ['Original', f"Scaled by [2, 2] (OpenCV)"])

rick = cv2.imread('rick.png')
angled_rick = angle_image(rick, 0.5, 'x')
reflected_rick = reflect_image(angled_rick, 'y')
rotated_rick = rotate_image(reflected_rick, 90)
show_image(rotated_rick)


rick2 = cv2.imread('rick.png')
rotated_rick2 = rotate_image(rick2, 90)
reflected_rick2 = reflect_image(rotated_rick2, 'y')
angled_rick2 = angle_image(reflected_rick2, 0.5, 'x')

show_image(angled_rick2)
