import numpy as np

from project.dia_pckg.Config import *
from project.part_2.GPTS_Learner import GPTS_Learner


class SubCampaignHandler:

    def __init__(self, class_name, bids, prices):
        self.class_name = class_name
        self.learnerADV = GPTS_Learner(bids)
        self.learnerCR = GPTS_Learner(prices)

    def daily_update(self, arm_price, arm_adv, clicks, purchases):
        self.learnerADV.update(arm_adv, clicks)
        self.learnerCR.update(arm_price, purchases)

    def get_estimated_clicks(self):
        estimated_means = self.learnerADV.pull_arm_sequence()
        return np.random.normal(estimated_means, [artificial_noise for i in range(len(estimated_means))])

    # TODO decidere se usare il artificial_noise anche qua
    def get_estimated_cr(self, arm_price):
        return np.random.normal(self.learnerCR.pull_arm(arm_price), artificial_noise)
