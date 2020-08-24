import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from project.dia_pckg.Learner import Learner
from project.dia_pckg.Config import *


class GP_Learner(Learner):

    def __init__(self, n_arms, arms):
        """
        We estimate the expected reward given by a bid value.
        At each round the learner fit a GP with the chosen bids as inputs
        The targets of the GP are the observed number of clicks
        @param n_arms:
        @param arms:
        """
        self.n_arms = n_arms

        self.t = 0
        self.rewards_per_arm = x = [[] for _ in range(n_arms)]
        self.collected_rewards = np.array([])

        self.arms = arms
        self.means = np.zeros(n_arms)
        self.sigmas = np.ones(n_arms) * 10
        self.pulled_arms = []

    def update_observations(self, arm_idx, reward):
        """
        Update the values of the pulled arms and of the collected rewards
        @param arm_idx: index of the arm
        @param reward: associated reward
        """
        self.rewards_per_arm[arm_idx].append(reward)
        self.pulled_arms.append(self.arms[arm_idx])
        self.collected_rewards = np.append(self.collected_rewards, reward)

    def update_model(self):
        """
        Update the GP estimation and the parameters (mean and sigma) after each round
        """
        alpha = 10.0
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))
        gp = GaussianProcessRegressor(kernel=kernel,
                                      alpha=alpha ** 2,
                                      normalize_y=True,
                                      n_restarts_optimizer=9)
        # self.gp = GaussianProcessRegressor(normalize_y=True,
        #                                  n_restarts_optimizer=9)

        x = np.atleast_2d(self.pulled_arms).T
        y = self.collected_rewards

        try:
            gp.fit(x, y)
            self.means, self.sigmas = gp.predict(np.atleast_2d(self.arms).T, return_std=True)
            self.sigmas = np.maximum(self.sigmas, 1e-2)
        except:
            self.means = [0]
            self.sigmas = [0]

    def update(self, pulled_arm, reward):
        """
        Given the pulled arm and the reward, update the observations and the model
        @param pulled_arm: index of the pulled arm
        @param reward: reward associated to the pulled arm
        """
        self.t += 1
        self.update_observations(pulled_arm, 100 * reward / max_n_clicks)
        self.update_model()

    def plot(self, env_sub):
        """
        For each sub-campaign we plot:
            - the real function nr.clicks w.r.t. the bid value
            - the observed click (one at each round)
            - the prediction model
        @param env_sub: considered sub-campaign
        """
        x_pred = np.atleast_2d(self.arms).T

        X = self.pulled_arms
        Y = self.collected_rewards * max_n_clicks / 100

        plt.figure()

        plt.plot(x_pred, env_sub(x_pred), ':', label=r'$n(x)$')
        plt.scatter(X, Y, marker='o', label=r'Observed Clicks')

        plt.plot(x_pred, self.means * max_n_clicks / 100, linestyle='-', label=f'Predicted Clicks {self.t}')
        plt.fill(np.concatenate([x_pred, x_pred[::-1]]),
                 np.concatenate([self.means - 1.96 * self.sigmas,
                                 (self.means + 1.96 * self.sigmas)[::-1]]) * max_n_clicks / 100,
                 alpha=.2, fc='C2', ec='None', label='95% conf interval')

        plt.xlabel('$x$')
        plt.ylabel('$n(x)$')
        plt.legend(loc='lower right')
        plt.show()
