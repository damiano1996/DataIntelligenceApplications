import numpy as np

from project.dia_pckg.Environment import Environment


class Env_4(Environment):

    def __init__(self, initial_date, n_days, users_per_day,
                 class_1, class_2, class_3, n_arms):
        """
        :param initial_date: when the campaign begins
        :param n_days: number of days of the campaign
        :param users_per_day: number of users per day
        :param class_1: Class object
        :param class_2: Class object
        :param class_3: Class object
        :param n_arms: number of arms of the Thomson Sampling algorithm
        """
        super().__init__(initial_date, n_days)

        self.round_per_day = users_per_day
        self.count_rounds_today = 0

        self.classes = {'class_1': class_1, 'class_2': class_2, 'class_3': class_3}
        self.aggregate_demand_curve = self.get_aggregate_curve()

        self.n_arms = n_arms
        self.arm_prices = self.get_candidate_prices()

    def user_step(self, pulled_arm, user):
        """
            This method performs a round considering the number of steps per day
            Only after n rounds it perform a step in the implemented class
        :param pulled_arm: arm to pull
        :param user: User object
        :return: (reward, current date, done) done is a boolean -> True if the "game" is finished
        """
        reward, opt_revenue = self.round(pulled_arm, user)

        current_date = self.get_current_date()
        done = False

        self.count_rounds_today += 1
        if self.count_rounds_today == self.round_per_day:
            self.count_rounds_today = 0
            current_date, done = self.step()

        return (reward, current_date, done, opt_revenue)

    def round(self, pulled_arm, user):
        """
            This method performs a round taking the probability from the user's class
        :param pulled_arm: arm to pull
        :param user: User object
        :return: reward
        """
        # class of the user
        conv_rate = None
        for class_ in self.classes.values():
            if user.class_name == class_.name:
                conv_rate = class_.conv_rates['phase_0']  # taking the first because no abrupt phases

        # taking the probability from the conversion curve, associated to the pulled_arm
        probability = conv_rate['probabilities'][self.arm_prices['indices'][pulled_arm]]
        optimals = self.get_optimal_price(conv_rate)
        optimal_revenue = optimals['price'] * optimals['probability']

        reward = np.random.binomial(1, probability)
        return (reward, optimal_revenue)

    def reset(self):
        """
            to reset the environment
        :return: None
        """
        self.count_rounds_today = 0
        return super(Env_4, self).reset()

    def get_aggregate_curve(self):
        """
        :return: the aggregate curve
        """
        prices = self.classes['class_1'].conv_rates['phase_0']['prices']

        stack = np.stack(
            [self.classes['class_1'].conv_rates['phase_0']['probabilities'],
             self.classes['class_2'].conv_rates['phase_0']['probabilities'],
             self.classes['class_3'].conv_rates['phase_0']['probabilities']], axis=1
        )
        aggr_proba = np.mean(stack, axis=-1)
        return {'prices': prices, 'probabilities': aggr_proba}

    def get_optimals(self):
        """
        :return: (aggregate_optimal, class_1_optimal, class_2_optimal, class_3_optimal)
        """
        return {'aggregate': self.get_optimal_price(self.aggregate_demand_curve),
                'class_1': self.get_optimal_price(self.classes['class_1'].conv_rates['phase_0']),
                'class_2': self.get_optimal_price(self.classes['class_2'].conv_rates['phase_0']),
                'class_3': self.get_optimal_price(self.classes['class_3'].conv_rates['phase_0'])}

    def get_optimal_price(self, conv_rate):
        """
            This method computes the max area
        :param conv_rate: (price, probability)
        :return:
        """
        areas = conv_rate['prices'] * conv_rate['probabilities']
        idx = np.argmax(areas)
        return {'price': conv_rate['prices'][idx],
                'probability': conv_rate['probabilities'][idx]}

    def get_candidate_prices(self):
        """
            This method return the candidate prices, one price for each arm.
            The "indices" array contains the positions of the specified prices in the aggregate curve
        :return:
        """
        arm_distance = int(self.aggregate_demand_curve['prices'].shape[0] / self.n_arms)
        idx = [int(arm_distance * arm) for arm in range(self.n_arms)]
        prices = self.aggregate_demand_curve['prices'][idx]
        return {'indices': idx, 'prices': prices}
