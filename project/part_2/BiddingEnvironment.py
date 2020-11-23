import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.SubCampaign import SubCampaign


class BiddingEnvironment(Environment):

    def __init__(self, bids):
        """
        @param bids: array of possible bids for the advertising subcampaign
        """
        super().__init__(initial_date, n_days)
        self.bids = bids
        self.subs = [SubCampaign(bids=bids, sigma=noise_std, max_n_clicks=max_n_clicks),
                     SubCampaign(bids=bids, sigma=noise_std, max_n_clicks=max_n_clicks),
                     SubCampaign(bids=bids, sigma=noise_std, max_n_clicks=max_n_clicks)]
        self.day = 0

    def round(self, pulled_arms):
        """
        For each sub-campaign, given the index of the pulled arm, i.e. the index of the bid chosen by the Learner,
        returns the reward
        @param pulled_arms: pulled arm for each sub campaign
        @return: array of the rewards, one for each sub-campaign
        """
        clicks = [self.round_single_arm(pulled_arm, sub_idx, phase=self.phase()) for sub_idx, pulled_arm in
                  enumerate(pulled_arms)]
        self.day = self.day + 1
        return np.asarray(clicks)

    def round_single_arm(self, pulled_arm, sub_idx, phase=0):
        """
        Get the number of clicks received during a day with the bid corresponding to the pulled_arm
        for the sub campaign with index sub_idx
        @param pulled_arm: arm corresponding to the chosen bid
        @param sub_idx: index of the sub campaign
        @param phase: abrupt phase number
        @return: number of clicks received during a day
        """
        received_clicks = np.random.normal(self.subs[sub_idx].means[f'phase_{phase}'][pulled_arm],
                                           self.subs[sub_idx].sigmas[f'phase_{phase}'][pulled_arm])
        received_clicks = 0 if received_clicks < 0 else received_clicks
        return int(received_clicks)

    def get_optimal_clicks(self, idx, phase=0):
        """
        means for the clicks of the sub campaign ( without any noise )
        @param idx: index of the sub campaign
        @param phase: abrupt phase number
        @return: clicks for each possible bid
        """
        return self.subs[idx].means[f'phase_{phase}']

    def reset(self):
        """
        restart from day 0
        """
        self.day = 0

    def phase(self):
        """
        This environment keep the phase to the first one
        """
        return 0
