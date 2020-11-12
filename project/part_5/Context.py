import copy


class Context:

    def __init__(self, features, mab_algorithm=None, mab_args=None):
        """
        This is the function called when we generate new contexts each week, it receives the feature set
        corresponding to the context and the parameters for the MAB algorithm of this context
        """
        # general MAB algorithm to perform multiple tests, with different configurations
        self.MAB = mab_algorithm  # Multi Armed Bandit algorithm to use
        self.MAB_args = mab_args

        if mab_algorithm is not None:
            self.learner = self.MAB(*self.MAB_args)

        self.features = features

        self.last_pulled = None

    def pull_arm(self, keep_daily_price=False, new_day=True):
        """
        pulls the arm corresponding to the curve of the context, if the price is chosen once for the entire day,
        it pulls the previously used arm
        """
        if keep_daily_price:
            if new_day or self.last_pulled is None:
                self.last_pulled = self.learner.pull_arm_revenue()
            return self.last_pulled
        else:
            return self.learner.pull_arm_revenue()

    def is_user_belonging(self, user):
        """
        Return true if the user belongs to this context by looking at common features, false otherwise
        :param user: User object
        :return: if the user belongs to this context
        """
        if user.features in self.features:
            return True
        return False

    def initialize_learner(self, mab):
        self.learner = copy.deepcopy(mab)
