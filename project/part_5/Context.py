import numpy as np

from project.part_4.Env_4 import Env_4


class Context(Env_4):

    def __init__(self, context_name, classes, feature, mch, mab_algorithm, mab_args):
        """
        constructor for the class, when called it creates the demand curve for the context
        based on the classes
        :param context_name:
        :param classes: array of classes in context
        :param feature: features of the context
        :param mab_algorithm: MAB algorithm to be created
        :param mab_args: arguments for the MAB learner
        """

        self.feature = feature
        self.name = context_name
        self.classes = classes
        self.n_classes = classes.len()
        self.arm_prices = self.get_candidate_prices()
        self.mch = mch
        self.MAB = mab_algorithm  # Multi Armed Bandit algorithm to use
        self.MAB_args = mab_args

        self.learner = self.MAB(*self.MAB_args)

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

        aggr_prob = np.mean(stack, axis=-1)
        return {'prices': prices, 'probabilities': aggr_prob}

    def get_optimals(self):
        """
        :return: (aggregate_optimal, array of optimals of the classes of the context)
        """
        if self.n_classes == 3:
            optimal_classes = {'class_1': self.mch.get_optimal_price(self.classes['class_1'].conv_rates['phase_0']),
                               'class_2': self.mch.get_optimal_price(self.classes['class_2'].conv_rates['phase_0']),
                               'class_3': self.mch.get_optimal_price(self.classes['class_3'].conv_rates['phase_0'])}
        elif self.n_classes == 2:
            optimal_classes = {'class_1': self.mch.get_optimal_price(self.classes['class_1'].conv_rates['phase_0']),
                               'class_2': self.mch.get_optimal_price(self.classes['class_2'].conv_rates['phase_0'])}
        else:
            optimal_classes = {'class_1': self.mch.get_optimal_price(self.classes['class_1'].conv_rates['phase_0'])}

        return {'context': self.mch.get_optimal_price(self.context_demand_curve),
                'classes': optimal_classes}

    def is_user_belonging(self, user):
        """
        Return if the user belongs to this context by looking at common features
        :param user: User object
        :return: if the user belongs to this context
        """
        if user.features in self.feature:
            return True
        return False
