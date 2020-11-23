"""
    This class extends LineBuilder to draw function on matplotlib figures.

    !!!!! Disclaimer !!!!!
    To draw on the matplotlib window you have to disable SciView on PyCharm:
    File -> Settings -> Tools -> Python Scientific -> deselect option
"""

import numpy as np
from matplotlib import pyplot as plt

from project.dia_pckg.chart_drawer.LineBuilder import LineBuilder


class FunctionBuilder(LineBuilder):

    def __init__(self, x_interval, y_interval):
        """
        :param x_interval: [x0, x1]
        :param y_interval: [y0, y1]
        """

        self.x_interval = x_interval
        self.y_interval = y_interval

        # initialize plot window
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim(x_interval[0], x_interval[1])
        ax.set_ylim(y_interval[0], y_interval[1])
        line, = ax.plot([], [])  # empty line
        super().__init__(line)

        self.last_xdata = x_interval[0]

    def start(self):
        plt.show()

    def __call__(self, event):
        if event.inaxes != self.line.axes:
            return
        if event.xdata < self.last_xdata:
            return

        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

        self.last_xdata = event.xdata

    def get_xydata(self):
        """
        :return: x, y as numpy arrays
        """
        x = self.line.get_xdata()
        y = self.line.get_ydata()
        return np.asarray(x), np.asarray(y)
