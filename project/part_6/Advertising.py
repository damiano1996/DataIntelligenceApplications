from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_6.TemporaryConfig import max_bid, max_clicks
from project.part_2.GPTS_Learner import GPTS_Learner

import numpy as np

class Advertising:
    """
        This class is an extension of parts 2 and 3
    """

    def __init__(self, n_arms_advertising, sub): #sub da togliere
        """
        :param n_arms_advertising
        :param n_subcampaigns
        """
        self.sub = sub #Da togliere quando ci sarà l'unione dei config

        self.bids = np.linspace(0, max_bid, n_arms_advertising)
        self.env = BiddingEnvironment(self.bids, max_clicks, sigma = 6.0)

        self.learner = GPTS_Learner(n_arms_advertising, self.bids)

    def get_num_clicks(self, learned_budget_allocation):
        """
        Retrieve the number of clicks of the corresponding learned budget allocation, 
        then update the distribution to search for best allocations
        :param learned_budget_allocation
        """
        round_clicks = self.env.single_round(learned_budget_allocation, self.sub)

        pulled = self.learner.pull_arm()
        clicks = self.env.single_round(pulled, self.sub)
        self.learner.update(pulled, clicks)

        return round_clicks

    def get_learner (self):
        return self.learner
