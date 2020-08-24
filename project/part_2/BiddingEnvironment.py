import numpy as np
from project.dia_pckg.Environment import Environment
from project.dia_pckg.SubCampaign import SubCampaign
from project.dia_pckg.Config import *


class BiddingEnvironment(Environment):
    def __init__(self, bids):
        self.bids = bids
        self.subs = [SubCampaign(), SubCampaign(), SubCampaign()]

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
