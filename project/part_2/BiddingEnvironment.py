import numpy as np
from project.dia_pckg.Environment import Environment
from project.dia_pckg.SubCampaign import SubCampaign
from project.dia_pckg.Config import *


class BiddingEnvironment(Environment):
    def __init__(self, bids, max):
        self.bids = bids
        self.max = max
        #self.subs = [self.bid_sub1, self.bid_sub2, self.bid_sub3]
        self.subs = [SubCampaign(max), SubCampaign(max), SubCampaign(max)]


    # def bid_sub1(self, x):
    #     return np.ceil(self.max * (1.0 - np.exp(-4 * x)))
    #
    # def bid_sub2(self, x):
    #     return np.ceil(self.max * (1.0 - np.exp(-5 * x)))
    #
    # def bid_sub3(self, x):
    #     return np.ceil(self.max * (1.0 - np.exp(-7 * x)))

    # for each sub-campaign, given the index of the pulled arm (i.e. the index of the bid chosen by the Learner)
    # returns the reward
    def round(self, pulled_arm1, pulled_arm2, pulled_arm3):
        rewards = np.array([])
        pulledarms = [pulled_arm1, pulled_arm2, pulled_arm3]

        for i in range(0, len(pulledarms)):
            avg_clicks = self.subs[i].bid(self.bids[pulledarms[i]])
            r = 0 if pulledarms[i] <= 0 else np.maximum(0, np.ceil(np.random.normal(
                avg_clicks, np.abs(avg_clicks * noise_percentage))))
            rewards = np.append(rewards, r)

        return rewards
