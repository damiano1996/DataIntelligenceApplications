import numpy as np

from project.dia_pckg.SubCampaign import SubCampaign
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.dia_pckg.Config import *

# AbruptBiddingEnvironment is an extension of the BiddingEnvironment class
# It works in a scenario of multiple abrupt phases:
# for each sub-campaign returns the reward of a given pulled arm, depending on the phase we are


class AbruptBiddingEnvironment(BiddingEnvironment):

    def __init__(self, bids):
        self.bids = bids
        self.subs_objects = [SubCampaign(), SubCampaign(), SubCampaign()]
        self.subs = [self.subs_objects[0].bid, self.subs_objects[1].bid, self.subs_objects[2].bid]
        self.day = 0

    def reset(self):
        self.day = 0

    def phase(self):
        return (self.day / phaselen) % n_phases

    def round(self, pulled_arm1, pulled_arm2, pulled_arm3):

        pulled_arms = [pulled_arm1, pulled_arm2, pulled_arm3]
        rewards = np.array([])
        for i in range(0, len(pulled_arms)):
            avg_clicks = self.subs[i](self.bids[pulled_arms[i]], self.phase())
            reward = 0 if pulled_arms[i] == 0 else np.maximum(0, np.ceil(np.random.normal(
                avg_clicks, avg_clicks * noise_percentage)))
            rewards = np.append(rewards, reward)
        self.day = self.day + 1
        return rewards
