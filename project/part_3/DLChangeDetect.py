import warnings

import numpy as np

from project.part_2.GPTS_Learner import GPTS_Learner as GP_Learner


class DLChangeDetect(GP_Learner):
    def __init__(self, arms, min_len=3, z_score=2.58):
        """
        @param arms: possible bids
        @param min_len: minimum number of sample on the arm to check for changes
        @param z_score: minimum result of the test to detect a change
        """
        super().__init__(arms)
        self.min_len = min_len
        self.z_score = z_score
        self.day = 0

    def update_observations(self, pulled_arm, reward):
        """
        @param pulled_arm: arm corresponding to the bid of the past day
        @param reward: number of clicks collected on the past day
        """
        warnings.simplefilter(action='ignore', category=FutureWarning)

        if len(self.rewards_per_arm[pulled_arm]) > self.min_len:

            mean_diff = reward - np.array(self.rewards_per_arm[pulled_arm]).mean()
            std = np.array(self.rewards_per_arm[pulled_arm]).std()

            test = np.abs(mean_diff / std) if std != 0 else 0

            if test > self.z_score:
                print("Change detected (DAY: " + str(self.day) + "): len=" +
                      str(len(self.rewards_per_arm[pulled_arm])) +
                      " std=" + str(std) +
                      " test=" + str(test))
                self.rewards_per_arm[pulled_arm].clear()
                self.collected_rewards = np.delete(self.collected_rewards, self.pulled_arms == self.arms[pulled_arm])
                self.pulled_arms = np.delete(self.pulled_arms, self.pulled_arms == self.arms[pulled_arm])

        self.rewards_per_arm[pulled_arm].append(reward)
        self.collected_rewards = np.append(self.collected_rewards, reward)

        self.pulled_arms = np.append(self.pulled_arms, self.arms[pulled_arm])

        self.day = self.day + 1
