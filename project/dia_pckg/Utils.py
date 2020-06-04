import os

import numpy as np


def polynomial(y, rank):
    """
        Polynomial approximation
    :param y: vector to smooth
    :param rank: rank of the poly
    :return:
    """
    x = range(len(y))
    coeffs = np.polyfit(x, y, rank)
    new_y = []
    for xi in x:
        new_xi = 0

        for i in range(rank + 1):
            coef = coeffs[len(coeffs) - 1 - i]
            new_xi += coef * xi ** i
        new_y.append(new_xi)

    return np.asarray(new_y)


def check_if_dir_exists(path, create=False):
    """
    :param path: directory path
    :param create: create dir if does not exist?
    :return:
    """
    if not os.path.isdir(path):
        if create:
            os.mkdir(path)
        return False
    else:
        return True


def check_if_file_exists(path, create=False):
    """
    :param path: file path
    :param create: create file if does not exist?
    :return:
    """
    if not os.path.exists(path):
        if create:
            file = open(path, 'w')
            file.close()
        return False
    else:
        return True
