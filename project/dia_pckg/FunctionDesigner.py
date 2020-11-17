"""
    This class is used to design functions by hand on the matplotlib figures.
"""

import matplotlib.pyplot as plt
import numpy as np

from project.dia_pckg.Utils import polynomial
from project.dia_pckg.chart_drawer.FunctionBuilder import FunctionBuilder


def design_function(x_interval, y_interval, density=1., poly_apprx=True, rank=5, plot_result=True):
    """
        This method is to draw a function by hand.
    :param x_interval: [x0, x1]
    :param y_interval: [y0, y1]
    :param density: delta between points
    :param poly_apprx: boolean to allow polynomial approximation of the step function
    :param rank: rank of the polynomial approximation
    :param plot_result: boolean to plot or not the final result
    :return:
    """
    fun = FunctionBuilder(x_interval, y_interval)
    fun.start()

    x_points, y_points = fun.get_xydata()
    if plot_result: plt.plot(x_points, y_points, linestyle='--', label=f'Original samples - {x_points.shape[0]} points')

    x = np.arange(x_interval[0], x_interval[1], density)
    y = np.zeros(x.shape)

    # step function to increase the definition of the function
    y[0:] = y_points[0]
    for i in range(1, x_points.shape[0]):
        xi = np.where(x >= x_points[i - 1])[0][0]
        xii = np.where(x >= x_points[i])[0][0]
        y[xi:xii] = y_points[i]
    y[xii:] = y_points[-1]

    if plot_result: plt.plot(x, y, label=f'Steps - {x.shape[0]} points')

    if poly_apprx:
        y = polynomial(y, rank)
        if plot_result:
            plt.plot(x, y, label='Polynomial approximation')
    if plot_result: plt.show()

    return x, y


def save_function(x, y, path):
    """
    :param x:
    :param y:
    :param path: path with .npy extension
    :return:
    """
    with open(path, 'wb') as f:
        np.save(f, x)
        np.save(f, y)


def load_function(path):
    """
    :param path: path with .npy extension
    :return:
    """
    with open(path, 'rb') as f:
        x = np.load(f)
        y = np.load(f)
        return x, y


if __name__ == '__main__':
    # test
    x, y = design_function(x_interval=[0, 100],
                           y_interval=[0, 1],
                           density=1,
                           poly_apprx=True,
                           rank=5,
                           plot_result=True)

    save_function(x, y, 'test.npy')
    x, y = load_function('test.npy')
    plt.plot(x, y)
    plt.show()
