import matplotlib.pyplot as plt
import numpy as np

from project.dia_pckg.Class import Class
from project.dia_pckg.Product import Product


class SubCampaign:
    def __init__(self, Class):
        self.Class = Class

    def define_clicks_over_budget(self, max_n_click, max_budget, zero_perc, full_perc, noise, length):
        """
            Generate the clicks over budget curve associated to the sub campaign
        :param max_n_click: Define the maximum number of click of the curve
        :param max_budget: Define the maximum budget of the curve
        :param zero_perc: Define the percentage of the curve (first part) that is zero
        :param full_perc: Define the percentage of the curve (last part) that is at the max_n_click
        :param noise: Noise applied to the curve
        :param length: Number of budgetes evalueted by the curve
        :return:
        """
        budget = np.linspace(0, max_budget, length)

        zero = np.zeros(int(length * zero_perc))

        line = np.linspace(0, max_n_click, int(length * (full_perc - zero_perc)))
        noise = np.random.normal(0, noise, int(length * (full_perc - zero_perc)))
        line = line + noise

        plate = np.full(length - len(line) - len(zero), max_n_click)

        clicks = np.append(zero, line)
        clicks = np.append(clicks, plate)
        self.cob_curve = (budget, clicks)

    def plot_clicks_over_budget(self):
        plt.plot(self.cob_curve[0], self.cob_curve[1])
        plt.show()


if __name__ == '__main__':
    prod = Product('shoes', 30)

    c1 = Class('elegant')
    c1.get_conversion_rate(prod, 0.85, 0.01, 50)

    c1.plot_conversion_rate()

    sub = SubCampaign(c1)
    sub.define_clicks_over_budget(50, 100, 0.3, 0.8, 0.5, 50)

    sub.plot_clicks_over_budget()
