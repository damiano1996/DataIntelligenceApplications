import numpy as np

from project.part_2.Optimizer import fit_table
from project.part_2.Utils import get_idx_arm_from_allocation


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
        self.predicted_clicks = 0
        self.n_arms_advertising = n_arms_advertising
        self.n_subcampaigns = n_subcampaigns

        self.best_allocation = self.day_zero_initialization()
        self.regret = []
        # self.optimal_total_revenue = self.get_optimal_total_revenue()

    def day_zero_initialization(self):
        """
            Initialize allocations for day zero
        """
        avg = 1 / self.n_subcampaigns
        allocation = [avg, avg, avg]
        return allocation

    def compute_best_allocation(self):
        """
        Chiamato ogni giorno per calcolare il budget per ogni subs
        e aggiorna i learners
        """

        table_all_subs = np.ndarray(shape=(0, len(self.ch.subcampaigns_handlers[0].advertising.env.bids)),
                                    dtype=np.float32)

        for subcampaign_handler in self.ch.subcampaigns_handlers:
            learner_clicks = subcampaign_handler.get_updated_parameters()

            n_clicks = subcampaign_handler.total_clicks
            # v = subcampaign_handler.total_revenue / n_clicks if n_clicks != 0 else 0
            revenue_clicks = np.multiply(learner_clicks, v)

            table_all_subs = np.append(table_all_subs, np.atleast_2d(revenue_clicks.T), 0)

        self.best_allocation, self.predicted_clicks = fit_table(table_all_subs)

        return np.asarray(self.best_allocation), self.predicted_clicks * self.learner

    def update_handlers(self):
        self.ch.update_all_subcampaign_handlers(self.best_allocation)
        self.regret.append(self.optimal_total_revenue - self.ch.daily_revenue)

    def get_optimal_total_revenue(self):
        """
            This function is to compute the total optimal revenue, for the computation of the non-agnostic regret.
            Note: the so called "agnostic" regret is the regret in which the optimal revenue
                is computed using the "optimal number of clicks",
                but the "optimal number of clicks" is NOT computed knowing the pricing.
                Below, we compute the "optimal number of clicks" using the pricing!
        """
        table_all_subs = np.ndarray(shape=(0, len(self.ch.subcampaigns_handlers[0].advertising.env.bids)),
                                    dtype=np.float32)

        # for loop to initialize the table with the product between the unknown curves and the optimal revenues
        for sub_idx, subcampaign_handler in enumerate(self.ch.subcampaigns_handlers):
            unknown_clicks_curve = subcampaign_handler.advertising.env.subs[sub_idx].means['phase_0']
            revenue_clicks = np.multiply(unknown_clicks_curve, subcampaign_handler.pricing.optimal_revenue)
            table_all_subs = np.append(table_all_subs, np.atleast_2d(revenue_clicks.T), 0)

        # computation of the optimal allocation
        optimal_allocation = fit_table(table_all_subs)[0]

        # Once we have computed the optimal allocation, we can compute the total revenue
        # using the pricing
        optimal_total_revenue = 0
        for sub_idx, (allocation, subcampaign_handler) in enumerate(zip(optimal_allocation,
                                                                        self.ch.subcampaigns_handlers)):
            hypothetical_pulled_arm = get_idx_arm_from_allocation(
                allocation=allocation,
                bids=self.ch.subcampaigns_handlers[0].advertising.env.bids)
            optimal_clicks = self.ch.bidding_environment.subs[sub_idx].means['phase_0'][hypothetical_pulled_arm]
            optimal_total_revenue += optimal_clicks * subcampaign_handler.pricing.optimal_revenue

        return optimal_total_revenue
