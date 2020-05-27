import numpy as np

from project.dia_pckg.Config import features_space
from project.part_5.ContextGenerator_V2 import MyContextGenerator


class CampaignScheduler(MyContextGenerator):

    def __init__(self, multi_class_handler, mab_algorithm, *mab_args):
        super().__init__(multi_class_handler, mab_algorithm, mab_args)

        # total reward: cumulative price
        # n_purchases: number of times that users bought with the corresponding feature
        # n_users: number of times users arrived with the corresponding feature
        self.counters = {feat: {'total_reward': 0, 'n_purchases': 0, 'n_users': 0} for feat in
                         list(features_space.values())[0] + list(features_space.values())[1]}
        self.week_contexts = {}
        self.collected_rewards = np.array([])

    def reset(self):
        """
            Resetting variables
        :return: None
        """
        self.counters = {feat: {'total_reward': 0, 'n_purchases': 0, 'n_users': 0} for feat in
                         list(features_space.values())[0] + list(features_space.values())[1]}
        self.week_contexts = {}
        self.collected_rewards = np.array([])

    def context_update(self):
        """
            Updating the context
        :return: None
        """
        self.week_contexts = self.get_weekly_contexts(last_contexts=self.week_contexts, rewards_counters=self.counters)
        print('WEEK CONTEXTS:')
        print(self.counters)
        for key, context in self.week_contexts.items():
            print(key, context.features)
        print()

    def pull_arm_from_user(self, user):
        """
            Return the pulled arm from the context in which the user belongs
        :param user: User object
        :return: pulled arm
        """
        for context_name, context_obj in self.week_contexts.items():
            if context_obj.is_user_belonging(user):
                return context_obj.learner.pull_arm_revenue()

    def update_rewards_counters(self, reward, user):
        """
            Updating the reward counter
        :param reward:
        :param user:
        :return:
        """
        user_features = user.get_features_meaning()
        for feat in user_features:
            self.counters[feat]['total_reward'] += reward
            self.counters[feat]['n_purchases'] += 1 if reward > 0 else 0
            self.counters[feat]['n_users'] += 1

    def update(self, user, pulled_arm, reward):
        """
            Update the context in which the user belongs, also update the collected rewards
        :param user: User object
        :param user: pulled arm
        :param user: reward associated to the pulled arm
        :return: None
        """

        for context_name, context_obj in self.week_contexts.items():
            if context_obj.is_user_belonging(user):
                context_obj.learner.update(pulled_arm, reward)
                real_reward = context_obj.learner.get_real_reward(pulled_arm, reward)
                self.update_rewards_counters(real_reward, user)
                self.collected_rewards = np.append(self.collected_rewards, real_reward)
