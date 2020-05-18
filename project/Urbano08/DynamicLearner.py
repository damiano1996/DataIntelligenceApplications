import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C



class DynamicLearner():

    def __init__(self, n_arms, arms, len_window):
        self.n_arms = n_arms
        self.len_window = len_window
        self.t = 0
        self.rewards_per_arm = [[] for _ in range(n_arms)]
        self.collected_rewards = np.array([])

        self.arms = arms
        self.means = np.zeros(n_arms)
        self.sigmas = np.ones(n_arms) * 10
        self.pulled_arms = []

        alpha = 10.0
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))
        self.gp = GaussianProcessRegressor(kernel=kernel,
                                           alpha=alpha ** 2,
                                           normalize_y=True,
                                           n_restarts_optimizer=9)

        self.X = []
        self.Y = []

    def update_observations(self, arm_idx, reward):
        if(len(self.collected_rewards) == self.len_window):
            index_arm = np.where(self.arms == self.pulled_arms[0])[0][0]
            self.rewards_per_arm[index_arm].pop(0)
            self.pulled_arms.pop(0)
            self.collected_rewards = np.delete(self.collected_rewards, 0)
        self.rewards_per_arm[arm_idx].append(reward)
        self.pulled_arms.append(self.arms[arm_idx])
        self.collected_rewards = np.append(self.collected_rewards, reward)

    def update_model(self):
        x = np.atleast_2d(self.pulled_arms).T
        y = self.collected_rewards

        self.X = x
        self.Y = y.ravel()

        self.gp.fit(x, y)
        self.means, self.sigmas = self.gp.predict(np.atleast_2d(self.arms).T, return_std=True)
        self.sigmas = np.maximum(self.sigmas, 1e-2)

    def update(self, pulled_arm, reward):
        self.t += 1
        self.update_observations(pulled_arm, reward)
        self.update_model()

    def pull_arm(self):
        return np.argmax(self.sigmas)