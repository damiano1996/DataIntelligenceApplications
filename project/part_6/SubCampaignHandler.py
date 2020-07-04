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
        n_daily_clicks = self.advertising.get_num_clicks(budget_allocation)

        # extracting the daily reward from the TS
        collected_rewards, optimal_rewards = self.pricing.get_daily_reward(n_daily_clicks) 
        
        print ('class:', self.class_name, 'budget allocation (arm):', budget_allocation, 'clicks:', n_daily_clicks)
        
        # Below the regret computed knowing the optimal for each user
        plt.plot(np.cumsum(optimal_rewards - collected_rewards), label='Regret of the true evaluation ' + self.class_name)
        plt.xlabel('Time')
        plt.ylabel('Regret')
        plt.legend()
        plt.show()

        return self.advertising.learner


        """
        daily_regret = self.get_daily_regret(n_daily_clicks_real,
                                             real_budget_allocation, learned_budget_allocation,
                                             best_daily_reward, learned_daily_reward)
        """
        #return n_daily_clicks_learned, daily_regret  # , v_j

    def get_daily_regret(self,
                         n_daily_clicks_real,
                         real_budget_allocation, learned_budget_allocation,
                         best_daily_reward, learned_daily_reward):
        """
        :param n_daily_clicks_real: 
        :param real_budget_allocation: 
        :param learned_budget_allocation: 
        :param best_daily_reward: 
        :param learned_daily_reward: 
        :return: 
        """
        best = n_daily_clicks_real * real_budget_allocation * best_daily_reward
        learned = n_daily_clicks_real * learned_budget_allocation * learned_daily_reward
        return best - learned
