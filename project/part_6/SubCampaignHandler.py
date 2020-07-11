import numpy as np

from project.part_6.Pricing import Pricing


class SubCampaignHandler(Pricing):
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
        super(SubCampaignHandler, self).__init__(class_name=class_name,
                                                 multi_class_handler=multi_class_handler,
                                                 subcampaign_name=subcampaign_name,
                                                 n_arms_pricing=n_arms_pricing,
                                                 n_arms_advertising=n_arms_advertising)

        self.daily_regret = 0
        self.daily_revenue = 0

    def daily_update(self, budget_allocation):
        """
            Daily update
        :param budget_allocation: Learned best budget allocation
        :return:
        """
        # extracting the daily reward from the TS
        daily_collected_revenues, optimal_daily_revenue = self.get_daily_collected_revenues(budget_allocation)

        self.daily_revenue = int(np.sum(daily_collected_revenues))

        self.daily_regret = self.get_daily_regret(self.daily_clicks, self.optimal_daily_clicks,
                                                  self.daily_revenue, optimal_daily_revenue)

        return self.daily_regret, self.daily_revenue

    def get_daily_regret(self, daily_clicks, optimal_daily_clicks, daily_revenue, optimal_daily_revenue):
        """
        :param daily_clicks:
        :param optimal_daily_clicks:
        :param daily_revenue:
        :param optimal_daily_revenue:
        :return:
        """
        best = optimal_daily_clicks * optimal_daily_revenue
        learned = daily_clicks * daily_revenue
        print(best, learned)
        return best - learned

    def get_updated_parameters(self):
        return self.advertising_learner
