from project.part_6.Advertising import Advertising
from project.part_6.Pricing import Pricing
import numpy as np
import matplotlib.pyplot as plt

class SubCampaignHandler:  # Can we implement the SubCampaign Class?

    """
        This class implements the "Subcampaign j" block of the other_files/schema.jpg
    """

    def __init__(self, class_name, multi_class_handler):
        self.class_name = class_name
        self.mch = multi_class_handler

        self.advertising = Advertising()
        self.pricing = Pricing(class_name,self.mch)


    def daily_update(self, learned_budget_allocation, real_budget_allocation):
        """
            Daily update
        :param learned_budget_allocation: Learned best budget
        :param real_budget_allocation: Real best budget
        :return:
        """

        # number of clicks of the current day
        #n_daily_clicks_learned, n_daily_clicks_real = self.advertising.get_num_clicks(learned_budget_allocation)
        #n_daily_clicks = 500 in toeria non c'è learned o real (?)
        n_daily_clicks = 10000

        # extracting the daily reward from the TS
        collected_rewards, optimal_rewards = self.pricing.get_daily_collected_reward(n_daily_clicks) 
        
        """
        daily_regret = self.get_daily_regret(n_daily_clicks_real,
                                             real_budget_allocation, learned_budget_allocation,
                                             best_daily_reward, learned_daily_reward)
        """
        
        # Below the regret computed knowing the optimal for each user
        plt.plot(np.cumsum(optimal_rewards - collected_rewards), label='Regret of the true evaluation')
        plt.xlabel('Time')
        plt.ylabel('Regret')
        plt.legend()
        plt.show()

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
