import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import figaspect


class SubCampaign:

    def __init__(self, class_obj, product, campaign):
        """
        :param class_obj: Class object
        :param product: Product object
        :param campaign: Campaign object
        """
        self.my_class = class_obj
        self.product = product
        self.campaign = campaign

        # similarly to Class, but in this case we don't need the three curves for the abrupt phases
        # Modify if necessary
        self.cob_curve = self.get_clicks_over_budget(self.campaign.max_budget,
                                                     self.campaign.max_n_clicks,
                                                     random_params=True)

    def get_clicks_over_budget(self, max_budget, max_n_clicks, m=1, q=0, random_params=False):
        """
            This function generates a clicks over budget curve
        :param max_budget: max budget allocated
        :param max_n_clicks: max number of clicks
        :param m: m-coefficient of the line
        :param q: q-coefficient of the line
        :param random_params: boolean to randomize m and q
        :return:
        """
        if random_params:
            m = np.random.uniform(0.9, 1.1)
            q = -np.random.randint(int(max_budget / 2 * 0.25), int(max_budget / 2 * 0.75))

        budget = np.linspace(0, max_budget)
        clicks = m * budget + q

        first_positive = np.where(clicks >= 0)[0]
        if first_positive.shape[0] > 0:
            clicks[:first_positive[0]] = 0
        first_n_clicks = np.where(clicks >= max_n_clicks)[0]
        if first_n_clicks.shape[0] > 0:
            clicks[first_n_clicks[0]:] = max_n_clicks

        return (np.asarray(budget), np.asarray(clicks))

    def plot_cob_curve(self):
        """
            To plot the curve
        :return:
        """
        w, h = figaspect(0.7)

        fig, ax = plt.subplots(1, 1, figsize=(w, h))
        fig.suptitle(f'Clicks over Budget Curve - Class name: {self.my_class.name}', y=1.)

        # ax.set_ylim(0, 1)
        ax.plot(self.cob_curve[0],
                self.cob_curve[1])
        ax.set_xlabel('Budget')
        ax.set_ylabel('Number of Clicks')

        fig.show()
