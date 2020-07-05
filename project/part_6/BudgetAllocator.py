from project.part_2.Optimizer import fit_table
from project.part_6.TemporaryConfig import max_bid

import numpy as np

class BudgetAllocator():

    def __init__(self, n_arms_advertising, n_subcampaigns):
        """
        :param n_arms_advertising
        :param n_subcampaigns
        """
        self.n_arms_advertising = n_arms_advertising
        self.bids = np.linspace(0, max_bid, n_arms_advertising)
        self.n_subcampaigns = n_subcampaigns

        self.day_zero_initialization()

    #To optimize and change when budget constraint is inserted
    def day_zero_initialization(self):
        self.best_allocation = []
        for _ in range (self.n_subcampaigns):
            self.best_allocation.append(int(self.n_arms_advertising / self.n_subcampaigns))
        
    #Not best update, keeps in consideration only advertising problem
    def update_v1(self, learners):
        """
            Here we update the best budget allocation given only advertising problem (maximize number of clicks)
        :return:
        """
        table_all_Subs = np.ndarray(shape=(0, len(self.bids)), dtype=float)
        for l in learners:
            table_all_Subs = np.append(table_all_Subs, np.atleast_2d(l.means.T), 0)

        self.best_allocation = fit_table(table_all_Subs)[0]

    def get_best_allocations(self):
        """
            Returns the best budget allocations for the subcampaigns
        :return:
        """
        return self.best_allocation
