from project.dia_pckg.Config import *
from project.part_2.BiddingEnvironment import BiddingEnvironment


# AbruptBiddingEnvironment is an extension of the BiddingEnvironment class
# It works in a scenario of multiple abrupt phases:
# for each sub-campaign returns the reward of a given pulled arm, depending on the phase we are


class AbruptBiddingEnvironment(BiddingEnvironment):

    def __init__(self, bids):
        super(AbruptBiddingEnvironment, self).__init__(bids=bids)
        self.day = 0

    def reset(self):
        self.day = 0

    def phase(self):
        d = self.day
        p = 0
        for p, phase_l in enumerate(phase_lens):
            d -= phase_l
            if d < 0:
                return p
        return p
    #(self.day / phase_len) % n_abrupts_phases

    def round(self, pulled_arms):
        return super(AbruptBiddingEnvironment, self).round(pulled_arms, int(self.phase()))
