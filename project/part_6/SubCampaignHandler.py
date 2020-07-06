from project.part_6.Advertising import Advertising
from project.part_6.Pricing import Pricing
import numpy as np
import matplotlib.pyplot as plt

from project.part_6.TemporaryConfig import classes_config

class SubCampaignHandler: 
    """
        This class implements the "Subcampaign j" block of the other_files/schema.jpg
    """

    def __init__(self, class_name, multi_class_handler, n_arms_pricing, n_arms_advertising):
        self.class_name = class_name
        self.mch = multi_class_handler

        self.n_arms_pricing = n_arms_pricing
        self.n_arms_advertising = n_arms_advertising

        self.advertising = Advertising(self.n_arms_advertising, classes_config[class_name])
        self.pricing = Pricing(class_name, self.mch, self.n_arms_pricing)


    def daily_update(self, budget_allocation):
        """
            Daily update
        :param budget_allocation: Learned best budget allocation
        :return:
        """

        # number of clicks of the current day
        collected_daily_clicks, optimal_daily_clicks = self.advertising.get_num_clicks(budget_allocation)

        # extracting the daily reward from the TS
        collected_rewards, optimal_reward = self.pricing.get_daily_reward(collected_daily_clicks) 
        
        print ('class:', self.class_name, 'budget allocation (arm):', budget_allocation, 
                'collected clicks:', collected_daily_clicks, 'optimal clicks:', optimal_daily_clicks,
                'collected revenue:', int(np.sum(collected_rewards)), 'optimal revenue:', int(optimal_reward * optimal_daily_clicks))
        
        #For viewing purpose
        import time
        #time.sleep(1)
        
        daily_regret = self.get_daily_regret(optimal_daily_clicks, optimal_reward, collected_rewards)
        daily_revenue = int(np.sum(collected_rewards))
        
        return daily_regret, daily_revenue

    #Da modificare con ottimo unito adv+pricing
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

    def get_update_parameters (self):
        return self.advertising.learner