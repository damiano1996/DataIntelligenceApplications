import numpy as np

from project.part_6.Advertising import Advertising
from project.part_2.GPTS_Learner import GPTS_Learner
from project.dia_pckg.Config import *


## bisogna far restituire click per subcampaign e aggiornare relative curve
## le curve dell'advertising sono aggiornate da advertising tramite get_daily_clicks, solo quelle del pricing vanno guardate

class SubCampaignHandler:
    """
        This class implements the "Subcampaign j" block of the other_files/schema.jpg
    """

    def __init__(self,
                 class_name,
                 subcampaign_idx,
                 n_arms_pricing,
                 n_arms_advertising,
                 bidding_environment):
        """
        :param class_name:
        :param multi_class_handler:
        :param subcampaign_idx:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """

        self.class_name = class_name

        self.n_arms_advertising = n_arms_advertising
        self.n_arms_pricing = n_arms_pricing

        self.advertising = Advertising(bidding_environment=bidding_environment,
                                       n_arms=self.n_arms_advertising,
                                       subcampaign_idx=subcampaign_idx)

        self.learner = GPTS_Learner(n_arms=self.n_arms_pricing, arms=self.get_candidate_prices())

        self.total_revenue = 0
        self.total_clicks = 0

        self.daily_revenue = 0
        self.daily_clicks = 0

        self.price = 0

    def pull_arms_advertising(self, pull_arm):
        """
            pull the advertiser selected arm
        :param pull_arm: Learned best budget allocation
        :return:
        """
        # extracting the daily reward from the TS
        self.daily_clicks = self.advertising.get_daily_clicks(pull_arm)

        return self.daily_clicks

    def get_updated_parameters(self):
        return self.advertising.learner.pull_arm_sequence()

    def get_price_convr(self, price_arm):
        return self.learner.means[price_arm]

    def update_conversion_rate(self, arm, value_conv_rate):
        self.learner.update(arm, value_conv_rate)

    def get_candidate_prices(self):
        """
            This method return the candidate prices, one price for each arm.
            The "indices" array contains the positions of the specified prices in the aggregate curve
        :return:
        """
        arm_distance = int(product_config["max_price"] / self.n_arms_pricing)
        prices = [int(arm_distance * arm) for arm in range(1, self.n_arms_pricing + 1)]

        return prices
