from project.part_2.GPTS_Learner import GPTS_Learner
from project.part_2.Utils import compute_clairvoyant


class Advertising:
    """
        This class is an extension of parts 2 and 3
    """

    def __init__(self, bidding_environment, n_arms, subcampaign_idx):
        """
        :param n_arms:
        :param subcampaign_idx:
        """
        self.n_arms = n_arms
        self.sub_idx = subcampaign_idx

        self.env = bidding_environment

        self.learner = GPTS_Learner(self.n_arms, self.env.bids)

        self.daily_clicks = 0
        self.optimal_clicks = compute_clairvoyant(self.env, verbose=True) / 3
        # division by three because the function returns the total optimal number of clicks,
        # but we need only the optimal for a single sub-campaign if we want to to compute the regret!

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

        return self.daily_clicks
