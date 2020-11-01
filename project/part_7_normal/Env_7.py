import numpy as np

from project.dia_pckg.Config import *

"""
Purchases Environment:
Each day compute the number of purchases for each class from the corresponding clicks
"""


class Env7():
    """
        multi_class_handler: keep the information and params for each class
        n_arms: number of different prices
    """

    def __init__(self, multi_class_handler, n_arms):
        self.mch = multi_class_handler
        self.n_arms = n_arms
        self.arm_prices = n_arms_pricing

    """
        pulled_arm_price: arm corresponding to the daily price
        clicks_per_class: number of clicks for each class
        return the purchases for each class
        return the purchases for each class
    """

    def round(self, pulled_arm_price, clicks_per_class):
        purchases = {}
        class_names = list(classes_config.keys())

        for cl, ck in enumerate(clicks_per_class):
            conv_rate = self.mch.get_class(class_name=class_names[cl]).conv_rates['phase_0']
            probability = conv_rate['probabilities'][self.get_true_index(pulled_arm_price)]

            if probability < 0:
                probability = 1e-3

            purchases[class_names[cl]] = int(np.random.normal(probability, noise_std) * ck)

        return purchases

    """
     pull_arm: selected arm
     returns the price corresponding to the selected arm
    """

    def get_true_index(self, pull_arm):
        arm_distance = int(self.mch.aggregate_demand_curve['prices'].shape[0] / self.n_arms)
        return int(arm_distance * pull_arm)
