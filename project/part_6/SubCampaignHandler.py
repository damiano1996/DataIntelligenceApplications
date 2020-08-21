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
                 subcampaign_name,
                 n_arms_pricing,
                 n_arms_advertising):
        """
        :param class_name:
        :param multi_class_handler:
        :param subcampaign_name:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """

        self.class_name = class_name

        self.pricing = Pricing(class_name=class_name, multi_class_handler=multi_class_handler, n_arms=n_arms_pricing)
        self.advertising = Advertising(n_arms=n_arms_advertising, subcampaign_name=subcampaign_name)

        self.daily_regret = 0
        self.daily_total_revenue = 0

        self.total_revenue = 0
        self.total_clicks = 0

    def daily_update(self, pulled_arm):
        """
            Daily update
        :param pulled_arm: Learned best budget allocation
        :return:
        """
        # extracting the daily reward from the TS
        daily_clicks, optimal_daily_clicks = self.advertising.get_daily_clicks(pulled_arm)
        daily_collected_revenues, optimal_daily_revenue = self.pricing.get_daily_collected_revenues(daily_clicks)

        self.daily_total_revenue = int(np.sum(daily_collected_revenues))

        self.daily_regret = self.get_daily_regret(daily_clicks, optimal_daily_clicks,
                                                  self.daily_total_revenue, optimal_daily_revenue)

        print('class: ', self.class_name,
              'optimal clicks: ', int(optimal_daily_clicks), 'collected clicks: ', int(daily_clicks),
              'optimal revenue: ', int(optimal_daily_revenue * optimal_daily_clicks), 'collected revenue: ',
              int(self.daily_total_revenue))

        self.total_revenue += self.daily_total_revenue
        self.total_clicks += daily_clicks

        return self.daily_regret, self.daily_total_revenue

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
