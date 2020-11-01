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
                 n_arms_advertising,
                 bidding_environment,
                 keep_daily_price):
        """
        :param class_name:
        :param multi_class_handler:
        :param subcampaign_idx:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """

        self.class_name = class_name

        self.n_arms_advertising = n_arms_advertising

        self.pricing = Pricing(class_name=class_name, multi_class_handler=multi_class_handler, n_arms=n_arms_pricing,
                               keep_daily_price=keep_daily_price)
        self.advertising = Advertising(bidding_environment=bidding_environment,
                                       n_arms=self.n_arms_advertising,
                                       subcampaign_idx=subcampaign_idx)

        self.window_size = 5
        self.window_revenue = np.array([])
        self.window_clicks = np.array([])
        self.campaign_value = 0

        self.total_revenue = 0
        self.total_clicks = 0

        self.daily_revenue = 0
        self.daily_clicks = 0

        self.price = 0

    def daily_update(self, pulled_arm, pull_fix_arm=None):
        """
            Daily update
        :param pulled_arm: Learned best budget allocation
        :return:
        """
        # extracting the daily reward from the TS
        self.daily_clicks = self.advertising.get_daily_clicks(pulled_arm)
        self.daily_revenue, daily_purchases = self.pricing.get_daily_revenue(self.daily_clicks,
                                                                             pull_fix_arm=pull_fix_arm)

        self.price = self.daily_revenue / self.daily_clicks if self.daily_clicks != 0 else self.price

        daily_regret = self.get_daily_regret(self.daily_clicks, self.advertising.optimal_clicks,
                                             self.daily_revenue, self.pricing.optimal_revenue)

        print('class: ', self.class_name,
              'optimal clicks: ', self.advertising.optimal_clicks,
              'collected clicks: ', round(self.daily_clicks),
              'optimal revenue: ', round(self.pricing.optimal_revenue * self.advertising.optimal_clicks),
              'collected revenue: ', int(self.daily_revenue))

        self.total_revenue += self.daily_revenue
        self.total_clicks += self.daily_clicks
        self.update_windows(self.daily_revenue, self.daily_clicks)

        return daily_regret, self.daily_revenue

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
        return self.advertising.learner.pull_arm_sequence()

    def update_windows(self, daily_revenue, daily_clicks):
        # if (self.keep_daily_price):

        # else:
        self.window_revenue = np.append(self.window_revenue, daily_revenue)
        if self.window_revenue.shape[0] > self.window_size:
            self.window_revenue = np.delete(self.window_revenue, 0)

        self.window_clicks = np.append(self.window_clicks, daily_clicks)
        if self.window_clicks.shape[0] > self.window_size:
            self.window_clicks = np.delete(self.window_clicks, 0)

        self.campaign_value = np.sum(self.window_revenue) / np.sum(self.window_clicks) if np.sum(
            self.window_clicks) > 0 else 0
