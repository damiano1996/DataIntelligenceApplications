import numpy as np

from project.part_2.GPTS_Learner import GP_Learner
from project.part_6.Pricing import Pricing


class SubCampaignHandler:

    def __init__(self, class_name, bids, prices, multiclasshandler):
        self.class_name = class_name
        self.learnerADV = GP_Learner(bids)
        self.prices = prices
        self.pricing = Pricing(class_name, multiclasshandler, len(prices), True)

    def get_daily_reward(self, clicks, arm_price):
        """
        From the purchases environment take the daily clicks and extract the number of purchases
        @param clicks: daily clicks
        @param arm_price: arm corresponding to the price proposed
        @return: number of purchases
        """
        return self.pricing.get_daily_revenue(clicks, arm_price)[0]

    def daily_update(self, arm_adv, clicks):
        """
        update the advertising learner with the information of the past day
        @param arm_adv: arm corresponding to the budget allocated on the sub-campaign
        @param clicks: click received from the sub-campaign
        """
        self.learnerADV.update(arm_adv, clicks)

    def get_estimated_clicks(self, adv_noise):
        """
        Compute the expected clicks for each possible arm adding a random noise to improve exploration
        @param adv_noise: arm corresponding to the budget
        @return: expected clicks
        """
        estimated_means = self.learnerADV.pull_arm_sequence()
        return np.random.normal(estimated_means,
                                [max([0, adv_noise * estimated_means[i]]) for i in range(len(estimated_means))])

    def get_estimated_cr(self, arm_price, cr_noise=0.0):
        """
        Given a price compute the expected coversion rate adding a random noise to improve exploration
        @param arm_price: arm corresponding to the price
        @param cr_noise: -not implemented
        @return: expected conversion rate
        """
        cr = self.pricing.learner.get_mean_reward_from_arm(arm_price)
        return np.random.normal(cr, max([0, cr_noise]))
