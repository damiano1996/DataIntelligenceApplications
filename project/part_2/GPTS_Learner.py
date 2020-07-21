import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

from project.dia_pckg.Learner import Learner


# we estimate the expected reward given by a bid value
# at each round the learner fit a GP with the chosen bids as inputs
# the targets of the GP are the observed number of clicks


class GPTS_Learner(Learner):

    def __init__(self, n_arms, arms):
        super(GPTS_Learner, self).__init__(n_arms=n_arms)

        self.arms = arms
        self.means = np.zeros(n_arms)
        self.sigmas = np.ones(n_arms) * 10
        self.pulled_arms = []

        alpha = 10.0
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))
        self.gp = GaussianProcessRegressor(kernel=kernel,
                                           alpha=alpha ** 2,
                                           normalize_y=True,
                                           n_restarts_optimizer=10)

    # update the values of the pulled arms and of the collected rewards
    def update_observations(self, arm_idx, reward):
        self.rewards_per_arm[arm_idx].append(reward)
        self.pulled_arms.append(self.arms[arm_idx])
        self.collected_rewards = np.append(self.collected_rewards, reward)

    # update the GP estimation and the parameters (mean and sigma) after each round
    def update_model(self):
        x = np.atleast_2d(self.pulled_arms).T
        y = self.collected_rewards

        if y.shape[0] == 1:
            return

        self.gp.fit(x, y)
        self.means, self.sigmas = self.gp.predict(np.atleast_2d(self.arms).T, return_std=True)
        self.sigmas = np.maximum(self.sigmas, 1e-2)

    # given the pulled arm and the reward, update the observations and the model
    def update(self, pulled_arm, reward):
        self.t += 1
        self.update_observations(pulled_arm, reward)
        self.update_model()

    # The learner choose which arm to pull at each round
    # it returns the index of the maximum value drawn from the normal distribution of the arms
    def pull_arm(self):
        sampled_values = np.random.normal(self.means, self.sigmas)
        return np.argmax(sampled_values)

    def pull_arm_v2(self):
        # sampled_values = np.random.normal(self.means, self.sigmas)
        return np.argmax(self.sigmas)

    def pull_arm_v3(self, availables):
        return np.argmax(self.sigmas[0:availables]) if (len(self.sigmas[0:availables]) > 0) else 0

    def pull_arm_v4 (self, availables):
        sampled_values = np.random.normal(self.means[0:availables], self.sigmas[0:availables])
        return np.argmax(sampled_values) if (len(sampled_values) > 0) else 0

    def get_confidence_sum (self):
        """
            Returns the mean of the accuracy over the entire GP, with a confidence bound of 95% (1.96).
            The first element is excluded since gives only noise
        """
        if (self.means[1:] > 0).all():
            return ((self.means[1:] - (1.96 * self.sigmas[1:])) / self.means[1:]).mean()
        else:
            return 0


    # For each sub-campaign we plot:
    # - the real function nr.clicks w.r.t. the bid value
    # - the observed click (one at each round)
    # - the prediction model
    def plot(self, env_sub):
        x_pred = np.atleast_2d(self.arms).T

        X = self.pulled_arms
        Y = self.collected_rewards

        plt.figure()

        plt.plot(x_pred, env_sub(x_pred), ':', label=r'$n(x)$')
        plt.scatter(X, Y, marker='o', label=r'Observed Clicks')

        plt.plot(x_pred, self.means, linestyle='-', label=f'Predicted Clicks {self.t}')
        plt.fill(np.concatenate([x_pred, x_pred[::-1]]),
                 np.concatenate([self.means - 1.96 * self.sigmas,
                                 (self.means + 1.96 * self.sigmas)[::-1]]),
                 alpha=.2, fc='C2', ec='None', label='95% conf interval')

        plt.xlabel('$x$')
        plt.ylabel('$n(x)$')
        plt.legend(loc='lower right')
        plt.show()
