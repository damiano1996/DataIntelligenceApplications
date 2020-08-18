import numpy as np
from project.part_2.GPTS_Learner import GPTS_Learner
from project.dia_pckg.Config import *


class DynamicLearner(GPTS_Learner):
    def __init__(self, n_arms, arms, len_window = len_window):
        super().__init__(n_arms, arms)
        self.len_window = len_window

    def update_observations(self, arm_idx, reward):
        if len(self.collected_rewards) == self.len_window:
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
        self.rewards_per_arm[arm_idx].append(reward)
        self.pulled_arms.append(self.arms[arm_idx])
        self.collected_rewards = np.append(self.collected_rewards, reward)
