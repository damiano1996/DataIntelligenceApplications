"""
    This class is used to design functions by hand on the matplotlib figures.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from project.dia_pckg.chart_drawer.FunctionBuilder import FunctionBuilder


def design_function(x_interval, y_interval, density=1., plot_result=True):
    """
        This method is to draw a function by hand.
    :param x_interval: [x0, x1]
    :param y_interval: [y0, y1]
    :param density: delta between points
    :param plot_result: boolean to plot or not the final result
    :return:
    """
    try:
        fun = FunctionBuilder(x_interval, y_interval)
        fun.start()

        # drawn data
        x_drawn, y_drawn = fun.get_xydata()

        # adding values on the margin
        x_drawn = np.append(x_interval[0], x_drawn)
        x_drawn = np.append(x_drawn, x_interval[1])

        y_drawn = np.append(y_drawn[0], y_drawn)
        y_drawn = np.append(y_drawn, y_drawn[-1])

        if plot_result: plt.plot(x_drawn, y_drawn, linestyle='--',
                                 label=f'Original samples - {x_drawn.shape[0]} points')

        # creation of the interpolation function
        f = interp1d(x_drawn, y_drawn, kind='cubic')

        # new x and y
        x_new = np.arange(x_interval[0], x_interval[1], density)
        y_new = f(x_new)

        y_new = np.where(y_new > 1, 1, y_new)
        y_new = np.where(y_new < 0, 0, y_new)

        if plot_result: plt.plot(x_new, y_new, label=f'Cubic interpolation')

        if plot_result: plt.show()

        return x_new, y_new

    except:
        again = input('Something went wrong... Would you like to draw again?\n [Y/n]')
        if again == 'Y' or again == 'y' or again == 'yes':
            return design_function(x_interval, y_interval, density=density, plot_result=plot_result)


def save_function(x, y, path):
    """
    :param x:
    :param y:
    :param path: path with .npy extension
    :return:
    """
    np.save(path, np.stack([x, y], axis=-1))


def load_function(path):
    """
    :param path: path with .npy extension
    :return:
    """
    xy = np.load(path)
    x = xy[:, 0]
    y = xy[:, 1]
    return x, y


if __name__ == '__main__':
    # test
    x, y = design_function(x_interval=[0, 100],
                           y_interval=[0, 1],
                           density=1,
                           plot_result=True)

    save_function(x, y, 'test.npy')
    x, y = load_function('test.npy')
    plt.plot(x, y)
    plt.show()
