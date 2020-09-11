import numpy as np
from project.part_2.GPTS_LearnerV2 import GPTS_LearnerV2

from project.dia_pckg.Config import *


# Extension of the standard GP_Learner for implementing a sliding-window combinatorial
# bandit algorithm due to the presence of multiple abrupt phases
class DynamicLearner(GPTS_LearnerV2):
    def __init__(self,n_arms, arms):
        super().__init__(n_arms, arms)

    def update_observations(self, pulled_arm, reward):
        if len(self.collected_rewards) == len_window:
            # try:
            #     index_to_pop = np.where(self.pulled_arms == self.arms[arm_idx])[0][0]
            #     self.rewards_per_arm[arm_idx].pop(0)
            #     self.pulled_arms.pop(index_to_pop)
            #     self.collected_rewards = np.delete(self.collected_rewards, index_to_pop)
            #
            #
            # except:
            index_arm = np.where(self.arms == self.pulled_arms[0])[0][0]
            self.rewards_per_arm[index_arm].pop(0)
            self.pulled_arms.pop(0)
            self.collected_rewards = np.delete(self.collected_rewards, 0)

        # if len(self.collected_rewards) == self.len_window:
        #    index_arm = np.where(self.arms == self.pulled_arms[0])[0][0]
        #    self.rewards_per_arm[index_arm].pop(0)
        #    self.pulled_arms.pop(0)
        #    self.collected_rewards = np.delete(self.collected_rewards, 0)
        self.rewards_per_arm[pulled_arm].append(reward)
        self.pulled_arms.append(self.arms[pulled_arm])
        self.collected_rewards = np.append(self.collected_rewards, reward)
