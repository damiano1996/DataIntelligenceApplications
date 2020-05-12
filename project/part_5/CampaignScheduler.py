from project.dia_pckg.Config import features_space
from project.part_5.ContextGenerator import ContextGenerator
from project.part_5.Week import Week


class CampaignScheduler():

    def __init__(self, initial_date, n_days, users_per_day, n_arms, mab_algorithm, *mab_args):
        super().__init__(initial_date, n_days)

        self.users_per_day = users_per_day
        self.n_arms = n_arms

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
        contexts = {'context_1': []}  # this represents a general context
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
        learners = self.learner_generator()
        week = Week(week_number=self.weeks[-1].number + 1,
                    contexts=contexts,
                    learners=learners)
        self.weeks.append(week)

    def learner_generator(self, new_contexts):
        """
            Knowing the new contexts and the past weeks, we generate associated MABs.
        :param new_contexts: contexts generated for the next week
        :return:
        """
        pass

    def round_in_week(self, user):
        """
            During the week, we know the generated contexts and we have one MAB for each context.
            In this function, we observe the features of the incoming user, to get the corresponding generated context
            and from the context, to get the associated MAB.
            From the MAB, we will propose a price to the user and we will observe the reward.
        :param user: User object
        :return: reward
        """
        current_week = self.weeks[-1]
        # to get the learner associated
        learner = current_week.get_learner(user_features=user.features)
        # we need an Env_5 to update the learner
        # or we can just return the learner to another class...
