from project.part_4.Env_4 import Env_4


class Env_5(Env_4):

    def __init__(self, initial_date, n_days, users_per_day, mutli_class_handler, n_arms):
        super().__init__(initial_date, n_days, users_per_day, mutli_class_handler, n_arms)

    def reset(self):
        """
        :return: (new_week, current date, done)
        """
        # This is a new week since it starts the experiment
        return True, super(Env_5, self).reset()

    def round(self, pulled_arm, user):
        """
            This method computes a round and checks if another week is finished.
        :param pulled_arm: arm to pull
        :param user: User object
        :return: (new_week, reward, current date, done)
        """
        new_week = False
        if self.get_current_date().weekday() == 6:
            new_week = True

        return new_week, super(Env_5, self).round(pulled_arm, user)
