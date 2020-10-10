import numpy as np

from project.dia_pckg.Config import classes_config
from project.part_5.ContextGenerator import ContextGenerator


class CampaignScheduler(ContextGenerator):

    def __init__(self, multi_class_handler, mab_algorithm, *mab_args):
        super().__init__(multi_class_handler, mab_algorithm, mab_args)

        # total reward: cumulative price
        # n_purchases: number of times that users bought with the corresponding feature
        # n_users: number of times users arrived with the corresponding feature
        self.counters = {(feat[0], feat[1]): {'total_reward': 0, 'n_purchases': 0, 'n_users': 0, 'rewards': []} for feat
                         in
                         list(classes_config.values())}
        self.week_contexts = {}
        self.collected_rewards = np.array([])

    def reset(self):
        """
            Resetting variables
        :return: None
        """
        self.counters = {(feat[0], feat[1]): {'total_reward': 0, 'n_purchases': 0, 'n_users': 0, 'rewards': []} for feat
                         in
                         list(classes_config.values())}
        self.week_contexts = {}
        self.collected_rewards = np.array([])

    def context_update(self):
        """
            Updating the context
        :return: None
        """
        self.week_contexts = self.get_weekly_contexts(last_contexts=self.week_contexts,
                                                      rewards_counters=self.counters)

    def pull_arm_from_user(self, user, keep_daily_price, new_day):
        """
            Return the pulled arm from the context in which the user belongs
        :param user: User object
        :return: pulled arm
        """
        for context_name, context_obj in self.week_contexts.items():
            if context_obj.is_user_belonging(user):
                return context_obj.pull_arm(keep_daily_price, new_day)

    def update_rewards_counters(self, reward, user):
        """
            Updating the reward counter
        :param reward:
        :param user:
        :return:
        """
        user_features = user.features
        self.counters[(user_features[0], user_features[1])]['total_reward'] += reward
        self.counters[(user_features[0], user_features[1])]['n_purchases'] += 1 if reward > 0 else 0
        self.counters[(user_features[0], user_features[1])]['n_users'] += 1
        self.counters[(user_features[0], user_features[1])]['rewards'].append(reward)

    def update(self, user, pulled_arm, reward):
        """
            Update the context in which the user belongs, also update the collected rewards
        :param user: User object
        :param pulled_arm: pulled arm
        :param reward: reward associated to the pulled arm
        :return: None
        """

        for context_name, context_obj in self.week_contexts.items():
            if context_obj.is_user_belonging(user):
                context_obj.learner.update(pulled_arm, reward)
                real_reward = context_obj.learner.get_real_reward(pulled_arm, reward)
                self.update_rewards_counters(real_reward, user)
                self.collected_rewards = np.append(self.collected_rewards, real_reward)
