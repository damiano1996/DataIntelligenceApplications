from project.dia_pckg.Learner import *


class TS_Learner(Learner):
    """
        This is the same code of the prof
    """

    def __init__(self, n_arms):
        """
        :param n_arms:
        """
        super().__init__(n_arms)

        self.beta_parameters = np.ones((n_arms, 2))

    def pull_arm(self):
        """
        :return: index of the most interesting arm from the demand point of view
        """
        idx = np.argmax(
            np.random.beta(self.beta_parameters[:, 0],
                           self.beta_parameters[:, 1])
        )
        return idx

    def pull_arm_v2(self, arm_prices):
        """
        :return: index of the most interesting arm from the revenue point of view
        """
        probabilities = np.random.beta(self.beta_parameters[:, 0],
                           self.beta_parameters[:, 1])
        values = probabilities * arm_prices
        idx = np.argmax(probabilities * arm_prices)
        return idx

    def update(self, pulled_arm, reward):
        """
        :param pulled_arm:
        :param reward:
        :return:
        """
        self.t += 1
        self.update_observations(pulled_arm, reward)
        self.beta_parameters[pulled_arm, 0] = self.beta_parameters[pulled_arm, 0] + reward
        self.beta_parameters[pulled_arm, 1] = self.beta_parameters[pulled_arm, 1] + 1.0 - reward
