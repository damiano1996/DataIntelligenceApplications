import numpy as np


class AbruptBiddingEnvironment():

    def __init__(self, bids, max, sigma):
        self.bids = bids
        self.sigma = sigma
        self.max = max
        self.subs = [self.bid_sub1,self.bid_sub2,self.bid_sub3]
        self.day = 0
        self.phaselen = 60
        self.n_phases = 3

    def phase(self):
        return (self.day / self.phaselen)% self.n_phases

    def bid_sub1(self, x, phase = 0):
        if phase == 0:
            return self.max * (1.0 - np.exp(-4 * x))
        elif phase == 1:
            return self.max * (1.0 - np.exp(-2 * x))
        elif phase == 2:
            return self.max * (1.0 - np.exp(-9 * x))

    def bid_sub2(self, x,phase = 0):
        if phase == 0:
            return self.max * (1.0 - np.exp(-5 * x))
        elif phase == 1:
            return self.max * (1.0 - np.exp(-9 * x))
        elif phase == 2:
            return self.max * (1.0 - np.exp(-2 * x))

    def bid_sub3(self, x,phase = 0):
        if phase == 0:
            return self.max * (1.0 - np.exp(-10 * x))
        elif phase == 1:
            return self.max * (1.0 - np.exp(-4 * x))
        elif phase == 2:
            return self.max * (1.0 - np.exp(-6 * x))

    def round(self, pulled_arm1, pulled_arm2, pulled_arm3,phase = 0):
        reward1 = 0 if pulled_arm1 == 0 else np.maximum(0,np.random.normal(self.bid_sub1(self.bids[pulled_arm1],(self.day/self.phaselen)%self.n_phases), self.sigma))
        reward2 = 0 if pulled_arm2 == 0 else np.maximum(0,np.random.normal(self.bid_sub2(self.bids[pulled_arm2],(self.day/self.phaselen)%self.n_phases), self.sigma))
        reward3 = 0 if pulled_arm3 == 0 else np.maximum(0,np.random.normal(self.bid_sub3(self.bids[pulled_arm3],(self.day/self.phaselen)%self.n_phases), self.sigma))
        self.day = self.day + 1
        return np.array([reward1,reward2,reward3])