import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment


class Env_7(Environment):

    def __init__(self, initial_date, multi_class_handler, n_arms):
        """
        :param initial_date: when the campaign begins
        :param users_per_day: number of users per day
        :param multi_class_handler: MultiClassHandler object
        :param n_arms: number of arms of the Thomson Sampling algorithm
        """
        super().__init__(initial_date, n_days)
        self.mch = multi_class_handler
        self.n_arms = n_arms
        self.arm_prices = self.get_candidate_prices()


    def round(self, pulled_arm_price, clicks_per_class):
        """
        Returns reward x each class
            This method performs a round considering the number of steps per day
            Only after n rounds it perform a step in the implemented class
        :param pulled_arm_price: arm to pull
        :param clicks_per_class: dict of how many clicks on that day for each class
        :return: rewards: price * clicks * %ofbuy for each class
        """

        rewards = {}
        optimals = {}

        for cl,ck in clicks_per_class:
            conv_rate = self.mch.get_class(class_name=cl).conv_rates['phase_0']
            probability = conv_rate['probabilities'][self.arm_prices['indices'][pulled_arm_price]]

            if (probability < 0):
                probability = 1e-3

            rewards[cl] = np.random.normal(probability, noise_std) * self.arm_prices['prices'][pulled_arm_price]

        super.step()
        return rewards,optimals

    def reset(self):
        """
            to reset the environment
        :return: None
        """
        self.current_idx = 0

    def get_candidate_prices(self):
        """
            This method return the candidate prices, one price for each arm.
            The "indices" array contains the positions of the specified prices in the aggregate curve
        :return:
        """
        arm_distance = int(self.mch.aggregate_demand_curve['prices'].shape[0] / self.n_arms)
        idx = [int(arm_distance * arm) for arm in range(self.n_arms)]
        prices = self.mch.aggregate_demand_curve['prices'][idx]
        return {'indices': idx, 'prices': prices}
