import copy
import math
import operator

import numpy as np

from project.dia_pckg.Config import features_space, classes_config
from project.part_5.Context_B import Context_B


class ContextGenerator:

    def __init__(self, multi_class_handler, mab_algorithm, mab_args):

        self.mch = multi_class_handler
        self.mab_algorithm = mab_algorithm
        self.mab_args = mab_args

    def get_weekly_contexts(self, users_counter, contexts, sales):
        """
        :param users_counter: dictionary of class->number of users, they are users collected from the beginning of the campaign
        :param contexts: the list of contexts used in the previous iteration
        :param sales: dictionary class->sold items during the week
        :return: dictionary of the following shape:
                {'context_1': features, 'context_2': features, ...}
                    where features is a list containing the features of the context: e.g. ['<30', 'worker]
        """
        if len(contexts) == 0:
            # create aggregate context
            my_features = [feat['features'] for feat in classes_config.values()]
            new_contexts = {'context_1': Context_B(features=my_features, mab_algorithm=self.mab_algorithm,
                                                   mab_args=self.mab_args)}

        elif len(contexts) == 1:
            cont = {}
            not_cont = {}
            low_bound = {}
            for feature in features_space.keys():
                cont[feature], not_cont[feature] = self.split(feature, contexts['context_1'])
                low_bound[feature] = self.get_low_bound(cont[feature], not_cont[feature], users_counter, sales)

            best_feature = max(low_bound.items(), key=operator.itemgetter(1))[0]
            if low_bound[best_feature] > self.get_low_bound(contexts['context_1'].classes, [], users_counter, sales):
                # split

                new_contexts = {
                    'context_1': Context_B(features=cont, mab_algorithm=self.mab_algorithm,
                                           mab_args=self.mab_args),
                    'context_2': Context_B(features=not_cont, mab_algorithm=self.mab_algorithm,
                                           mab_args=self.mab_args)}
            else:
                # no split
                new_contexts = {'context_1': copy.deepcopy(contexts['context_1'])}

        elif len(contexts) == 2:
            if contexts['context_1'].feature == 'age':
                cont, not_cont = self.split('profession', contexts['context_1'])
                feature = 'profession'
                low_bound = self.get_low_bound(cont, not_cont, users_counter, sales)
            else:
                cont, not_cont = self.split('age', contexts['context_1'])
                feature = 'age'
                low_bound = self.get_low_bound(cont, not_cont, users_counter, sales)
            # add possibility to recombine contexts
            if low_bound > self.get_low_bound(contexts['context_1'].features, [], users_counter, sales):
                # split
                new_contexts = {
                    'context_1': Context_B(features=cont, mab_algorithm=self.mab_algorithm,
                                           mab_args=self.mab_args),
                    'context_2': Context_B(features=not_cont, mab_algorithm=self.mab_algorithm,
                                           mab_args=self.mab_args),
                    'context_3': copy.deepcopy(contexts['context_2'])}
            else:
                # no split
                new_contexts = {
                    'context_1': copy.deepcopy(contexts['context_1']),
                    'context_2': copy.deepcopy(contexts['context_2'])}
        else:
            # add possibility to recombine contexts
            new_contexts = copy.deepcopy(contexts)

        if len(new_contexts) == 2:
            prior = contexts['context_1'].learner.beta_parameters
            rewards_per_arm = contexts['context_1'].learner.rewards_per_arm

            new_contexts['context_1'].learner.initialize_learner(prior, rewards_per_arm)
            new_contexts['context_2'].learner.initialize_learner(prior, rewards_per_arm)

        elif len(new_contexts) == 3:
            prior = contexts['context_1'].learner.beta_parameters
            rewards_per_arm = contexts['context_1'].learner.rewards_per_arm

            new_contexts['context_1'].learner.initialize_learner(prior, rewards_per_arm)
            new_contexts['context_2'].learner.initialize_learner(prior, rewards_per_arm)
            new_contexts['context_3'].learner.initialize_learner(prior, rewards_per_arm)

        return new_contexts

    def split(self, feature, context):
        """
        this function splits according to the considered feature
        :param feature: the feature we want to evaluate
        :param context: the context we want to split
        :return:
        """
        class_cont = {}
        class_not_cont = {}
        if len(context.features) == 3:
            if feature == 'age':
                class_cont = [[0, 0], [0, 1]]
                class_not_cont = [1, 1]
            else:

                class_cont = [[1, 1], [0, 1]]
                class_not_cont = [0, 0]

        elif len(context.features) == 2:
            if feature == 'age':
                class_cont = [[1, 1]]
                class_not_cont = [0, 1]
            else:
                class_cont = [[0, 1]]
                class_not_cont = [0, 0]

        return class_cont, class_not_cont

    def get_low_bound(self, conts, not_cont, users, sales):
        """
        this function evaluates a feature based on the classes that it splits
        :param sales:
        :param users: number of users in the last week for each class
        :param cont: the class we want to put in the context
        :param not_cont: the class we don't want to put in the context
        :return: the lower bound of the context to be generated
        """
        delta_1 = 5
        z_1 = 0
        x_1 = 0
        delta_2 = 5
        z_2 = np.finfo(np.float32).eps
        x_2 = 0

        for class_ in self.mch.classes:
            class_name = class_.name
            for cont in conts:
                if cont == class_.features:
                    z_1 += users[class_name]
                    x_1 += sales[class_name]

            if not_cont == class_.features:
                z_2 += users[class_name]
                x_2 += sales[class_name]

        tot = z_1 + z_2

        return z_1 / tot * (x_1 - math.sqrt(-math.log(delta_1) / 2 * z_1)) + z_2 / tot * (
                x_2 - math.sqrt(-math.log(delta_2) / 2 * z_2))


if __name__ == '__main__':
    a = {'a': 5, 'b': 4}

    b = 1

    print(len(a))
