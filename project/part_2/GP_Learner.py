import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

from project.dia_pckg.Learner import Learner
from project.dia_pckg.plot_style.cb91visuals import *


class GP_Learner(Learner):

    def __init__(self, arms):
        super().__init__(len(arms))

        alpha = 15.0
        self.arms = arms
        self.means = np.zeros(len(arms))
        self.sigmas = np.full(self.means.shape, alpha)
        self.pulled_arms = []

        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))
        self.gp = GaussianProcessRegressor(kernel=kernel,
                                           alpha=alpha ** 2,
                                           normalize_y=True,
                                           n_restarts_optimizer=9)

    def update_observations(self, arm_idx, reward):
        super().update_observations(arm_idx, reward)
        self.pulled_arms.append(self.arms[arm_idx])

    def update_model(self):
        x = np.atleast_2d(self.pulled_arms).T
        y = self.collected_rewards
        self.gp.fit(x, y)
        self.means, self.sigmas = self.gp.predict(np.atleast_2d(self.arms).T, return_std=True)
        self.sigmas = np.maximum(self.sigmas, 1e-2)

    def update(self, pulled_arm, reward):
        self.t += 1
        self.update_observations(pulled_arm, reward)
        self.update_model()

    def pull_arm(self, arm):
        sampled_value = np.random.normal(self.means[arm], self.sigmas[arm])
        return sampled_value

    def pull_arm_sequence(self):
        sampled_values = np.random.normal(self.means, self.sigmas)
        return sampled_values

    def plot(self, unknown_function, sigma_scale_factor=20):
        x_pred = np.atleast_2d(self.arms).T
        y_pred, sigma = self.gp.predict(x_pred, return_std=True)

        plt.figure(0)
        plt.title(f'Regret')
        plt.plot(x_pred, unknown_function, ':', label=r'Unknown function')
        plt.scatter(self.pulled_arms, self.collected_rewards, marker='o', label=r'Observed Clicks')
        plt.plot(x_pred, y_pred, '-', label=r'Predicted Clicks')
        plt.fill(np.concatenate([x_pred, x_pred[::-1]]),
                 np.concatenate([y_pred - 1.96 * sigma * sigma_scale_factor,
                                 (y_pred + 1.96 * sigma * sigma_scale_factor)[::-1]]),
                 alpha=.2, fc='C2', ec='None', label='95% conf interval')
        plt.xlabel('$x$')
        plt.ylabel('$n(x)$')
        plt.legend(loc='lower right')
        plt.show()
