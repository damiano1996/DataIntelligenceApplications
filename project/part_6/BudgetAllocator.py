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

        self.exploarion_iteration = 0
        self.is_exploiting = False

        self.day_zero_initialization()

    #TODO optimize, now gives [3,3,3]
    def day_zero_initialization(self):
        """
            Inizialize allocations for day zero
        """
        self.best_allocation = []
        for _ in range (self.n_subcampaigns):
            self.best_allocation.append(int(self.n_arms_advertising / self.n_subcampaigns))
        
    def update_v1(self, learners):
        """
            Here we update the best budget allocation given only advertising problem (maximize number of clicks)
        :return:
        """
        #Exploration phase 
        if (not self.isExploiting(learners)):
            first = self.exploarion_iteration % 3
            pulled = [0, 0, 0]

            pulled[first] = learners[first].pull_arm_v2()
            pulled[(first + 1) % 3] = learners[(first + 1) % 3].pull_arm_v3(self.n_arms_advertising - pulled[first])
            pulled[(first + 2) % 3] = learners[(first + 2) % 3].pull_arm_v3(self.n_arms_advertising - pulled[first] - pulled[(first + 1) % 3] - 1) 

            self.exploarion_iteration += 1
            self.best_allocation = pulled 

        #Exploitation phase 
        #TODO knapsack problem solver to keep in cosideration both pricing and advertising
        else:
            table_all_Subs = np.ndarray(shape=(0, len(self.bids)), dtype=float)
            for l in learners:
                table_all_Subs = np.append(table_all_Subs, np.atleast_2d(l.means.T), 0)

            self.best_allocation = fit_table(table_all_Subs)[0]

    
    #TODO search for the best switch phase parameters, possibly not those constants
    def isExploiting (self, learners):
        """
            #Decide whether to explore or exploit.
        """
        #print (learners[0].get_sigma_sum(), learners[1].get_sigma_sum(), learners[2].get_sigma_sum())
        #If the variances on the GP curves is not enough confident, keep explore. Otherwise exploit.
        if (self.is_exploiting == False):
            if (learners[0].get_sigma_sum() < 100 and learners[1].get_sigma_sum() < 100 and learners[2].get_sigma_sum() < 100 and self.exploarion_iteration > 0):
                self.is_exploiting = True
                print ('exploit')
        #If the variances on the gp curves raise too much, turn back to explore. Otherwise exploit.
        else:
            if (learners[0].get_sigma_sum() > 110 and learners[1].get_sigma_sum() > 110 and learners[2].get_sigma_sum() > 110):
                self.is_exploiting = False

        return self.is_exploiting



    def get_best_allocations(self):
        """
            Returns the best budget allocations for the subcampaigns
        :return:
        """
        return self.best_allocation
