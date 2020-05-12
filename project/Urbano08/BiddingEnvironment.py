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
        return self.max * (1.0 - np.exp(-0.9 * x))

    def round(self, pulled_arm1, pulled_arm2, pulled_arm3):

        return np.array([np.maximum(0,np.random.normal(self.bid_sub1(self.bids[pulled_arm1]), self.sigma)),
                np.maximum(0,np.random.normal(self.bid_sub2(self.bids[pulled_arm2]), self.sigma)),
                np.maximum(0,np.random.normal(self.bid_sub3(self.bids[pulled_arm3]), self.sigma))])

