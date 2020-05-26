import numpy as np

from project.dia_pckg.Config import classes_config
from project.part_5.ContextGenerator import ContextGenerator


class CampaignScheduler(ContextGenerator):

    def __init__(self, multi_class_handler, mab_algorithm, *mab_args):
        super().__init__(multi_class_handler, mab_algorithm, mab_args)

        self.users_counters = self.rewards_counters = {class_name: 0 for class_name in classes_config.keys()}
        self.week_contexts = {}
        self.collected_rewards = np.array([])

    def reset(self):
        """
            Resetting variables
        :return: None
        """
        self.users_counters = {class_name: 0 for class_name in classes_config.keys()}
        self.rewards_counters = {class_name: 0 for class_name in classes_config.keys()}
        self.week_contexts = {}
        self.collected_rewards = np.array([])

    def context_update(self):
        """
            Updating the context
        :return: None
        """
        self.week_contexts = self.get_weekly_contexts(last_contexts=self.week_contexts,
                                                      users_counters=self.users_counters,
                                                      rewards_counters=self.rewards_counters)

    def pull_arm_from_user(self, user):
        """
            Return the pulled arm from the context in which the user belongs
        :param user: User object
        :return: pulled arm
        """
        for context_name, context_obj in self.week_contexts.items():
            if context_obj.is_user_belonging(user):
                return context_obj.learner.pull_arm_revenue()

    def update_users_counters(self, user):
        """
            Updating the user counter
        :param user: User object
        :return: None
        """
        class_name_user = user.class_name
        self.users_counters[class_name_user] += 1

    def update_rewards_counters(self, reward, user):
        """
            Updating the reward counter
        :param reward:
        :param user:
        :return:
        """
        class_name_user = user.class_name
        self.rewards_counters[class_name_user] += reward

    def update(self, user, pulled_arm, reward):
        """
            Update the context in which the user belongs, also update the collected rewards
        :param user: User object
        :param user: pulled arm
        :param user: reward associated to the pulled arm
        :return: None
        """
        self.update_users_counters(user)
        # self.update_rewards_counters(reward, user)

        for context_name, context_obj in self.week_contexts.items():
            if context_obj.is_user_belonging(user):
                context_obj.learner.update(pulled_arm, reward)
                real_reward = context_obj.learner.get_real_reward(pulled_arm, reward)
                self.update_rewards_counters(real_reward, user)
                self.collected_rewards = np.append(self.collected_rewards, real_reward)
