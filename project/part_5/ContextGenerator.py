import copy
import math
import operator

from project.dia_pckg.Config import features_space, classes_config
from project.part_5.Context import Context


class ContextGenerator:

    def __init__(self, multi_class_handler, mab_algorithm, mab_args):

        self.mch = multi_class_handler
        self.mab_algorithm = mab_algorithm
        self.mab_args = mab_args

        self.report = ''

    def get_weekly_contexts(self, last_contexts, rewards_counters):
        """
        :param last_contexts: dictionary containing Context objects
        :param rewards_counters: dictionary containing counters of rewards for each class
        :return: dictionary containing Context objects
        """
        self.report = 'Generation context '

        if len(last_contexts) == 0:
            # create aggregate context
            my_features = [feat for feat in classes_config.values()]
            new_contexts = {'context_1': Context(features=my_features, mab_algorithm=self.mab_algorithm,
                                                 mab_args=self.mab_args)}
            self.report += 'aggregate '

        elif len(last_contexts) == 1:
            cont = {}
            not_cont = {}
            low_bound = {}

            for feature in features_space.keys():
                cont[feature], not_cont[feature] = self.split(feature, last_contexts['context_1'])
                print(cont[feature])
                print(not_cont[feature])
                low_bound[feature] = self.get_low_bound(cont[feature], not_cont[feature], rewards_counters)
                # low_bound[feature] = self.get_mean_value(cont[feature], not_cont[feature], users_counters, rewards_counters)
                print(low_bound[feature])
            best_feature = max(low_bound.items(), key=operator.itemgetter(1))[0]
            parent_low_bound = self.get_low_bound(last_contexts['context_1'].features, [], rewards_counters)
            # parent_low_bound = self.get_mean_value(last_contexts['context_1'].features, [], users_counters, rewards_counters)
            print(low_bound[best_feature])
            print(parent_low_bound)
            if low_bound[best_feature] > parent_low_bound:
                # split
                new_contexts = {
                    'context_1': Context(features=cont[best_feature], mab_algorithm=self.mab_algorithm,
                                         mab_args=self.mab_args),
                    'context_2': Context(features=not_cont[best_feature], mab_algorithm=self.mab_algorithm,
                                         mab_args=self.mab_args)}
                self.report += 'split 1 -> 2 features '

            else:
                # no split
                new_contexts = {'context_1': copy.deepcopy(last_contexts['context_1'])}
                self.report += 'no split 1 feature '

        elif len(last_contexts) == 2:
            if last_contexts['context_1'].features == [[0, 0], [0, 1]]:
                cont, not_cont = self.split('profession', last_contexts['context_1'])
                low_bound = self.get_low_bound(cont, not_cont, rewards_counters)
                # low_bound = self.get_mean_value(cont, not_cont, users_counters, rewards_counters)
            else:
                cont, not_cont = self.split('age', last_contexts['context_1'])
                low_bound = self.get_low_bound(cont, not_cont, rewards_counters)
                # low_bound = self.get_mean_value(cont, not_cont, users_counters, rewards_counters)
            # add possibility to recombine contexts
            parent_low_bound = self.get_low_bound(last_contexts['context_1'].features, [], rewards_counters)
            combined_low_bound = self.get_combined_bound(rewards_counters)

            extra_low_bound = self.get_low_bound([], last_contexts['context_2'].features, rewards_counters)
            # parent_low_bound = self.get_mean_value(last_contexts['context_1'].features, [], users_counters, rewards_counters)
            print(low_bound)
            print(parent_low_bound)
            print(combined_low_bound)
            if combined_low_bound > low_bound + extra_low_bound:
                if combined_low_bound > parent_low_bound + extra_low_bound:
                    # create aggregate again
                    my_features = [feat['features'] for feat in classes_config.values()]
                    new_contexts = {'context_1': Context(features=my_features, mab_algorithm=self.mab_algorithm,
                                                         mab_args=self.mab_args)}
                    self.report += 'recombined -> aggregate context'
                else:
                    # no split
                    new_contexts = {
                        'context_1': copy.deepcopy(last_contexts['context_1']),
                        'context_2': copy.deepcopy(last_contexts['context_2'])}
                    self.report += 'no split 2 feature '
            else:
                if low_bound > parent_low_bound:
                    # split
                    new_contexts = {
                        'context_1': Context(features=cont, mab_algorithm=self.mab_algorithm,
                                             mab_args=self.mab_args),
                        'context_2': Context(features=not_cont, mab_algorithm=self.mab_algorithm,
                                             mab_args=self.mab_args),
                        'context_3': copy.deepcopy(last_contexts['context_2'])}
                    self.report += 'split 2 -> 3 features '
                else:
                    # no split
                    new_contexts = {
                        'context_1': copy.deepcopy(last_contexts['context_1']),
                        'context_2': copy.deepcopy(last_contexts['context_2'])}
                    self.report += 'no split 2 feature '

        else:
            cont = {}
            not_cont = {}
            low_bound = {}
            for feature in features_space.keys():
                cont[feature], not_cont[feature] = self.split(feature, last_contexts['context_1'])
                low_bound[feature] = self.get_low_bound(cont[feature], not_cont[feature], rewards_counters)

            best_feature = max(low_bound.items(), key=operator.itemgetter(1))[0]
            low_bound_old = self.get_low_bound(last_contexts['context_1'], [], rewards_counters) + \
                            self.get_low_bound(last_contexts['context_2'], [], rewards_counters) + \
                            self.get_low_bound(last_contexts['context_3'], [], rewards_counters)

            if low_bound[best_feature] > low_bound_old:
                # recombine 3 -> 2
                new_contexts = {
                    'contest_1': Context(features=cont, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args),
                    'contest_2': Context(features=not_cont, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)
                }
                self.report += 'recombined -> 2 features'
                prior_1 = 0
                rewards_per_arm_1 = 0
                prior_2 = 0
                rewards_per_arm_2 = 0
                for context in last_contexts:
                    if last_contexts[context].features == not_cont:
                        prior_2 = last_contexts[context].learner.beta_parameters
                        rewards_per_arm_2 = last_contexts[context].learner.rewards_per_arm
                    else:
                        prior_1 += last_contexts[context].learner.beta_parameters
                        rewards_per_arm_1 += last_contexts[context].learner.rewards_per_arm
                new_contexts['context_1'].learner.initialize_learner(prior_1/2, rewards_per_arm_1)
                new_contexts['context_2'].learner.initialize_learner(prior_2, rewards_per_arm_2)
            else:
                # no split
                new_contexts = {
                    'context_1': copy.deepcopy(last_contexts['context_1']),
                    'context_2': copy.deepcopy(last_contexts['context_2']),
                    'context_3': copy.deepcopy(last_contexts['context_3'])}
                # new_contexts = copy.deepcopy(last_contexts) #sembra non funzionare a dovere, o  comunque da una peggiore regret
                self.report += 'no split 3 feature '

        new_contexts = self.initialize_learners(last_contexts, new_contexts)
        print(self.report)
        return new_contexts

    def initialize_learners(self, last_contexts, new_contexts):
        # Initialization of the new learners
        if len(new_contexts) == 1 and len(last_contexts) == 2:
            prior_1 = last_contexts['context_1'].learner.beta_parameters
            rewards_per_arm_1 = last_contexts['context_1'].learner.rewards_per_arm
            prior_2 = last_contexts['context_2'].learner.beta_parameters
            rewards_per_arm_2 = last_contexts['context_2'].learner.rewards_per_arm

            prior = (prior_1 + prior_2) / 2
            rewards_per_arm = rewards_per_arm_1 + rewards_per_arm_2
            new_contexts['context_1'].learner.initialize_learner(prior, rewards_per_arm)

            self.report += '| Initialized prior aggregate'

        elif len(new_contexts) == 2 and len(last_contexts) == 3:
            self.report += '| Initialized prior 2 features'

        elif len(new_contexts) == 2 and len(last_contexts) != len(new_contexts):
            prior = last_contexts['context_1'].learner.beta_parameters
            rewards_per_arm = last_contexts['context_1'].learner.rewards_per_arm

            new_contexts['context_1'].learner.initialize_learner(prior, rewards_per_arm)
            new_contexts['context_2'].learner.initialize_learner(prior, rewards_per_arm)

            self.report += '| Initialized prior 2 features'

        elif len(new_contexts) == 3 and len(last_contexts) != len(new_contexts):
            prior_1 = last_contexts['context_1'].learner.beta_parameters
            rewards_per_arm_1 = last_contexts['context_1'].learner.rewards_per_arm
            prior_2 = last_contexts['context_2'].learner.beta_parameters
            rewards_per_arm_2 = last_contexts['context_2'].learner.rewards_per_arm

            new_contexts['context_1'].learner.initialize_learner(prior_1, rewards_per_arm_1)
            new_contexts['context_2'].learner.initialize_learner(prior_1, rewards_per_arm_1)
            new_contexts['context_3'].learner.initialize_learner(prior_2, rewards_per_arm_2)

            self.report += '| Initialized prior 3 features'
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
        if len(context.features) == 3 or len(context.features) == 1:
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

    def get_low_bound(self, conts, not_cont, rewards_counters):
        """
            This function evaluates a feature based on the classes that it splits
        :param conts: list of features e.g.: [[0, 0], [0, 1]]
        :param not_cont: feature: always one feature
        :param rewards_counters: dictionary containing counters of rewards for each class
        :return:
        """
        delta = 0.05
        z_1 = 0
        x_1 = 0
        z_2 = 0
        x_2 = 0

        print(conts, not_cont, rewards_counters)

        for cont in conts:
            z_1 += rewards_counters[(cont[0], cont[1])]['n_purchases']
            x_1 += rewards_counters[(cont[0], cont[1])]['total_reward']

        if len(not_cont) > 0:
            z_2 += rewards_counters[(not_cont[0][0], not_cont[0][1])]['n_purchases']
            x_2 += rewards_counters[(not_cont[0][0], not_cont[0][1])]['total_reward']

        print(x_1, x_2, z_1, z_2)
        tot = z_1 + z_2
        cont_val = (z_1 / tot) * (x_1 / z_1 - math.sqrt(-math.log(delta) / (2 * z_1)))
        not_cont_val = (z_2 / tot) * (x_2 / z_2 - math.sqrt(-math.log(delta) / (2 * z_2))) if z_2 > 0 else 0
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

    def get_combined_bound(self, rewards_counters):
        x = 0
        z = 0
        delta = 0.5
        for feat in classes_config.values():
            z += rewards_counters[(feat[0], feat[1])]['n_purchases']
            x += rewards_counters[(feat[0], feat[1])]['total_reward']

        combined = (x / z - math.sqrt(-math.log(delta) / (2 * z)))
        return combined
