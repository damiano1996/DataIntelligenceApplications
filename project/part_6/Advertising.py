import numpy as np

from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_2.GPTS_Learner_v2 import GPTS_Learner_v2
from project.part_2.Utils import compute_clairvoyant
from project.part_6.TemporaryConfig import max_bid


class Advertising:
    """
        This class is an extension of parts 2 and 3
    """

    def __init__(self, n_arms, subcampaign_idx):
        """
        :param n_arms:
        :param subcampaign_idx:
        """
        self.n_arms = n_arms

        self.sub_idx = subcampaign_idx
        self.bids = np.linspace(0, max_bid, self.n_arms)
        self.env = BiddingEnvironment(self.bids)

        self.learner = GPTS_Learner_v2(self.n_arms, self.bids)

        self.daily_clicks = 0
        self.optimal_daily_clicks = compute_clairvoyant(self.bids, 3, self.env)

    def get_daily_clicks(self, pulled_arm):
        """
            Retrieve the number of clicks of the corresponding learned and optimal budget allocation,
            then update the distribution
        :param pulled_arm
        """
        # Get current number of clicks and optimal number of clicks
        self.daily_clicks = self.env.round_single_arm(pulled_arm, self.sub_idx)

        # Update GP learner
        self.learner.update(pulled_arm, self.daily_clicks)

        return self.daily_clicks, self.optimal_daily_clicks
