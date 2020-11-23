from project.part_2.GPTS_Learner import GPTS_Learner as GP_Learner
from project.part_2.Utils import compute_clairvoyant, get_idx_arm_from_allocation


class Advertising:
    """
        This class is an extension of parts 2 and 3, solves the advertising part of the algorithm
    """

    def __init__(self, bidding_environment, n_arms, subcampaign_idx):
        """
        :param n_arms:
        :param subcampaign_idx:
        """
        self.n_arms = n_arms
        self.sub_idx = subcampaign_idx

        self.env = bidding_environment

        self.learner = GP_Learner(self.env.bids)

        self.daily_clicks = 0
        self.optimal_clicks = self.get_optimal()
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

    def get_optimal(self):
        optimal_allocation = compute_clairvoyant(self.env, verbose=True)[0][self.sub_idx]
        hypothetical_pulled_arm = get_idx_arm_from_allocation(
            allocation=optimal_allocation,
            bids=self.env.bids)
        optimal_clicks = self.env.subs[self.sub_idx].means['phase_0'][hypothetical_pulled_arm]
        return optimal_clicks
