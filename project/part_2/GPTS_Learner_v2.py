import matplotlib.pyplot as plt
import numpy as np

from exercises.part3.GPTS_Learner import GPTS_Learner
from project.dia_pckg.Config import max_n_clicks


class GPTS_Learner_v2(GPTS_Learner):

    def __init__(self, n_arms, arms):
        super().__init__(n_arms, arms)

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
        Y = self.collected_rewards * max_n_clicks / 10

        plt.figure()

        plt.plot(x_pred, env_sub(x_pred), ':', label=r'$n(x)$')
        plt.scatter(X, Y, marker='o', label=r'Observed Clicks')

        plt.plot(x_pred, self.means * max_n_clicks / 10, linestyle='-', label=f'Predicted Clicks {self.t}')
        plt.fill(np.concatenate([x_pred, x_pred[::-1]]),
                 np.concatenate([self.means - 1.96 * self.sigmas,
                                 (self.means + 1.96 * self.sigmas)[::-1]]) * max_n_clicks / 10,
                 alpha=.2, fc='C2', ec='None', label='95% conf interval')

        plt.xlabel('$x$')
        plt.ylabel('$n(x)$')
        plt.legend(loc='lower right')
        plt.show()
