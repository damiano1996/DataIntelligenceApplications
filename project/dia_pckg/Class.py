import matplotlib.pyplot as plt
import numpy as np

from project.dia_pckg.Product import Product
from project.dia_pckg.Utils import polynomial


class Class:
    def __init__(self, class_name, product):
        """
        :param class_name:
        :param product:
        """
        self.name = class_name

        self.conv_rate = self.get_conversion_rate(product.base_price, product.max_price)

    def get_conversion_rate(self, product_base_price, product_max_price, n_steps=3, polynomial_rank=10):
        """
            Function to generate the conversion rate of the class
        :param product_base_price: minimum price of the product
        :param product_max_price: maximum price of the product
        :param n_steps: number of intervals to keep the same convertion rate
        :param polynomial_rank: rank of the polynomial for the approximation of the steps, to obtain a curve
        :return: tuple containing the x-axis: prices and the y-axis: conversion rate
        """
        prices = np.linspace(product_base_price, product_max_price, product_max_price - product_base_price)
        y = np.zeros(shape=prices.shape)

        steps_idx = np.sort(np.random.randint(0, prices.shape[0], n_steps))
        last_step_idx = 0
        last_value = 1.0
        for step_idx in steps_idx:
            value = np.random.uniform(last_value / 2, last_value)
            y[last_step_idx:step_idx] = value
            last_value = value
            last_step_idx = step_idx

        demand_curve = polynomial(y, rank=polynomial_rank)

        return (prices, demand_curve)

    def plot_conversion_rate(self):
        plt.title(f'Conversion Curve - Class name: {self.name}')
        plt.plot(self.conv_rate[0], self.conv_rate[1])
        plt.xlabel('Price')
        plt.ylabel('Conversion Rate')
        plt.show()


if __name__ == '__main__':
    # example
    my_class = Class('class_name', Product('product_name', 100, 500))
    my_class.plot_conversion_rate()
