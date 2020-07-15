import numpy as np

from project.dia_pckg.Utils import find_nearest
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_2.GPTS_Learner import GPTS_Learner
from project.part_2.Optimizer import fit_table
from project.part_6.TemporaryConfig import max_bid, max_clicks


class Advertising:
    """
        This class is an extension of parts 2 and 3
    """

    def __init__(self, n_arms, subcampaign_name):  # sub da togliere
        """
        :param n_arms:
        :param subcampaign_name:
        """
        self.n_arms = n_arms

        self.sub = subcampaign_name  # Da togliere quando ci sarà l'unione dei config

        self.bids = np.linspace(0, max_bid, self.n_arms)
        self.env = BiddingEnvironment(self.bids, max_clicks, sigma=6.0)

        self.learner = GPTS_Learner(self.n_arms, self.bids)

        self.daily_clicks = 0
        self.optimal_daily_clicks = 0

    def get_daily_clicks(self, pulled_arm):
        """
            Retrieve the number of clicks of the corresponding learned and optimal budget allocation,
            then update the distribution
        :param pulled_arm
        """
        # Get current number of clicks and optimal number of clicks
        optimal_arm = self.get_optimal_arm()
        self.daily_clicks = self.env.single_round(pulled_arm, self.sub)
        self.optimal_daily_clicks = self.env.single_round(optimal_arm, self.sub)

        # Update GPTS learner
        self.learner.update(pulled_arm, self.daily_clicks)

        return self.daily_clicks, self.optimal_daily_clicks

    # Da cambiare
    # Si può calcolare una volta sola... Da ottimizzare. Intanto sistemo per quello che mi serve.
    def get_optimal_arm(self):
        all_optimal_subs = np.ndarray(shape=(0, len(self.bids)), dtype=float)
        for i in range(0, 3):
            all_optimal_subs = np.append(all_optimal_subs, np.atleast_2d(self.env.subs[i](self.bids)), 0)

        optimals = fit_table(all_optimal_subs)[0]
        opt_allocation = optimals[self.sub]

        # conversion from percentage to arm
        allocation_bid = opt_allocation * max_bid
        nearest_allocation = find_nearest(self.bids, allocation_bid)
        optimal_pulled_arm = np.where(self.bids == nearest_allocation)[0][0]
        return optimal_pulled_arm
