import numpy as np

from project.part_2.GP_Learner import GP_Learner


class SubCampaignHandler:

    def __init__(self, class_name, bids, prices):
        self.class_name = class_name
        self.learnerADV = GP_Learner(bids)
        self.learnerCR = GP_Learner(prices)

    def daily_update(self, arm_price, arm_adv, clicks, purchases):
        self.learnerADV.update(arm_adv, clicks)
        self.learnerCR.update(arm_price, purchases)

    def get_estimated_clicks(self, adv_noise):
        estimated_means = self.learnerADV.pull_arm_sequence()
        return np.random.normal(estimated_means, [adv_noise for i in range(len(estimated_means))])

    def get_estimated_cr(self, arm_price, cr_noise):
        return np.random.normal(self.learnerCR.pull_arm(arm_price), cr_noise)
