import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import figaspect

from project.dia_pckg.Config import features_space
from project.dia_pckg.Utils import polynomial


class Class:

    def __init__(self, class_name, class_features, product, n_abrupt_phases, summary=True):
        """
        :param class_name: name of the class
        :param class_features: binary features of the class
        :param product: Product object
        :param n_abrupt_phases: number of abrupt phases
        :param summary: boolean to print the summary of the informations of the class
        """
        self.name = class_name
        self.features = class_features

        self.product = product
        self.n_abrupt_phases = n_abrupt_phases

        # here we generate one conversion curve for each phase
        self.conv_rates = [self.get_conversion_rate(self.product.base_price,
                                                    self.product.max_price) for _ in range(self.n_abrupt_phases)]

        if summary:
            self.print_summary()

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
        last_value = 0.90
        for step_idx in steps_idx:
            value = np.random.uniform(last_value / 2, last_value)
            y[last_step_idx:step_idx] = value
            last_value = value
            last_step_idx = step_idx

        probabilities = polynomial(y, rank=polynomial_rank)
        # using the polynomial approximation sometime the curve can oscillate near zero
        # to avoid this problem we find the first zero and set all the next values equal to zero
        first_zero = np.where(probabilities <= 0)[0]
        if first_zero.shape[0] > 0:
            probabilities[first_zero[0]:] = 0

        # to rescale between 0 and 1
        # probabilities = probabilities / np.max(probabilities)

        return (np.asarray(prices), np.asarray(probabilities))

    def plot_conversion_rate(self):
        """
            This function plots the curves of the different abrupt phases
        :return:
        """
        w, h = figaspect(0.2)

        fig, axs = plt.subplots(1, self.n_abrupt_phases, figsize=(w, h))
        fig.suptitle(f'Conversion Curves - Class name: {self.name}', y=1.)

        for n in range(self.n_abrupt_phases):
            axs[n].set_title(f'Phase: {n + 1}')
            axs[n].set_ylim(0, 1)
            axs[n].plot(self.conv_rates[n][0],
                        self.conv_rates[n][1])
            axs[n].set_xlabel('Price')
            axs[n].set_ylabel('Conversion Rate')

        fig.show()

    def print_summary(self):
        """
            This function prints a summary of this class
        :return:
        """
        features_meaning = []
        for i, bin in enumerate(self.features):
            feat_value = features_space[list(features_space.keys())[i]][bin]
            features_meaning.append(feat_value)

        summary = f'---------------------------------\n' \
                  f'Class name: {self.name}\n' \
                  f'Feature values: {features_meaning}\n' \
                  f'Number of abrupt phases: {self.n_abrupt_phases}\n' \
                  f'---------------------------------\n'
        print(summary)
