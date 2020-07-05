import numpy as np
from project.part_4.TS_Learner import TS_Learner
from project.part_4.Env_4 import Env_4
from project.dia_pckg.User import User

class Pricing:
    """
        This class is an extension of parts 4 and 5
    """

    def __init__(self, class_name, multi_class_handler, n_arms=20):
        self.mch = multi_class_handler
        self.n_arms = n_arms
        self.class_name = class_name

        # ts_learner = SWTS_Learner(n_arms=n_arms, arm_prices=env.arm_prices['prices'], window_size=2000)
        self.ts_learner = TS_Learner(n_arms=n_arms, arm_prices=self.get_candidate_prices()['prices'])


    def get_daily_reward(self, n_daily_clicks): #to change n_arms
        """
            Get the daily reward and the optimal one
        """
        optimal_revenue = self.get_optimal_revenue()
        collected_revenues = np.array([])

        if (n_daily_clicks == 0):
            return collected_revenues, optimal_revenue
        
        #Generate an environment for a day simulation
        env = Env_4(initial_date='20200101',
                n_days=1,
                users_per_day=n_daily_clicks,
                mutli_class_handler=self.mch,
                n_arms=self.n_arms)

        _, done = env.reset()

        while not done:
            user = User(class_name=self.class_name)

            pulled_arm = self.ts_learner.pull_arm_revenue()  # optimize by revenue

            reward, _, done, _ = env.round(pulled_arm, user)

            self.ts_learner.update(pulled_arm, reward)
            
            #optimal_revenues = np.append(optimal_revenues, opt_revenue)
            collected_revenues = np.append(collected_revenues, self.ts_learner.get_real_reward(pulled_arm, reward))

        return collected_revenues, optimal_revenue




    def get_candidate_prices(self):
        """
            This method return the candidate prices, one price for each arm.
            The "indices" array contains the positions of the specified prices in the aggregate curve
        :return:
        """
        arm_distance = int(self.mch.aggregate_demand_curve['prices'].shape[0] / self.n_arms)
        idx = [int(arm_distance * arm) for arm in range(self.n_arms)]
        prices = self.mch.aggregate_demand_curve['prices'][idx]
        return {'indices': idx, 'prices': prices}

    
    def get_optimal_revenue (self):
        opt = self.mch.get_optimal(class_name=self.class_name)
        optimal_revenue = opt['price'] * opt['probability']

        return optimal_revenue
