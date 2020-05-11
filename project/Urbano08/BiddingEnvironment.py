import numpy as np


class BiddingEnvironment():

    def __init__(self, bids, max, sigma):
        self.bids = bids
        self.sigma = sigma
        self.max = max

    def bid_sub1(self,x):
        return self.max * (1.0 - np.exp(-(8 * x)))

    def bid_sub2(self,x):
        return self.max * (1.0 - np.exp(-(5 * x)))

    def bid_sub3(self,x):
        return self.max * (1.0 - np.exp(-(3 * x)))


    def round(self, pulled_arm1,pulled_arm2, pulled_arm3):

        return (np.random.normal(self.bid_sub1(pulled_arm1), self.sigma) ,
               np.random.normal(self.bid_sub2(pulled_arm2), self.sigma) ,
               np.random.normal(self.bid_sub3(pulled_arm3), self.sigma) )
