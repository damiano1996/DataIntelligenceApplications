from project.dia_pckg.Config import *
from project.part_2.BiddingEnvironment import BiddingEnvironment


# AbruptBiddingEnvironment is an extension of the BiddingEnvironment class
# It works in a scenario of multiple abrupt phases:
# for each sub-campaign returns the reward of a given pulled arm, depending on the phase we are


class AbruptBiddingEnvironment(BiddingEnvironment):

    def __init__(self, bids):
        """
        @param bids: array of possible bids for the advertising subcampaign
        """
        super(AbruptBiddingEnvironment, self).__init__(bids=bids)
        self.day = 0

    def phase(self):
        """
        compute the current phase
        @return: current phase
        """
        d = self.day
        p = 0
        for p, phase_l in enumerate(phase_lens):
            d -= phase_l
            if d < 0:
                return p
        return int(p)

    def round(self, pulled_arms):
        return super(AbruptBiddingEnvironment, self).round(pulled_arms)
