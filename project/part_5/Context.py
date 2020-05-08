import numpy as np

from project.dia_pckg.Environment import Environment


class Context(Environment):

    def __init__(self, context_name, classes, initial_date, n_days, users_per_day, n_arms):
        '''
        constructor for the class, when called it creates the demand curve for the context
        based on the classes
        :param context_name:
        :param classes: array of classes in context
        :param initial_date:
        :param n_days:
        :param users_per_day: number of rounds for each day
        :param n_arms: number of arms of TS algorithm
        '''

        super().__init__(initial_date, n_days)

        self.name = context_name
        self.classes = classes
        self.n_classes = classes.len()
        self.round_per_day = users_per_day
        self.count_rounds_today = 0
        self.initial_date = initial_date
        self.n_days = n_days
        self.users_per_day = users_per_day
        self.n_arms = n_arms
        self.arm_prices = self.get_candidate_prices()

        if self.n_classes == 3:
            self.classes = {'class_1': classes[0], 'class_2': classes[1], 'class_3': classes[2]}
        elif self.n_classes == 2:
            self.classes = {'class_1': classes[0], 'class_2': classes[1]}
        else:
            self.classes = {'class_1': classes[0]}

        self.context_demand_curve = self.get_aggregate_curve()

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

        return reward, current_date, done, opt_revenue

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
        return reward, optimal_revenue

    def reset(self):
        """
            to reset the environment
        :return: None
        """
        self.count_rounds_today = 0
        return super(Context, self).reset()

    def get_aggregate_curve(self):
        """
        :return: the aggregate curve
        """

        prices = self.classes['class_1'].conv_rates['phase_0']['prices']

        if self.n_classes == 3:
            stack = np.stack(
                [self.classes['class_1'].conv_rates['phase_0']['probabilities'],
                 self.classes['class_2'].conv_rates['phase_0']['probabilities'],
                 self.classes['class_3'].conv_rates['phase_0']['probabilities']], axis=1
            )
        elif self.n_classes == 2:
            stack = np.stack(
                [self.classes['class_1'].conv_rates['phase_0']['probabilities'],
                 self.classes['class_2'].conv_rates['phase_0']['probabilities']], axis=1
            )
        else:
            stack = self.classes['class_1'].conv_rates['phase_0']['probabilities']

        aggr_proba = np.mean(stack, axis=-1)
        return {'prices': prices, 'probabilities': aggr_proba}

    def get_optimals(self):
        """
        :return: (aggregate_optimal, array of optimals of the classes of the context)
        """
        if self.n_classes == 3:
            optimal_classes = {'class_1': self.get_optimal_price(self.classes['class_1'].conv_rates['phase_0']),
                               'class_2': self.get_optimal_price(self.classes['class_2'].conv_rates['phase_0']),
                               'class_3': self.get_optimal_price(self.classes['class_3'].conv_rates['phase_0'])}
        elif self.n_classes == 2:
            optimal_classes = {'class_1': self.get_optimal_price(self.classes['class_1'].conv_rates['phase_0']),
                               'class_2': self.get_optimal_price(self.classes['class_2'].conv_rates['phase_0'])}
        else:
            optimal_classes = {'class_1': self.get_optimal_price(self.classes['class_1'].conv_rates['phase_0'])}

        return {'context': self.get_optimal_price(self.context_demand_curve),
                'classes': optimal_classes}

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
        arm_distance = int(self.context_demand_curve['prices'].shape[0] / self.n_arms)
        idx = [int(arm_distance * arm) for arm in range(self.n_arms)]
        prices = self.context_demand_curve['prices'][idx]
        return {'indices': idx, 'prices': prices}
