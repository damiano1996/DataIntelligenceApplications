import numpy as np

from project.part_2.GPTS_Learner import GPTS_Learner
from project.dia_pckg.Config import *


class SubCampaignHandler:


    def __init__(self, class_name, bids, prices):
        self.class_name = class_name
        self.learnerADV = GPTS_Learner(bids)
        self.learnerCR = GPTS_Learner(prices)

    def daily_update(self,arm_price, arm_adv, clicks, purchases):
        self.learnerADV.update(arm_adv, clicks)
        self.learnerCR.update(arm_price, purchases)

    def get_estimated_clicks(self):
        return self.learnerADV.pull_arm_sequence()

    def get_estimated_cr(self, arm_price):
        return self.learnerCR.pull_arm(arm_price)






