import numpy as np


class SubCampaign:

    def __init__(self,
                 bids, sigma, max_n_clicks,
                 class_obj=None, product=None, campaign=None):
        """
        :param class_obj: Class object
        :param product: Product object
        :param campaign: Campaign object
        """
        self.bids = bids
        self.sigma = sigma
        self.max_n_clicks = max_n_clicks

        self.my_class = class_obj
        self.product = product
        self.campaign = campaign

        self.param_for_phase = np.random.choice(np.arange(2, 7, 0.01), 3)
        self.max_value_phase = np.random.choice(np.arange(0.3, 1, 0.01), 3)

        self.means = {f'phase_{i}': self.phase_curve(bids, phase=i) for i in range(3)}
        self.sigmas = {f'phase_{i}': np.multiply(self.means[f'phase_{i}'], sigma) for i in range(3)}

    def phase_curve(self, x, phase=0):
        curve = self.max_n_clicks * (self.max_value_phase[phase] - np.exp(-self.param_for_phase[phase] * x))
        curve[np.where(curve < 0)] = 0
        return curve


if __name__ == '__main__':
    x = np.arange(0, 1, 0.01)
    sc = SubCampaign(x, 5, 1000)

    import matplotlib.pyplot as plt

    for phase in range(3):
        plt.plot(x, sc.means[f'phase_{phase}'])
        plt.show()
