import copy

import numpy as np

from project.dia_pckg.Config import features_space
from project.part_5.ContextGenerator import ContextGenerator
from project.part_5.Week import Week


class CampaignScheduler():

    def __init__(self, mab_algorithm, *mab_args):
        # general MAB algorithm to perform multiple tests, with different configurations
        self.MAB = mab_algorithm  # Multi Armed Bandit algorithm to use
        self.MAB_args = mab_args

        self.users = []  # to list the users
        self.weeks = []  # to store the Week objects
        self.initialize_weeks_list()

        self.context_generator = ContextGenerator()

    def initialize_weeks_list(self):
        """
            For the first week we cannot generate contexts,
            thus we initialize only one learner, to learn the aggregate model
        :return:
        """
        learner = self.MAB(self.MAB_args)
        contexts = {'context_1': []}  # this represents an empty context
        week = Week(week_number=0, contexts=contexts, learners=[learner])
        self.weeks.append(week)

    def weekend_update(self):
        """
            At the end of the week,
            we'll generate the new contexts and
            we'll associate to each new context a MAB (where possible, re-using the prior of the last week).
        :return:
        """
        contexts = self.context_generator.get_weekly_contexts(features_space=features_space, users=self.users)
        # here we need an algorithm being able to select from the last week the learner that we can re-use.
        learners = self.learner_generator(contexts)
        week = Week(week_number=self.weeks[-1].number + 1,
                    contexts=contexts,
                    learners=learners)
        self.weeks.append(week)

    def learner_generator(self, new_contexts):
        """
            Knowing the new contexts and the past weeks, we generate associated MABs.
        :param new_contexts: contexts generated for the next week
        :return: list of learners
        """
        # greedy implementation. We have to discuss about this algorithm
        last_week_learner = np.random.choice(self.weeks[-1].pairs)['learner']
        new_learners = [copy.deepcopy(last_week_learner) for i in range(len(list(new_contexts.keys())))]
        return new_learners

    def add_user(self, user):
        """
        :param user: User object
        :return:
        """
        self.users.append(user)

    def get_learner(self, user):
        """
            During the week, we know the generated contexts and we have one MAB for each context.
            In this function, we observe the features of the incoming user, to get the corresponding generated context
            and from the context, to get the associated MAB.
            From the MAB, we will propose a price to the user and we will observe the reward.
        :param user: User object
        :return: Learner object
        """
        current_week = self.weeks[-1]
        # to get the learner associated
        learner = current_week.get_learner(user_features=user.features)
        return learner
