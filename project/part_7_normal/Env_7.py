import numpy as np

from project.dia_pckg.Config import *


class Env7:
    """
    Each day compute the number of purchases for each class from the corresponding clicks
    """

    def __init__(self, multi_class_handler, n_arms):
        """

        @param multi_class_handler: keep the information and params for each class
        @param n_arms: number of different prices
        """
        self.mch = multi_class_handler
        self.n_arms = n_arms
        self.arm_prices = n_arms_pricing

    def round(self, pulled_arm_price, clicks_per_class):
        """

        @param pulled_arm_price: arm corresponding to the daily price
        @param clicks_per_class: number of clicks for each class during the day
        @return: purchases for each class during the day
        """
        purchases = {}
        class_names = list(classes_config.keys())

        for cl, ck in enumerate(clicks_per_class):
            conv_rate = self.mch.get_class(class_name=class_names[cl]).conv_rates['phase_0']
            probability = conv_rate['probabilities'][self.get_true_index(pulled_arm_price)]

            if probability < 0:
                probability = 1e-3

            noise = np.sqrt(probability * (1 - probability) * ck)
            purchases[class_names[cl]] = int(np.random.normal(probability * ck, noise))

        return purchases

    def get_true_index(self, pull_arm):
        """
        @param pull_arm: selected arm
        @return: the price corresponding to the selected arm
        """
        arm_distance = int(self.mch.aggregate_demand_curve['prices'].shape[0] / self.n_arms)
        return int(arm_distance * pull_arm)
