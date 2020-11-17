"""
    Here we have general functions that are used in different classes.
"""

import os

import numpy as np


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


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
