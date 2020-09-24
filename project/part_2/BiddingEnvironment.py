import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.SubCampaign import SubCampaign


class BiddingEnvironment(Environment):

    def __init__(self, bids):
        self.bids = bids
        self.subs = [SubCampaign(bids=bids, sigma=noise_std, max_n_clicks=max_n_clicks),
                     SubCampaign(bids=bids, sigma=noise_std, max_n_clicks=max_n_clicks),
                     SubCampaign(bids=bids, sigma=noise_std, max_n_clicks=max_n_clicks)]
        self.day = 0

    def round(self, pulled_arms, phase=0):
        """
        For each sub-campaign, given the index of the pulled arm, i.e. the index of the bid chosen by the Learner,
        returns the reward
        @return: array of the rewards, one for each sub-campaign
        """
        clicks = [self.round_single_arm(pulled_arm, sub_idx, phase=phase) for sub_idx, pulled_arm in
                  enumerate(pulled_arms)]
        self.day = self.day + 1
        return np.asarray(clicks)

    def round_single_arm(self, pulled_arm, sub_idx, phase=0):
        received_clicks = np.random.normal(self.subs[sub_idx].means[f'phase_{phase}'][pulled_arm],
                                           self.subs[sub_idx].sigmas[f'phase_{phase}'][pulled_arm])
        received_clicks = 0 if received_clicks < 0 else received_clicks
        return int(received_clicks)

    def reset(self):
        self.day = 0

    def phase(self):
        return 0
