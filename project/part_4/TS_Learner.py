from project.dia_pckg.Learner import *


class TS_Learner(Learner):
    """
        This is the same code of the prof
    """

    def __init__(self, n_arms, arm_prices):
        """
        :param n_arms:
        """
        super().__init__(n_arms)

        self.beta_parameters = np.ones((n_arms, 2))
        self.arm_prices = arm_prices

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

    def update(self, pulled_arm, reward):
        """
        :param pulled_arm:
        :param reward:
        :return:
        """
        self.t += 1
        real_reward = reward * self.arm_prices[pulled_arm]  # calculate the real reward (isBought*price)

        self.update_observations(pulled_arm, real_reward)
        self.beta_parameters[pulled_arm, 0] = self.beta_parameters[pulled_arm, 0] + reward
        self.beta_parameters[pulled_arm, 1] = self.beta_parameters[pulled_arm, 1] + 1.0 - reward
