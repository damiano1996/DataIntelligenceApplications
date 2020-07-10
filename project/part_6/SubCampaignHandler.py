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

    def daily_update(self, budget_allocation):
        """
            Daily update
        :param budget_allocation: Learned best budget allocation
        :return:
        """
        # extracting the daily reward from the TS
        collected_revenues, optimal_revenue, round_clicks, optimal_clicks = self.get_daily_reward(budget_allocation)

        daily_regret = self.get_daily_regret(optimal_clicks, optimal_revenue, collected_revenues)
        daily_revenue = int(np.sum(collected_revenues))

        return daily_regret, daily_revenue

    # Da modificare con ottimo unito adv+pricing
    def get_daily_regret(self, optimal_daily_clicks, optimal_reward, collected_rewards):
        """
        :param optimal_daily_clicks: 
        :param optimal_reward: 
        :param collected_rewards:
        :return: regret of the current day
        """
        best = optimal_daily_clicks * optimal_reward
        learned = np.sum(collected_rewards)
        return best - learned

    def get_update_parameters(self):
        return self.advertising_learner
