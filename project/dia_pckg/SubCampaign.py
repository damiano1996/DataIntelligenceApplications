import numpy as np

from project.dia_pckg.Config import *


class SubCampaign:

    def __init__(self, class_obj=None, product=None, campaign=None):
        """
        :param class_obj: Class object
        :param product: Product object
        :param campaign: Campaign object
        """
        self.my_class = class_obj
        self.product = product
        self.campaign = campaign

        self.param_for_phase = np.random.random_integers(10, 200, 3) / 10
        self.max_click_phase = np.minimum(np.random.random_integers(30, 200, 3) / 100, [1, 1, 1])

    def bid(self, x, phase=-1):
        phase = 0 if phase == -1 else int(phase)
        percentage_value = (self.max_click_phase[phase] - np.exp(-self.param_for_phase[phase] * x))

        return np.ceil(max_n_clicks * percentage_value)
