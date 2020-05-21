import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

from project.Urbano08.Learner import Learner


class DynamicLearner(Learner):
    def __init__(self, n_arms, arms, len_window):
        super().__init__(n_arms, arms)
        self.len_window = len_window

    def update_observations(self, arm_idx, reward):
        if len(self.collected_rewards) == self.len_window:
            index_arm = np.where(self.arms == self.pulled_arms[0])[0][0]
            self.rewards_per_arm[index_arm].pop(0)
            self.pulled_arms.pop(0)
            self.collected_rewards = np.delete(self.collected_rewards, 0)
        self.rewards_per_arm[arm_idx].append(reward)
        self.pulled_arms.append(self.arms[arm_idx])
        self.collected_rewards = np.append(self.collected_rewards, reward)

