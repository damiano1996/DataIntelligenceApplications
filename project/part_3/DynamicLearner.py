import numpy as np

from project.part_2.GPTS_Learner import GPTS_Learner as GP_Learner


# Extension of the standard GP_Learner for implementing a sliding-window combinatorial
# bandit algorithm due to the presence of multiple abrupt phases
class DynamicLearner(GP_Learner):
    def __init__(self, arms, win_length=30):
        super().__init__(arms)
        self.win_length = win_length

    def update_observations(self, pulled_arm, reward):
        if len(self.collected_rewards) >= self.win_length:
            index_arm = np.where(self.arms == self.pulled_arms[0])[0][0]
            self.rewards_per_arm[index_arm].pop(0)
            self.pulled_arms.pop(0)
            self.collected_rewards = np.delete(self.collected_rewards, 0)

        self.rewards_per_arm[pulled_arm].append(reward)
        self.pulled_arms.append(self.arms[pulled_arm])
        self.collected_rewards = np.append(self.collected_rewards, reward)
