import numpy as np

from project.part_4.Env_4 import Env_4


class Context(Env_4):

    def __init__(self, context_name, classes, initial_date, n_days, users_per_day, n_arms, feature):
        """
        constructor for the class, when called it creates the demand curve for the context
        based on the classes
        :param context_name:
        :param classes: array of classes in context
        :param initial_date:
        :param n_days:
        :param users_per_day: number of rounds for each day
        :param n_arms: number of arms of TS algorithm
        """

        super().__init__(initial_date, n_days)

        self.feature = feature
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
