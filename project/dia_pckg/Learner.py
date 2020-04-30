import numpy as np


class Learner():
    """
        This is the same Learner of the prof
    """

    def __init__(self, n_arms):
        """
        :param n_arms:
        """
        self.n_arms = n_arms

        self.t = 0
        self.rewards_per_arm = x = [[] for _ in range(n_arms)]
        self.collected_rewards = np.array([])

    def update_observations(self, pulled_arm, reward):
        """
        :param pulled_arm:
        :param reward:
        :return:
        """
        self.rewards_per_arm[pulled_arm].append(reward)
        self.collected_rewards = np.append(self.collected_rewards, reward)
