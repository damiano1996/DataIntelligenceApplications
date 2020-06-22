import math

import numpy as np
import scipy

from project.dia_pckg.Config import classes_config
from project.part_5.Context import Context


class ContextGenerator:

    def __init__(self, multi_class_handler, mab_algorithm, mab_args):

        self.mch = multi_class_handler
        self.mab_algorithm = mab_algorithm
        self.mab_args = mab_args

        self.report = ''

    def get_weekly_contexts_v2(self, last_contexts, rewards_counters, delta=0.9):
        self.report = 'Generation context '

        if len(last_contexts) == 0:
            # create aggregate context
            my_features = [feat for feat in classes_config.values()]
            new_contexts = {
                'context_1': Context(features=my_features, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)}
            self.report += 'aggregate '

        else:
            father_rewards = self.get_rewards_from_features([[[0, 0], [0, 1], [1, 1]]], rewards_counters)
            son1_rewards = self.get_rewards_from_features([[[0, 0]], [[1, 1], [0, 1]]], rewards_counters)
            son2_rewards = self.get_rewards_from_features([[[0, 0], [0, 1]], [[1, 1]]], rewards_counters)
            father_low_bound = self.get_context_low_bound(father_rewards, delta)
            son1_low_bound = self.get_context_low_bound(son1_rewards, delta)
            son2_low_bound = self.get_context_low_bound(son2_rewards, delta)

            best_son_low_bound = max([son1_low_bound, son2_low_bound])
            if best_son_low_bound > father_low_bound:
                son_rewards = self.get_rewards_from_features([[[0, 0]], [[0, 1]], [[1, 1]]], rewards_counters)
                son_low_bound = self.get_context_low_bound(son_rewards, delta)

                # split feature -> split feature
                if son_low_bound > best_son_low_bound:
                    new_context_features = [[[0, 0]], [[0, 1]], [[1, 1]]]
                    self.report += '3 contexts '

                else:
                    # split feature 1 -> no split feature 2
                    if best_son_low_bound == son1_low_bound:
                        new_context_features = [[[0, 0]], [[0, 1]], [[1, 1]]]
                        self.report += '2 contexts '
                    # split feature 2 -> no split feature 1
                    else:
                        new_context_features = [[[0, 0], [0, 1]], [[1, 1]]]
                        self.report += '2 contexts '

            # no split feature 1 or 2
            else:
                new_context_features = [[[0, 0], [0, 1], [1, 1]]]
                self.report += 'aggregate '

            new_contexts = self.initialize_contexts(last_contexts, new_context_features)

        print(self.report)
        return new_contexts

    def is_worth_split(self, father_features, son_features, reward_counters, delta=0.9):
        father_rewards = self.get_rewards_from_features(father_features, reward_counters)
        son_rewards = self.get_rewards_from_features(son_features, reward_counters)

        father_low_bound = self.get_context_low_bound(father_rewards, delta)
        son_low_bound = self.get_context_low_bound(son_rewards, delta)

        # print('father: ' + str(father_low_bound), 'son: ' + str(son_low_bound))
        # print()

        return True if son_low_bound >= father_low_bound else False

    def get_context_low_bound(self, feature_rewards, delta):
        expected_low_bound = 0
        for rewards in feature_rewards:
            reward_low_bound = self.get_gaussian_low_bound(rewards, delta)  # Lower bound on the expected reward
            prob_low_bound = self.get_bernoullian_low_bound(rewards,
                                                            delta)  # Lower bound on the probability of the context
            expected_low_bound += prob_low_bound * reward_low_bound
            # print(prob_low_bound, reward_low_bound)
        return expected_low_bound

    def get_bernoullian_low_bound(self, rewards, delta):
        rewards[rewards > 0] = 1
        x = np.mean(rewards)  # Mean value
        log_d = math.log(delta, math.e)  # Natural logarithm of delta
        n = len(rewards)  # Number of samples
        low_bound = x - (math.sqrt(-(log_d / (2 * n))))  # Hoeffding bound
        return low_bound

    def get_gaussian_low_bound(self, rewards, delta):
        x = np.mean(rewards)  # Mean value
        s_q = np.var(rewards, ddof=1)  # Corrected variance
        n = len(rewards)  # Number of samples
        t = scipy.stats.t.ppf(delta, n - 1)  # T student for ((1-d/2),n-1)
        low_bound = x - (t * math.sqrt(s_q / n))  # Lower bound for gaussian distribution with unknow standard deviation
        return low_bound

    def get_rewards_from_features(self, features, reward_counters):
        rewards = []
        for combinations in features:
            rew = np.empty((0))
            for comb in combinations:
                rew = np.append(rew, np.array(reward_counters[(comb[0], comb[1])]['rewards']))
            rewards.append(rew)
        return rewards

    def initialize_contexts(self, last_contexts, new_context_features):
        """
        :param last_contexts:
        :param new_contexts:
        :return:
        """
        new_contexts = {}

        # Non capisco perchè, ma sembra che quando cambi i contexts è meglio resettare tutto
        if (len(last_contexts) != len(new_context_features)):
            for i in range(len(new_context_features)):
                new_contexts['context_' + str(i)] = Context(features=new_context_features[i],
                                                            mab_algorithm=self.mab_algorithm,
                                                            mab_args=self.mab_args)

        # Non funziona bene se si diminuisce il numero di contexts tra una settimana e l'altra
        else:
            for i in range(len(new_context_features)):
                for comb in new_context_features[i]:
                    for context in last_contexts:
                        if (comb in last_contexts[context].features):
                            new_contexts['context_' + str(i)] = Context(features=new_context_features[i])
                            new_contexts['context_' + str(i)].initialize_learner(last_contexts[context].learner)

        return new_contexts
