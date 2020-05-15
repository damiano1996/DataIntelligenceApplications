import numpy as np

from project.part_4.TS_Learner import TS_Learner


class SWTS_Learner(TS_Learner):

    def __init__(self, n_arms, arm_prices, window_size):
        super().__init__(n_arms, arm_prices)

        self.window_size = window_size

    def update(self, pulled_arm, bernoulli_reward):
        """
        :param pulled_arm:
        :param reward:
        :return:
        """
        self.t += 1

        real_reward = bernoulli_reward * self.arm_prices[pulled_arm]  # calculate the real reward (isBought*price)
        self.update_observations(pulled_arm, bernoulli_reward, real_reward)

        cum_rew = np.sum(self.rewards_per_arm[pulled_arm][-self.window_size:])
        n_rounds_arm = len(self.rewards_per_arm[pulled_arm][-self.window_size:])

        self.beta_parameters[pulled_arm, 0] = cum_rew + 1.0
        self.beta_parameters[pulled_arm, 1] = n_rounds_arm - cum_rew + 1.0

    def update_observations(self, pulled_arm, bernoulli_reward, real_reward):
        """
        :param pulled_arm:
        :param reward:
        :return:
        """
        self.rewards_per_arm[pulled_arm].append(bernoulli_reward)
        self.collected_rewards = np.append(self.collected_rewards, real_reward)
