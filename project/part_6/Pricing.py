from project.dia_pckg.User import User
from project.part_4.Env_4 import Env_4
from project.part_4.TS_Learner import TS_Learner


class Pricing:
    """
        This class is an extension of parts 4 and 5
    """

    def __init__(self,
                 class_name,
                 multi_class_handler,
                 n_arms):
        """
        :param class_name:
        :param multi_class_handler:
        :param n_arms:
        """

        self.mch = multi_class_handler
        self.n_arms = n_arms
        self.class_name = class_name

        # self.pricing_learner = SWTS_Learner(n_arms=n_arms, arm_prices=self.get_candidate_prices()['prices'], window_size=5000)
        self.learner = TS_Learner(n_arms=self.n_arms, arm_prices=self.get_candidate_prices()['prices'])

        self.optimal_revenue = self.get_optimal_revenue()

    def get_daily_revenue(self, daily_clicks, fix_arm=None):  # to change n_arms
        """
            Get the daily reward and the optimal one
        """

        daily_revenue = 0

        if daily_clicks == 0:
            return daily_revenue

        # Generate an environment for a day simulation
        env = Env_4(initial_date='20200101',
                    n_days=1,
                    users_per_day=daily_clicks,
                    multi_class_handler=self.mch,
                    n_arms=self.n_arms)

        _, done = env.reset()
        while not done:
            user = User(class_name=self.class_name)

            if fix_arm is None:
                pulled_arm = self.learner.pull_arm_revenue()  # optimize by revenue

                reward, _, done, _ = env.round(pulled_arm, user)

                self.learner.update(pulled_arm, reward)

                # optimal_revenues = np.append(optimal_revenues, opt_revenue)
                daily_revenue += self.learner.get_real_reward(pulled_arm, reward)

            else:

                reward, _, done, _ = env.round(fix_arm, user)
                daily_revenue += self.learner.get_real_reward(fix_arm, reward)

        return daily_revenue

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

    def get_optimal_revenue(self):
        opt = self.mch.get_optimal(class_name=self.class_name)
        optimal_revenue = opt['price'] * opt['probability']
        return optimal_revenue
