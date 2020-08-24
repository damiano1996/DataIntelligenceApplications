import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.SubCampaign import SubCampaign


class BiddingEnvironment(Environment):

    def __init__(self, bids):
        self.bids = bids
        self.subs = [SubCampaign(), SubCampaign(), SubCampaign()]

    def round(self, pulled_arm1, pulled_arm2, pulled_arm3):
        """
        For each sub-campaign, given the index of the pulled arm, i.e. the index of the bid chosen by the Learner,
        returns the reward
        @param pulled_arm1: index of pulled arm for sub-campaign 1
        @param pulled_arm2: index of pulled arm for sub-campaign 2
        @param pulled_arm3: index of pulled arm for sub-campaign 3
        @return: array of the rewards, one for each sub-campaign
        """
        rewards = np.array([])
        pulledarms = [pulled_arm1, pulled_arm2, pulled_arm3]

        for i in range(0, len(pulledarms)):
            avg_clicks = self.subs[i].bid(self.bids[pulledarms[i]])
            r = 0 if pulledarms[i] <= 0 else np.maximum(0, np.ceil(np.random.normal(
                avg_clicks, np.abs(avg_clicks * noise_percentage))))
            rewards = np.append(rewards, r)

        return rewards
