from project.dia_pckg.Learner import *


class TS_Learner(Learner):

    def __init__(self, n_arms, arm_prices):
        """
        :param n_arms:
        """
        super().__init__(n_arms)

        self.beta_parameters = np.ones((n_arms, 2))
        self.arm_prices = arm_prices

    def initialize_learner(self, beta_parameters, rewards_per_arm):
        """
        Set the prior passed as input
        :param beta_parameters: beta parameters with whom will be initialized
        :param rewards_per_arm: beta rewards_per_arm with whom will be initialized
        """
        if beta_parameters is not None:
            self.beta_parameters = beta_parameters
        if rewards_per_arm is not None:
            self.rewards_per_arm = rewards_per_arm

    def pull_arm_demand(self):
        """
        :return: index of the most interesting arm from the demand point of view
        """
        idx = np.argmax(
            np.random.beta(self.beta_parameters[:, 0],
                           self.beta_parameters[:, 1])
        )
        return idx

    def pull_arm_revenue(self):
        """
        :return: index of the most interesting arm from the revenue point of view
        """
        probabilities = np.random.beta(self.beta_parameters[:, 0],
                                       self.beta_parameters[:, 1])
        idx = np.argmax(probabilities * self.arm_prices)
        return idx

    def update(self, pulled_arm, bernoulli_reward):
        """
        :param pulled_arm:
        :param bernoulli_reward:
        :return:
        """
        self.t += 1
        real_reward = bernoulli_reward * self.arm_prices[pulled_arm]  # calculate the real reward (isBought*price)

        self.update_observations(pulled_arm, real_reward)
        self.beta_parameters[pulled_arm, 0] = self.beta_parameters[pulled_arm, 0] + bernoulli_reward
        self.beta_parameters[pulled_arm, 1] = self.beta_parameters[pulled_arm, 1] + 1.0 - bernoulli_reward

    def get_real_reward(self, pulled_arm, bernoulli_reward):
        """
        :param pulled_arm:
        :param bernoulli_reward:
        :return: the real reward price*bernoulli_reard
        """
        real_reward = bernoulli_reward * self.arm_prices[pulled_arm]  # calculate the real reward (isBought*price)
        return real_reward
