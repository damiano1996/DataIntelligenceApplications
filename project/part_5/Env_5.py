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
            This method performs a round considering the number of steps per day
            Only after n rounds it perform a step in the implemented class
        :param pulled_arm: arm to pull
        :return: (reward, current date, done) done is a boolean -> True if the "game" is finished
        """
        new_week = False
        done = False

        reward, opt_revenue = self.one_user_round(pulled_arm, user)
        current_date = self.get_current_date()

        self.count_rounds_today += 1
        if self.count_rounds_today == self.round_per_day:
            self.count_rounds_today = 0
            current_date, done = self.step()
            if self.get_current_date().weekday() == 6:
                new_week = True

        return new_week, reward, current_date, done, opt_revenue

        
