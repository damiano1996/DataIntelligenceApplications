import numpy as np

from project.part_6.Advertising import Advertising
from project.part_6.Pricing import Pricing


class SubCampaignHandler:
    """
        This class implements the "Subcampaign j" block of the other_files/schema.jpg
    """

    def __init__(self,
                 class_name,
                 multi_class_handler,
                 subcampaign_idx,
                 n_arms_pricing,
                 n_arms_advertising):
        """
        :param class_name:
        :param multi_class_handler:
        :param subcampaign_idx:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """

        self.class_name = class_name

        self.pricing = Pricing(class_name=class_name, multi_class_handler=multi_class_handler, n_arms=n_arms_pricing)
        self.advertising = Advertising(n_arms=n_arms_advertising, subcampaign_idx=subcampaign_idx)

        self.total_revenue = 0
        self.total_clicks = 0

    def daily_update(self, pulled_arm, opt=False):
        """
            Daily update
        :param pulled_arm: Learned best budget allocation
        :return:
        """
        # extracting the daily reward from the TS
        daily_clicks = self.advertising.get_daily_clicks(pulled_arm)
        daily_collected_revenues = self.pricing.get_daily_revenues(daily_clicks)

        daily_revenue = np.sum(daily_collected_revenues)

        daily_regret = self.get_daily_regret(daily_clicks, self.advertising.optimal_clicks,
                                             daily_revenue, self.pricing.optimal_revenue)

        print('class: ', self.class_name,
              'optimal clicks: ', self.advertising.optimal_clicks,
              'collected clicks: ', round(daily_clicks),
              'optimal revenue: ', round(self.pricing.optimal_revenue * self.advertising.optimal_clicks),
              'collected revenue: ', int(daily_revenue))

        # To update the total revenue in case of optimality, we have to multiply the optimal_daily_revenue
        # by the number of daily_clicks since the number of daily_clicks can be greater than optimal_daily_clicks.
        self.total_revenue += daily_revenue if not opt else self.pricing.optimal_revenue * daily_clicks
        # For the same reason above, we don't need the optimal_daily_clicks in case of optimality
        self.total_clicks += daily_clicks  # if not opt else optimal_daily_clicks

        return daily_regret, daily_revenue

    def get_daily_regret(self, daily_clicks, optimal_daily_clicks, daily_revenue, optimal_daily_revenue):
        """
        :param daily_clicks:
        :param optimal_daily_clicks:
        :param daily_revenue:
        :param optimal_daily_revenue:
        :return:
        """
        best = optimal_daily_clicks * optimal_daily_revenue
        learned = daily_revenue  # this is the total profit
        return best - learned

    def get_updated_parameters(self):
        return self.advertising.learner
