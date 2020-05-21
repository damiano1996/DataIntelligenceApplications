import numpy as np


class BiddingEnvironment():

    def __init__(self, bids, max, sigma):
        self.bids = bids
        self.sigma = sigma
        self.max = max
        self.subs = [self.bid_sub1,self.bid_sub2,self.bid_sub3]

    def bid_sub1(self, x):
        # return self.max * (1.0 - np.exp(-(4 * x)))
        return self.max * (1.0 - np.exp(-4 * x))

    def bid_sub2(self, x):
        return self.max * (1.0 - np.exp(-5 * x))

    def bid_sub3(self, x):
        return self.max * (1.0 - np.exp(-7 * x))

    def round(self, pulled_arm1, pulled_arm2, pulled_arm3):
        rewards = np.array([])
        pulledarms = [pulled_arm1,pulled_arm2,pulled_arm3]

        for i in range(0,pulledarms):
            r = 0 if pulledarms[i] == 0 else np.maximum(0,np.random.normal(self.bid_sub[i](self.bids[pulledarms[i]]), self.sigma))
            rewards = np.append(rewards,r)

        return rewards

