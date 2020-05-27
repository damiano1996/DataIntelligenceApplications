import numpy as np

from project.dia_pckg.Config import features_space
from project.part_5.Context import Context


class MyContextGenerator():

    def __init__(self, multi_class_handler, mab_algorithm, mab_args):
        self.mch = multi_class_handler
        self.mab_algorithm = mab_algorithm
        self.mab_args = mab_args

    def get_weekly_contexts(self, last_contexts, rewards_counters):
        features_contexts = self.get_features_contexts(rewards_counters, delta=0.5)
        print(len(features_contexts))
        new_contexts = {}
        for i, features_context in enumerate(features_contexts):
            context = Context(features=features_context,
                              mab_algorithm=self.mab_algorithm,
                              mab_args=self.mab_args)
            new_contexts[f'context_{i + 1}'] = context

        new_contexts = self.initialize_learners(last_contexts, new_contexts)
        return new_contexts

    def initialize_learners(self, last_contexts, new_contexts):
        """
        :param last_contexts:
        :param new_contexts:
        :return:
        """
        for new_context in new_contexts.values():
            for last_context in last_contexts.values():
                if new_context.features[0] in last_context.features:
                    prior = last_context.learner.beta_parameters
                    rewards_per_arm = last_context.learner.rewards_per_arm
                    new_context.learner.initialize_learner(prior, rewards_per_arm)

        return new_contexts

    def get_features_contexts(self, rewards_counters, delta=0.1):
        """
        :param rewards_counters: {'<30': counter, '>30: counter, 'student': counter, 'worker': counter}
        :return:
        """
        first_feature = list(features_space.keys())[0]
        if self.is_split(first_feature, rewards_counters, father_value=None, delta=delta):
            print('First split on ', first_feature)
            second_feature = list(features_space.keys())[1]

            print('LEFT BRANCH')
            left_branch = self.is_split(second_feature, rewards_counters,
                                        father_value=features_space[first_feature][0],
                                        delta=delta)
            print('RIGHT BRANCH')
            right_branch = self.is_split(second_feature, rewards_counters,
                                         father_value=features_space[first_feature][1],
                                         delta=delta)
            # we can have 4 sub-cases
            # - both branches split
            # - only left branch splits
            # - only right branch splits
            # - no split
            if left_branch and right_branch:
                print('Second split on all combinations')
                return [[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]]  # 4 contexts
            elif left_branch:
                print('Second split on left branch only')
                return [[[0, 0]], [[1, 0]], [[0, 1], [1, 1]]]  # 3 contexts
            elif right_branch:
                print('Second split on right branch only')
                return [[[0, 0], [1, 0]], [[0, 1]], [[1, 1]]]  # 3 contexts
            else:
                print('No second split')
                return [[[0, 0], [1, 0]], [[0, 1], [1, 1]]]  # 2 contexts

        else:
            print('No split')
            return [[[0, 0], [0, 1], [1, 0], [1, 1]]]  # 1 context

    def is_split(self, feature_name, rewards_counters, father_value=None, delta=0.5):
        """
        :param feature_name: 'age' or 'profession'
        :param rewards_counters:
        :param father_value: '<30' or '>30' (if feature_name = 'profession') or viceversa.
                                It can be None if there isn't a father.
        :return:
        """
        # to consider also the reward of the father
        father_reward = rewards_counters[father_value]['total_reward'] if father_value != None else 0
        father_purchases = rewards_counters[father_value]['n_purchases'] if father_value != None else 0
        father_users = rewards_counters[father_value]['n_users'] if father_value != None else 0

        # to get the name of the branches
        branch_1, branch_2 = features_space[feature_name]
        print('branches:', branch_1, branch_2)

        # average expected reward for branch_1 and branch_2:
        x_1 = (rewards_counters[branch_1]['total_reward'] + father_reward) / (
                rewards_counters[branch_1]['n_purchases'] + father_purchases + 1e-20)
        x_2 = (rewards_counters[branch_2]['total_reward'] + father_reward) / (
                rewards_counters[branch_2]['n_purchases'] + father_purchases + 1e-20)
        print('x_1, x_2', x_1, x_2)

        # probability that contexts occurs
        p_c1 = (rewards_counters[branch_1]['n_purchases'] + father_purchases) / (
                    rewards_counters[branch_1]['n_users'] + father_users + 1e-20)
        p_c2 = (rewards_counters[branch_2]['n_purchases'] + father_purchases) / (
                    rewards_counters[branch_2]['n_users'] + father_users + 1e-20)
        print('p_c1, p_c2', p_c1, p_c2)

        # lower bound of the un-splitted node -> node c0
        x_0 = (rewards_counters[branch_1]['total_reward'] + rewards_counters[branch_2][
            'total_reward'] + father_reward) / (rewards_counters[branch_1]['n_purchases'] + rewards_counters[branch_2][
            'n_purchases'] + father_purchases + 1e-20)

        return self.split_condition(mu_c0=x_0, p_c1=p_c1, mu_c1=x_1, p_c2=p_c2, mu_c2=x_2)

    def split_condition(self, mu_c0, p_c1, mu_c1, p_c2, mu_c2):
        print('Split condition:', p_c1 * mu_c1 + p_c2 * mu_c2, mu_c0)
        return p_c1 * mu_c1 + p_c2 * mu_c2 >= mu_c0

    def get_lower_bound(self, x, Z, delta=0.5):
        return x - np.sqrt(- np.log(delta) / np.abs(Z))
