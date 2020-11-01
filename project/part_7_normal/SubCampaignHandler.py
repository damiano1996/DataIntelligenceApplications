import numpy as np

from project.part_2.GP_Learner import GP_Learner
from project.part_7_binomial.SubCampaignHandler import SubCampaignHandler as subh


class SubCampaignHandler(subh):

    def __init__(self, class_name, bids, prices, multiclasshandler):
        super().__init__(class_name, bids, prices, multiclasshandler)
        self.learnerCR = GP_Learner(prices)

    def comlete_daily_update(self, arm_price, arm_adv, clicks, purchases):
        self.learnerADV.update(arm_adv, clicks)
        self.learnerCR.update(arm_price, purchases)

    def get_estimated_cr(self, arm_price, cr_noise):
        return np.random.normal(self.learnerCR.pull_arm(arm_price), cr_noise)
