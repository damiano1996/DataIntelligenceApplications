class CampaignScheduler():

    def __init__(self):
        self.users = []  # to list the users
        self.weekly_contexts = []  # to store the contexts generated at each week
        self.learners = []  # to store the bandits algorithms

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
