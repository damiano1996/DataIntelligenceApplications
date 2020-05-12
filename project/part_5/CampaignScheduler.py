from project.dia_pckg.Environment import Environment
from project.part_5.ContextGenerator import ContextGenerator


class CampaignScheduler(Environment):

    def __init__(self, initial_date, n_days, MAB_algorithm, users_per_day, n_arms):
        super().__init__(initial_date, n_days)

        self.MAB = MAB_algorithm  # Multi Armed Bandit algorithm to use
        self.users_per_day = users_per_day
        self.n_arms = n_arms

        self.users = []  # to list the users
        self.weeks = []  # to store the Week objects

        self.cntxt_generator = ContextGenerator()

    def weekend_update(self):
        """
            At the end of the week,
            we'll generate the new contexts and
            we'll associate to each new context a MAB (where possible, re-using the prior of the last week).
        :return:
        """
        pass

    def learner_generator(self, contexts):
        """
            Knowing the new contexts, we will generate the associate MAB.
        :param contexts:
        :return:
        """
        pass

    def context_generator(self):
        """
            Here we'll call the ContextGenerator object to get the new contexts
        :return:
        """
        # new_contexts = self.cntxt_generator.get_weekly_contexts(features_space, self.users)
        # self.weekly_contexts.append(new_contexts)

    def round_in_week(self, user):
        """
            During the week, we know the generated contexts and we have one MAB for each context.
            In this function, we observe the features of the incoming user, to get the corresponding generated context
            and from the context, to get the associated MAB.
            From the MAB, we will propose a price to the user and we will observe the reward.
        :param user: User object
        :return: reward
        """
