import numpy as np

from project.dia_pckg.Environment import Environment


class Env_4(Environment):

    def __init__(self, initial_date, n_days, users_per_day,
                 class_1, class_2, class_3, n_arms):
        """
        :param initial_date: when the campaign begins
        :param n_days: number of days of the campaign
        :param users_per_day: number of users per day
        :param class_1: Class object
        :param class_2: Class object
        :param class_3: Class object
        :param n_arms: number of arms of the Thomson Sampling algorithm
        """
        super().__init__(initial_date, n_days)

        self.round_per_day = users_per_day
        self.count_rounds_today = 0

        self.classes = [class_1, class_2, class_3]
        self.aggregate_demand_curve = self.get_aggregate_curve()

        self.n_arms = n_arms
        # In the exercises of the prof there are fixed probabilities, but in our case
        # we need to fix the position of the arms at a specific distance -> our candidates
        self.arm_distance = int(self.aggregate_demand_curve[1].shape[0] / self.n_arms)

    def user_step(self, pulled_arm, user):
        """
            This method performs a round considering the number of steps per day
            Only after n rounds it perform a step in the implemented class
        :param pulled_arm: arm to pull
        :param user: User object
        :return: (reward, current date, done) done is a boolean -> True if the "game" is finished
        """
        reward = self.round(pulled_arm, user)

        current_date = self.get_current_date()
        done = False

        self.count_rounds_today += 1
        if self.count_rounds_today == self.round_per_day:
            self.count_rounds_today = 0
            current_date, done = self.step()

        return (reward, current_date, done)

    def reset(self):
        """
            to reset the environment
        :return: None
        """
        self.count_rounds_today = 0
        return super(Env_4, self).reset()

    def round(self, pulled_arm, user):
        """
            This method performs a round taking the probability from the user's class
        :param pulled_arm: arm to pull
        :param user: User object
        :return: reward
        """
        # class of the user
        conv_rate = None
        for class_ in self.classes:
            if user.class_name == class_.name:
                conv_rate = class_.conv_rates[0]  # taking the first because no abrupt phases

        # taking the index of the pulled arm
        probability = conv_rate[1][pulled_arm * self.arm_distance]

        reward = np.random.binomial(1, probability)
        return reward

    def get_aggregate_curve(self):
        """
        :return: the aggregate curve
        """
        prices = self.classes[0].conv_rates[0][0]

        stack = np.stack(
            [self.classes[0].conv_rates[0][1],
             self.classes[1].conv_rates[0][1],
             self.classes[2].conv_rates[0][1]], axis=1
        )
        aggr_proba = np.mean(stack, axis=-1)
        return (prices, aggr_proba)

    def get_optimals(self):
        """
        :return: (aggregate_optimal, class_1_optimal, class_2_optimal, class_3_optimal)
        """
        return (
            self.get_optimal_price(self.aggregate_demand_curve),
            self.get_optimal_price(self.classes[0].conv_rates[0]),
            self.get_optimal_price(self.classes[1].conv_rates[0]),
            self.get_optimal_price(self.classes[2].conv_rates[0]),
        )

    # [Disclaimer!]
    # I don't know where is the best allocation for this function.
    # I will leave it here for the moment.
    def get_optimal_price(self, conv_rate):
        """
            This method computes the max area
        :param conv_rate: (price, probability)
        :return:
        """
        areas = conv_rate[0] * conv_rate[1]
        idx = np.argmax(areas)
        return (conv_rate[0][idx], conv_rate[1][idx])
