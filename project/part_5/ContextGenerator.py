import copy
import math
import operator

import numpy as np

from project.dia_pckg.Config import features_space, classes_config
from project.part_5.Context import Context


class ContextGenerator:

    def __init__(self, multi_class_handler, mab_algorithm, mab_args):

        self.mch = multi_class_handler
        self.mab_algorithm = mab_algorithm
        self.mab_args = mab_args

    def get_weekly_contexts(self, last_contexts, users_counters, rewards_counters):
        """
        :param last_contexts: dictionary containing Context objects
        :param users_counters: dictionary containing counters of users for each class
        :param rewards_counters: dictionary containing counters of rewards for each class
        :return: dictionary containing Context objects
        """
        report = 'Generation context '

        if len(last_contexts) == 0:
            # create aggregate context
            my_features = [feat['features'] for feat in classes_config.values()]
            new_contexts = {'context_1': Context(features=my_features, mab_algorithm=self.mab_algorithm,
                                                 mab_args=self.mab_args)}
            report += 'aggregate '

        elif len(last_contexts) == 1:
            cont = {}
            not_cont = {}
            low_bound = {}
            
            for feature in features_space.keys():
                cont[feature], not_cont[feature] = self.split(feature, last_contexts['context_1'])
                # low_bound[feature] = self.get_low_bound(cont[feature], not_cont[feature], users_counters, rewards_counters)
                low_bound[feature] = self.get_mean_value(cont[feature], not_cont[feature], users_counters, rewards_counters)
                
            best_feature = max(low_bound.items(), key=operator.itemgetter(1))[0]
            # parent_low_bound = self.get_low_bound(last_contexts['context_1'].features, [], users_counters, rewards_counters)
            parent_low_bound = self.get_mean_value(last_contexts['context_1'].features, [], users_counters, rewards_counters)
            if low_bound[best_feature] > parent_low_bound:
                # split
                new_contexts = {
                    'context_1': Context(features=cont[best_feature], mab_algorithm=self.mab_algorithm,
                                         mab_args=self.mab_args),
                    'context_2': Context(features=not_cont[best_feature], mab_algorithm=self.mab_algorithm,
                                         mab_args=self.mab_args)}
                report += 'split 1 -> 2 features '
            else:
                # no split
                new_contexts = {'context_1': copy.deepcopy(last_contexts['context_1'])}
                report += 'no split 1 feature '

        elif len(last_contexts) == 2:
            if last_contexts['context_1'].features == [[0, 0], [0, 1]]:
                cont, not_cont = self.split('profession', last_contexts['context_1'])
                # low_bound = self.get_low_bound(cont, not_cont, users_counters, rewards_counters)
                low_bound = self.get_mean_value(cont, not_cont, users_counters, rewards_counters)
            else:
                cont, not_cont = self.split('age', last_contexts['context_1'])
                # low_bound = self.get_low_bound(cont, not_cont, users_counters, rewards_counters)
                low_bound = self.get_mean_value(cont, not_cont, users_counters, rewards_counters)
            # add possibility to recombine contexts
            # parent_low_bound = self.get_low_bound(last_contexts['context_1'].features, [], users_counters, rewards_counters)
            parent_low_bound = self.get_mean_value(last_contexts['context_1'].features, [], users_counters, rewards_counters)
            if low_bound > parent_low_bound:
                # split
                new_contexts = {
                    'context_1': Context(features=cont, mab_algorithm=self.mab_algorithm,
                                         mab_args=self.mab_args),
                    'context_2': Context(features=not_cont, mab_algorithm=self.mab_algorithm,
                                         mab_args=self.mab_args),
                    'context_3': copy.deepcopy(last_contexts['context_2'])}
                report += 'split 2 -> 3 features '
            else:
                # no split
                new_contexts = {
                    'context_1': copy.deepcopy(last_contexts['context_1']),
                    'context_2': copy.deepcopy(last_contexts['context_2'])}
                report += 'no split 2 feature '
        
        else:
            # no split
            new_contexts = {
                'context_1': copy.deepcopy(last_contexts['context_1']),
                'context_2': copy.deepcopy(last_contexts['context_2']),
                'context_3': copy.deepcopy(last_contexts['context_3'])}
            #new_contexts = copy.deepcopy(last_contexts) #sembra non funzionare a dovere, o  comunque da una peggiore regret
            report += 'no split 3 feature '

        # Initialization of the new learners
        if len(new_contexts) == 2 and len(last_contexts) != len(new_contexts):
            prior = last_contexts['context_1'].learner.beta_parameters
            rewards_per_arm = last_contexts['context_1'].learner.rewards_per_arm

            new_contexts['context_1'].learner.initialize_learner(prior, rewards_per_arm)
            new_contexts['context_2'].learner.initialize_learner(prior, rewards_per_arm)

            report += '| Initialized prior 2 features'

        elif len(new_contexts) == 3 and len(last_contexts) != len(new_contexts):
            prior = last_contexts['context_1'].learner.beta_parameters
            rewards_per_arm = last_contexts['context_1'].learner.rewards_per_arm

            new_contexts['context_1'].learner.initialize_learner(prior, rewards_per_arm)
            new_contexts['context_2'].learner.initialize_learner(prior, rewards_per_arm)

            report += '| Initialized prior 3 features'
        
        print(report)
        return new_contexts

    def split(self, feature_name, context):
        """
        this function splits according to the considered feature
        :param feature_name: the feature we want to evaluate
        :param context: Context object: the context we want to split
        :return:
        """
        class_cont = {}
        class_not_cont = {}
        if len(context.features) == 3:
            if feature_name == 'age':
                class_cont = [[0, 0], [0, 1]]
                class_not_cont = [[1, 1]]
            else:
                class_cont = [[1, 1], [0, 1]]
                class_not_cont = [[0, 0]]

        elif len(context.features) == 2:
            if feature_name == 'age':
                class_cont = [[1, 1]]
                class_not_cont = [[0, 1]]
            else:
                class_cont = [[0, 1]]
                class_not_cont = [[0, 0]]

        return class_cont, class_not_cont

    def get_low_bound(self, conts, not_cont, users_counters, rewards_counters):
        """
            This function evaluates a feature based on the classes that it splits
        :param conts: list of features e.g.: [[0, 0], [0, 1]]
        :param not_cont: feature: always one feature
        :param users_counters: dictionary containing counters of users for each class
        :param rewards_counters: dictionary containing counters of rewards for each class
        :return:
        """
        delta = 0.05
        z_1 = 0
        x_1 = 0
        z_2 = np.finfo(np.float32).eps
        x_2 = 0

        for class_ in self.mch.classes:
            class_name = class_.name
            for cont in conts:
                if cont == class_.features:
                    z_1 += users_counters[class_name]
                    x_1 += rewards_counters[class_name]

            if not_cont == class_.features:
                z_2 += users_counters[class_name]
                x_2 += rewards_counters[class_name]

        tot = z_1 + z_2
        cont_val = (z_1 / tot) * (x_1 - math.sqrt(-math.log(delta) / (2 * z_1)))
        not_cont_val = (z_2 / tot) * (x_2 - math.sqrt(-math.log(delta) / (2 * z_2)))
        return cont_val + not_cont_val

    # rew_cont/user_cont + rew_not_cont/user_not_cont
    def get_mean_value(self, conts, not_cont, users_counters, rewards_counters):
        z_1 = 0
        x_1 = 0
        z_2 = 0
        x_2 = 0

        for class_ in self.mch.classes:
            class_name = class_.name
            for cont in conts:
                if cont == class_.features:
                    z_1 += users_counters[class_name]
                    x_1 += rewards_counters[class_name]

            if not_cont == class_.features:
                z_2 += users_counters[class_name]
                x_2 += rewards_counters[class_name]

        cont_value = x_1 / z_1 if z_1 > 0 else 0
        not_cont_value = x_2 / z_2 if z_2 > 0 else 0

        return cont_value + not_cont_value
