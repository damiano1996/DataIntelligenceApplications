import pandas as pd


class Environment():

    def __init__(self, initial_date, n_days):
        """
        :param initial_date: Initial date of the campaign in YYYYMMDD format
        :param n_days: duration of the campaign
        """
        self.dates = pd.date_range(initial_date, periods=n_days, freq='D')
        self.current_idx = 0

    def get_current_date(self):
        """
        :return: the current date
        """
        return self.dates[self.current_idx]

    def step(self):
        """
            Performing a round
            This method updates the index of the current date and return
            a boolean that is False until we haven't finish the iterations
        :return: (current date, done)
        """
        self.current_idx += 1

        if self.current_idx >= len(self.dates):
            self.current_idx = len(self.dates) - 1
            return self.get_current_date(), True  # done?

        self.current_date = self.get_current_date()
        return self.get_current_date(), False  # done?

    def reset(self):
        """
            Resetting the index of the dates
        :return: (current date, done)
        """
        self.current_idx = 0
        return self.get_current_date(), False


if __name__ == '__main__':
    # example

    env = Environment('20200101', 366)

    curr_date, done = env.reset()
    print(curr_date)
    while not done:
        curr_date, done = env.step()
        print(curr_date)
