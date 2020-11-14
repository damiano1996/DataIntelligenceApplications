import numpy as np

from project.part_2.GP_Learner import GP_Learner
from project.part_7.SubCampaignHandler import SubCampaignHandler as subh


class Normal_SubCampaignHandler(subh):

    def __init__(self, class_name, bids, prices, multiclasshandler):
        super().__init__(class_name, bids, prices, multiclasshandler)
        self.learnerCR = GP_Learner(prices)

    def comlete_daily_update(self, arm_price, arm_adv, clicks, purchases):
        """
        update the learners with the information gathered the past day
        @param arm_price: arm corresponding to the price proposed
        @param arm_adv: arm corresponding to the budget allocated on the sub-campaign
        @param clicks: click received from the sub-campaign
        @param purchases: purchases received from the sub-campaign
        """
        self.learnerADV.update(arm_adv, clicks)
        self.learnerCR.update(arm_price, purchases)

    def get_estimated_cr(self, arm_price, cr_noise=0.0):
        """
        get the predicted conversion rate of a specific price
        @param arm_price: arm corresponding to the price we want the conversion rate of
        @param cr_noise: artificial noise to add exploration
        @return: computed conversion rate
        """
        return np.random.normal(self.learnerCR.pull_arm(arm_price), cr_noise)
