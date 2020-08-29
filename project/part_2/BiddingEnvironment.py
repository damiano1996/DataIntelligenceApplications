import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.SubCampaign import SubCampaign


class BiddingEnvironment(Environment):

    def __init__(self, bids):
        self.bids = bids
        self.subs = [SubCampaign(), SubCampaign(), SubCampaign()]

    def round(self, pulled_arms):
        """
        For each sub-campaign, given the index of the pulled arm, i.e. the index of the bid chosen by the Learner,
        returns the reward
        @return: array of the rewards, one for each sub-campaign
        """
        clicks = [self.round_single_arm(pulled_arm, i) for i, pulled_arm in enumerate(pulled_arms)]
        return np.asarray(clicks)

    def round_single_arm(self, pulled_arm, sub_idx):
        avg_clicks = self.subs[sub_idx].bid(self.bids[pulled_arm])
        clicks = 0 if pulled_arm <= 0 else np.maximum(0, np.ceil(np.random.normal(
            avg_clicks, np.abs(avg_clicks * noise_percentage))))
        return clicks
