import copy

import numpy as np

from project.part_2.Optimizer import fit_table
from project.part_6.MultiSubCampaignHandler import MultiSubCampaignHandler
from project.part_6.TemporaryConfig import max_bid


class BudgetAllocator:

    def __init__(self,
                 multi_class_handler,
                 n_arms_pricing,
                 n_arms_advertising,
                 enable_pricing=True):
        """
        :param multi_class_handler:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """

        self.msh = MultiSubCampaignHandler(multi_class_handler=multi_class_handler,
                                           n_arms_pricing=n_arms_pricing,
                                           n_arms_advertising=n_arms_advertising)
        self.opt_msh = copy.deepcopy(self.msh)

        self.enable_pricing = enable_pricing

        self.n_arms_pricing = self.msh.subcampaigns_handlers[0].pricing.n_arms
        self.n_arms_advertising = self.msh.subcampaigns_handlers[0].advertising.n_arms
        self.n_subcampaigns = len(self.msh.subcampaigns_handlers)

        self.exploration_iteration = 0
        self.opt_exploration_iteration = 0
        self.is_exploiting = False
        self.opt_is_exploiting = False

        self.best_allocation = self.day_zero_initialization()
        self.opt_best_allocation = self.day_zero_initialization()  # for computation of regret

        self.regret = []

    def day_zero_initialization(self):
        """
            Initialize allocations for day zero
        """
        avg = 1 / self.n_subcampaigns
        return [avg, avg, avg]

    def update(self):
        # updating the real msh
        self.best_allocation, self.is_exploiting, self.exploration_iteration = self.update_(
            learners=self.msh.update_all_subcampaign_handlers(self.best_allocation),
            multi_subcampaign_handler=self.msh,
            is_exploiting=self.is_exploiting,
            exploration_iteration=self.exploration_iteration,
            opt=False)

        # updating the optimal
        self.opt_best_allocation, self.opt_is_exploiting, self.opt_exploration_iteration = self.update_(
            learners=self.opt_msh.update_all_subcampaign_handlers(self.opt_best_allocation, opt=True),
            multi_subcampaign_handler=self.opt_msh,
            is_exploiting=self.opt_is_exploiting,
            exploration_iteration=self.opt_exploration_iteration,
            opt=True)

        print(f'\nBest Allocation: {self.best_allocation} - Optimal Best Allocation: {self.opt_best_allocation}')
        self.regret.append(self.opt_msh.total_revenue - self.msh.total_revenue)

    # TODO: Le prime allocazioni hanno somma < 1.0
    def update_(self, learners, multi_subcampaign_handler, is_exploiting, exploration_iteration, opt=False):
        """
            Here we update the best budget allocation given only advertising problem (maximize number of clicks)
        :return:
        """

        # Exploration phase
        is_exploiting = self.is_exploiting_phase(learners, is_exploiting, exploration_iteration)
        if not is_exploiting:
            first = exploration_iteration % 3
            pulled = [0, 0, 0]

            pulled[first] = learners[first].pull_arm_v2()
            pulled[(first + 1) % 3] = learners[(first + 1) % 3].pull_arm_v3(self.n_arms_advertising - pulled[first])
            pulled[(first + 2) % 3] = learners[(first + 2) % 3].pull_arm_v4(
                self.n_arms_advertising - pulled[first] - pulled[(first + 1) % 3] - 1)

            exploration_iteration += 1
            allocation = [pull / (self.n_arms_advertising - 1) for pull in pulled]

        # Exploitation phase
        else:

            table_all_subs = np.ndarray(
                shape=(0, len(multi_subcampaign_handler.subcampaigns_handlers[0].advertising.bids)), dtype=float)

            for subcampaign_handler in multi_subcampaign_handler.subcampaigns_handlers:
                if not opt:
                    # in this case we get the learned curves from the learners
                    learner_clicks = subcampaign_handler.get_updated_parameters().means

                    n_clicks = subcampaign_handler.total_clicks
                    v = subcampaign_handler.total_revenue / n_clicks if n_clicks != 0 else 0
                    revenue_clicks = learner_clicks * v if self.enable_pricing else learner_clicks

                else:
                    # in the optimal case we already know the complete curve
                    bids = np.linspace(0, max_bid, subcampaign_handler.advertising.n_arms)
                    learner_clicks = subcampaign_handler.advertising.env.subs[subcampaign_handler.advertising.sub](bids)

                    revenue_clicks = learner_clicks * subcampaign_handler.pricing.get_optimal_revenue()

                table_all_subs = np.append(table_all_subs, np.atleast_2d(revenue_clicks.T), 0)

            allocation = fit_table(table_all_subs)[0]

        if sum(allocation) > 1:
            raise Exception("Allocation unfeasible")

        return allocation, is_exploiting, exploration_iteration

    # TODO search for the best switch phase parameters, possibly not those constants
    def is_exploiting_phase(self, learners, is_exploiting, exploration_iteration,
                            confidence_exploiting=0.95, confidence_exploring=0.93):
        """
            Decide whether to explore or exploit.
        """
        print('Confidences',
              learners[0].get_confidence_sum(),
              learners[1].get_confidence_sum(),
              learners[2].get_confidence_sum())

        # If the variances on the GP curves is not enough confident, keep explore. Otherwise exploit.
        if not is_exploiting:
            if (
                    learners[0].get_confidence_sum() > confidence_exploiting and
                    learners[1].get_confidence_sum() > confidence_exploiting and
                    learners[2].get_confidence_sum() > confidence_exploiting and
                    exploration_iteration > 0
            ):
                is_exploiting = True
                print('--> EXPLOITING!')
        # If the variances on the gp curves raise too much, turn back to explore. Otherwise exploit.
        else:
            if (
                    learners[0].get_confidence_sum() < confidence_exploring or
                    learners[1].get_confidence_sum() < confidence_exploring or
                    learners[2].get_confidence_sum() < confidence_exploring
            ):
                is_exploiting = False
                print('--> EXPLORING!')

        return is_exploiting
