import numpy as np

from project.part_6.Advertising import Advertising


class SubCampaignHandler:
    """
        This class implements the "Subcampaign j" block of the other_files/schema.jpg
    """

    def __init__(self,
                 class_name,
                 subcampaign_idx,
                 n_arms_advertising,
                 bidding_environment,
                 arm):
        """
        :param class_name:
        :param multi_class_handler:
        :param subcampaign_idx:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """

        self.class_name = class_name

        self.n_arms_advertising = n_arms_advertising

        self.arm = arm

        self.advertising = Advertising(bidding_environment=bidding_environment,
                                       n_arms=self.n_arms_advertising,
                                       subcampaign_idx=subcampaign_idx)

        self.window_size = 5
        self.window_revenue = np.array([])
        self.window_clicks = np.array([])

        self.total_revenue = 0
        self.total_clicks = 0

        self.daily_revenue = 0
        self.daily_clicks = 0

        self.price = 0

    def daily_update(self, pulled_arm):
        """
            Daily update
        :param pulled_arm: Learned best budget allocation
        :return:
        """
        # extracting the daily reward from the TS
        self.daily_clicks = self.advertising.get_daily_clicks(pulled_arm)

        #daily_regret = self.get_daily_regret(self.daily_clicks, self.advertising.optimal_clicks,
        #                                     self.daily_revenue, self.pricing.optimal_revenue)

        #print('class: ', self.class_name,
        #      'optimal clicks: ', self.advertising.optimal_clicks,
        #      'collected clicks: ', round(self.daily_clicks),
        #      'optimal revenue: ', round(self.pricing.optimal_revenue * self.advertising.optimal_clicks),
        #      'collected revenue: ', int(self.daily_revenue))

        # self.total_revenue += self.daily_revenue
        # self.total_clicks += self.daily_clicks
        #self.update_windows(self.daily_revenue, self.daily_clicks)

        return self.daily_clicks

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
        self.window_revenue = np.append(self.window_revenue, daily_revenue)
        if (self.window_revenue.shape[0] > self.window_size):
            self.window_revenue = np.delete(self.window_revenue, 0)

        self.window_clicks = np.append(self.window_clicks, daily_clicks)
        if (self.window_clicks.shape[0] > self.window_size):
            self.window_clicks = np.delete(self.window_clicks, 0)

        self.total_revenue = np.sum(self.window_revenue)
        self.total_clicks = np.sum(self.window_clicks)
