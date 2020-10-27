import numpy as np

from project.dia_pckg.Config import *
from project.part_2.GPTS_Learner import GPTS_Learner


# Extension of the standard GP_Learner for implementing a sliding-window combinatorial
# bandit algorithm due to the presence of multiple abrupt phases
class DynamicLearner(GPTS_Learner):
    def __init__(self, arms):
        super().__init__(arms)

    def update_observations(self, pulled_arm, reward):
        if len(self.collected_rewards) >= len_window:
            index_arm = np.where(self.arms == self.pulled_arms[0])[0][0]
            self.rewards_per_arm[index_arm].pop(0)
            self.pulled_arms.pop(0)
            self.collected_rewards = np.delete(self.collected_rewards, 0)

        self.rewards_per_arm[pulled_arm].append(reward)
        self.pulled_arms.append(self.arms[pulled_arm])
        self.collected_rewards = np.append(self.collected_rewards, reward)


