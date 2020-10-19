import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment


class Env7():

    def __init__(self, multi_class_handler, n_arms):
        """
        :param initial_date: when the campaign begins
        :param users_per_day: number of users per day
        :param multi_class_handler: MultiClassHandler object
        :param n_arms: number of arms of the Thomson Sampling algorithm
        """
        self.mch = multi_class_handler
        self.n_arms = n_arms
        self.arm_prices = n_arms_pricing

    def round(self, pulled_arm_price, clicks_per_class):
        """
        Returns reward x each class
            This method performs a round considering the number of steps per day
            Only after n rounds it perform a step in the implemented class
        :param pulled_arm_price: arm to pull
        :param clicks_per_class: dict of how many clicks on that day for each class
        :return: rewards: price * clicks * %ofbuy for each class
        """

        purchases = {}
        class_names = list(classes_config.keys())

        for cl, ck in enumerate(clicks_per_class):
            conv_rate = self.mch.get_class(class_name=class_names[cl]).conv_rates['phase_0']
            probability = conv_rate['probabilities'][pulled_arm_price]

            if probability < 0:
                probability = 1e-3

            purchases[class_names[cl]] = int(np.random.normal(probability, noise_std) * ck)

        return purchases

