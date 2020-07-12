import numpy as np

from project.part_2.Optimizer import fit_table
from project.part_6.MultiSubCampaignHandler import MultiSubCampaignHandler


class BudgetAllocator:

    def __init__(self,
                 multi_class_handler,
                 n_arms_pricing,
                 n_arms_advertising):
        """
        :param multi_class_handler:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """

        self.msh = MultiSubCampaignHandler(multi_class_handler=multi_class_handler,
                                           n_arms_pricing=n_arms_pricing,
                                           n_arms_advertising=n_arms_advertising)

        self.n_arms_pricing = self.msh.subcampaigns_handlers[0].pricing.n_arms
        self.n_arms_advertising = self.msh.subcampaigns_handlers[0].advertising.n_arms
        self.n_subcampaigns = len(self.msh.subcampaigns_handlers)

        self.exploration_iteration = 0
        self.is_exploiting = False

        self.day_zero_initialization()

    # TODO optimize, now gives [3, 3, 3]
    def day_zero_initialization(self):
        """
            Inizialize allocations for day zero
        """
        self.best_allocation = []
        for _ in range(self.n_subcampaigns):
            self.best_allocation.append(int(self.n_arms_advertising / self.n_subcampaigns))

    def update(self):
        """
            Here we update the best budget allocation given only advertising problem (maximize number of clicks)
        :return:
        """
        learners = self.msh.update_all_subcampaign_handlers(self.get_best_allocations())

        # Exploration phase
        if not self.is_exploiting_phase(learners):
            first = self.exploration_iteration % 3
            pulled = [0, 0, 0]

            pulled[first] = learners[first].pull_arm_v2()
            pulled[(first + 1) % 3] = learners[(first + 1) % 3].pull_arm_v3(self.n_arms_advertising - pulled[first])
            pulled[(first + 2) % 3] = learners[(first + 2) % 3].pull_arm_v3(
                self.n_arms_advertising - pulled[first] - pulled[(first + 1) % 3] - 1)

            self.exploration_iteration += 1
            self.best_allocation = pulled

            # Exploitation phase
        # TODO knapsack problem solver to keep in consideration both pricing and advertising
        else:
            table_all_subs = np.ndarray(shape=(0, len(self.msh.subcampaigns_handlers[0].advertising.bids)), dtype=float)
            for subcampaign_handler in self.msh.subcampaigns_handlers:
                learner_clicks = subcampaign_handler.get_updated_parameters().means
                revenue = subcampaign_handler.daily_revenue
                n_clicks = subcampaign_handler.advertising.daily_clicks
                v = revenue / n_clicks

                revenue_clicks = learner_clicks * v

                table_all_subs = np.append(table_all_subs, np.atleast_2d(revenue_clicks.T), 0)

            self.best_allocation = fit_table(table_all_subs)[0]
            print('BEST ALLOCATION:', self.best_allocation)

    # TODO search for the best switch phase parameters, possibly not those constants
    def is_exploiting_phase(self, learners, sigma_exploiting=135, sigma_exploring=140):
        """
            Decide whether to explore or exploit.
        """
        print(learners[0].get_sigma_sum(), learners[1].get_sigma_sum(), learners[2].get_sigma_sum())
        # If the variances on the GP curves is not enough confident, keep explore. Otherwise exploit.
        if not self.is_exploiting:
            if (
                    learners[0].get_sigma_sum() < sigma_exploiting and
                    learners[1].get_sigma_sum() < sigma_exploiting and
                    learners[2].get_sigma_sum() < sigma_exploiting and
                    self.exploration_iteration > 0
            ):
                self.is_exploiting = True
                print('--> EXPLOITING!')
        # If the variances on the gp curves raise too much, turn back to explore. Otherwise exploit.
        else:
            if (
                    learners[0].get_sigma_sum() > sigma_exploring and
                    learners[1].get_sigma_sum() > sigma_exploring and
                    learners[2].get_sigma_sum() > sigma_exploring
            ):
                self.is_exploiting = False
                print('--> EXPLORING!')

        return self.is_exploiting

    def get_best_allocations(self):
        """
            Returns the best budget allocations for the subcampaigns
        :return:
        """
        return self.best_allocation
