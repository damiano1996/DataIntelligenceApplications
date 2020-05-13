from project.part_4.Env_4 import Env_4


class Env_5(Env_4):

    def __init__(self, initial_date, n_days, users_per_day, mutli_class_handler, n_arms):
        super().__init__(initial_date, n_days, users_per_day, mutli_class_handler, n_arms)

    def reset(self):
        """
        :return: (new_week, current date, done)
        """
        # This isn't a new week -> False
        return False, super(Env_5, self).reset()

    def round(self, pulled_arm, user):
        """
            This method computes a round and checks if another week is finished.
        :param pulled_arm: arm to pull
        :param user: User object
        :return: (new_week, reward, current date, done)
        """
        new_week = False
        if self.current_date.weekday() == 7:
            new_week = True

        # below the code is equal to the code in Env_4.round()
        reward, opt_revenue = self.one_user_round(pulled_arm, user)

        current_date = self.get_current_date()
        done = False

        self.count_rounds_today += 1
        if self.count_rounds_today == self.round_per_day:
            self.count_rounds_today = 0
            current_date, done = self.step()

        return new_week, reward, current_date, done, opt_revenue
