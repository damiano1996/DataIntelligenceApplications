class Context_B():

    def __init__(self, features, mab_algorithm, mab_args):
        # general MAB algorithm to perform multiple tests, with different configurations
        self.MAB = mab_algorithm  # Multi Armed Bandit algorithm to use
        self.MAB_args = mab_args

        self.learner = self.MAB(*self.MAB_args)

        self.features = features

    def is_user_belonging(self, user):
        """
        Return if the user belongs to this context by looking at common features
        :param user: User object
        :return: if the user belongs to this context
        """
        if user.features in self.features:
            return True
        return False
