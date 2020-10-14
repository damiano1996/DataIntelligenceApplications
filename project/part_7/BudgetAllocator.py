import numpy as np

from project.part_2.Optimizer import fit_table
from project.part_2.Utils import get_idx_arm_from_allocation
from project.part_7.MultiSubcampaignHandler import MultiSubcampaignHandler
from project.part_2.GPTS_Learner import GPTS_Learner

class BudgetAllocator:
    """
    Definito un price da provare vogliamo calcolare lállocazione migliore del budget
    Dura tutta la durata dell'esperimento
    """

    def __init__(self,
                 arm_pricing,
                 campaignHandler,
                 n_arms_advertising,
                 n_subcampaigns
                 ):

        self.arm_pricing = arm_pricing
        self.ch = campaignHandler
        self.n_arms_advertising = n_arms_advertising
        self.n_subcampaigns = n_subcampaigns

        self.best_allocation = self.day_zero_initialization()
        self.predicted_purchases = 0

        #self.optimal_total_revenue = self.get_optimal_total_revenue()

    def day_zero_initialization(self):
        """
            Initialize allocations for day zero
        """
        avg = 1 / self.n_subcampaigns
        allocation = [avg, avg, avg]
        return allocation

    def get_best_allocation(self):
        return self.best_allocation, self.predicted_purchases

    def compute_best_allocation(self):
        """
        Chiamato ogni giorno per calcolare il budget per ogni subs
        e aggiorna i learners
        """

        table_all_subs = np.ndarray(shape=(0, len(self.ch.subcampaigns_handlers[0].advertising.env.bids)),
                                    dtype=np.float32)

        for subcampaign_handler in self.ch.subcampaigns_handlers:
            learner_clicks = subcampaign_handler.get_updated_parameters()


            v = subcampaign_handler.get_price_convr(self.arm_pricing)

            pp = np.multiply(learner_clicks, v)

            table_all_subs = np.append(table_all_subs, np.atleast_2d(pp.T), 0)

        self.best_allocation, self.predicted_purchases = fit_table(table_all_subs)

        return np.asarray(self.best_allocation), self.predicted_purchases



    def update_handlers(self):
        self.ch.update_all_subcampaign_handlers(self.best_allocation)
        #self.regret.append(self.optimal_total_revenue - self.ch.daily_revenue)

