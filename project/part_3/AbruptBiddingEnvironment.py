import numpy as np


class AbruptBiddingEnvironment():

    def __init__(self, bids, max, sigma, phaselen=60, n_phases=3):
        self.bids = bids
        self.sigma = sigma
        self.max = max
        self.subs = [self.bid_sub1, self.bid_sub2, self.bid_sub3]
        self.day = 0
        self.phaselen = phaselen
        self.n_phases = n_phases
        self.phase = 0

    def phase(self):
        return (self.day / self.phaselen) % self.n_phases

    def bid_sub1(self, x, phase=-1):
        phase = self.phase if phase == -1 else phase
        if int(phase) == 0:
            return np.ceil(self.max * (1.0 - np.exp(-4 * x)))
        elif int(phase) == 1:
            return np.ceil(self.max * (1.0 - np.exp(-20 * x)))
        elif int(phase) == 2:
            return np.ceil(self.max * (1.0 - np.exp(-9 * x)))

    def bid_sub2(self, x, phase=-1):
        phase = self.phase if phase == -1 else phase

        if int(phase) == 0:
            return x - x  # self.max * (1.0 - np.exp(-5 * x))
        elif int(phase) == 1:
            return np.ceil(self.max * (1.0 - np.exp(-1 * x)))
        elif int(phase) == 2:
            return np.ceil(self.max * (1.0 - np.exp(-2 * x)))

    def bid_sub3(self, x, phase=-1):
        phase = self.phase if phase == -1 else phase

        if int(phase) == 0:
            return np.ceil(self.max * (1.0 - np.exp(-10 * x)))
        elif int(phase) == 1:
            return np.ceil(self.max * (1.0 - np.exp(-1 * x)))
        elif int(phase) == 2:
            return x - x  # self.max * (1.0 - np.exp(-6 * x))

    def round(self, pulled_arm1, pulled_arm2, pulled_arm3):
        self.phase = (self.day / self.phaselen) % self.n_phases
        pulled_arms = [pulled_arm1, pulled_arm2, pulled_arm3]
        rewards = np.array([])
        for i in range(0, len(pulled_arms)):
            reward = 0 if pulled_arms[i] == 0 else np.maximum(0, np.ceil(np.random.normal(
                self.subs[i](self.bids[pulled_arms[i]], self.phase), self.sigma)))
            rewards = np.append(rewards, reward)
        self.day = self.day + 1
        return rewards
