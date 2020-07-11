import numpy as np

from project.dia_pckg.User import User
from project.part_4.Env_4 import Env_4
from project.part_4.TS_Learner import TS_Learner
from project.part_6.Advertising import Advertising


class Pricing(Advertising):
    """
        This class is an extension of parts 4 and 5
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
        :param n_arms_advertising:
        :param n_arms_advertising:
        """
        super(Pricing, self).__init__(n_arms_advertising=n_arms_advertising, subcampaign_name=subcampaign_name)

        self.mch = multi_class_handler
        self.n_arms_pricing = n_arms_pricing
        self.class_name = class_name

        # self.pricing_learner = SWTS_Learner(n_arms=n_arms, arm_prices=self.get_candidate_prices()['prices'], window_size=5000)
        self.pricing_learner = TS_Learner(n_arms=self.n_arms_pricing, arm_prices=self.get_candidate_prices()['prices'])

        self.daily_collected_revenues = 0
        self.optimal_daily_revenue = 0

    def get_daily_collected_revenues(self, learned_budget_allocation):  # to change n_arms
        """
            Get the daily reward and the optimal one
        """
        # from the super class
        daily_clicks, optimal_daily_clicks = self.get_daily_clicks(learned_budget_allocation)

        self.optimal_daily_revenue = self.get_optimal_revenue()
        self.daily_collected_revenues = np.array([])

        if daily_clicks == 0:
            return self.daily_collected_revenues, self.optimal_daily_revenue

        # Generate an environment for a day simulation
        env = Env_4(initial_date='20200101',
                    n_days=1,
                    users_per_day=daily_clicks,
                    multi_class_handler=self.mch,
                    n_arms=self.n_arms_pricing)

        _, done = env.reset()

        while not done:
            user = User(class_name=self.class_name)

            pulled_arm = self.pricing_learner.pull_arm_revenue()  # optimize by revenue

            reward, _, done, _ = env.round(pulled_arm, user)

            self.pricing_learner.update(pulled_arm, reward)

            # optimal_revenues = np.append(optimal_revenues, opt_revenue)
            self.daily_collected_revenues = np.append(self.daily_collected_revenues,
                                                      self.pricing_learner.get_real_reward(pulled_arm, reward))

        return self.daily_collected_revenues, self.optimal_daily_revenue

    def get_candidate_prices(self):
        """
            This method return the candidate prices, one price for each arm.
            The "indices" array contains the positions of the specified prices in the aggregate curve
        :return:
        """
        arm_distance = int(self.mch.aggregate_demand_curve['prices'].shape[0] / self.n_arms_pricing)
        idx = [int(arm_distance * arm) for arm in range(self.n_arms_pricing)]
        prices = self.mch.aggregate_demand_curve['prices'][idx]
        return {'indices': idx, 'prices': prices}

    def get_optimal_revenue(self):
        opt = self.mch.get_optimal(class_name=self.class_name)
        optimal_revenue = opt['price'] * opt['probability']
        return optimal_revenue
