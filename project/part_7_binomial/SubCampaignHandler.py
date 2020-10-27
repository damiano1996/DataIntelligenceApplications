import numpy as np

from project.part_2.GPTS_Learner import GPTS_Learner
from project.part_6.Pricing import Pricing


class SubCampaignHandler:

    def __init__(self, class_name, bids, prices, multiclasshandler):
        self.class_name = class_name
        self.learnerADV = GPTS_Learner(bids)
        self.prices = prices
        self.pricing = Pricing(class_name, multiclasshandler, len(prices), True)

    def get_daily_reward(self, clicks, arm_price):
        return self.pricing.get_daily_revenue(clicks, arm_price)[0]

    def daily_update(self, arm_adv, clicks):
        self.learnerADV.update(arm_adv, clicks)

    def get_estimated_clicks(self, adv_noise):
        estimated_means = self.learnerADV.pull_arm_sequence()
        return np.random.normal(estimated_means, [adv_noise for i in range(len(estimated_means))])

    def get_estimated_reward(self, arm_price):
        return self.pricing.learner.get_mean_reward_from_arm(arm_price) * self.prices[arm_price]
