import numpy as np

from project.part_5.ContextGenerator import ContextGenerator


class CampaignScheduler():

    def __init__(self, multi_class_handler, mab_algorithm, *mab_args):
        self.mch = multi_class_handler
        # general MAB algorithm to perform multiple tests, with different configurations
        self.MAB = mab_algorithm  # Multi Armed Bandit algorithm to use
        self.MAB_args = mab_args

        self.users_counter = {'elegant': 0, 'sports': 0, 'casual': 0}  # dictionary to count incoming users
        self.rewards_counter = {'elegant': 0, 'sports': 0, 'casual': 0}
        self.contexts = {}

        self.context_generator = ContextGenerator(multi_class_handler, mab_algorithm, mab_args)
        self.collected_rewards = np.array([])

    def reset(self):
        self.users_counter = {'elegant': 0, 'sports': 0, 'casual': 0}  # dictionary to count incoming users
        self.rewards_counter = {'elegant': 0, 'sports': 0, 'casual': 0}
        self.contexts = {}

        self.collected_rewards = np.array([])

    def context_update(self):
        """
            At the end of the week, I take the new contexts from ContextGenerator 
        :return:
        """
        try:
            self.contexts = self.context_generator.get_weekly_contexts(users_counter=self.users_counter,
                                                                       contexts=self.contexts,
                                                                       sales=self.rewards_counter)
        except:
            print('Errore fatale')

    def add_new_user(self, user):
        """
        :return:
        """
        class_name_user = user.class_name
        self.users_counter[class_name_user] += 1

    def add_sale(self, reward, user):
        class_name_user = user.class_name
        self.rewards_counter[class_name_user] += reward

    def pull_arm_from_user(self, user):
        """
        Return the pulled arm from the context in which the user belongs
        :param user: User object
        :return: pulled arm
        """
        self.add_new_user(user)
        for context_name, context_obj in self.contexts.items():
            if context_obj.is_user_belonging(user):
                return context_obj.learner.pull_arm_revenue()

    def update(self, user, pulled_arm, reward):
        """
        Update the context in which the user belongs, also update the collected rewards
        :param user: User object
        :param user: pulled arm
        :param user: reward associated to the pulled arm
        :return:
        """
        for context_name, context_obj in self.contexts.items():
            if (context_obj.is_user_belonging(user)):
                context_obj.learner.update(pulled_arm, reward)
                real_reward = context_obj.learner.get_real_reward(pulled_arm, reward)
                self.collected_rewards = np.append(self.collected_rewards, real_reward)
