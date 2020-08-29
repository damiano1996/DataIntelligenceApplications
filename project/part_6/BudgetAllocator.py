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

        self.enable_pricing = enable_pricing

        self.n_arms_pricing = self.msh.subcampaigns_handlers[0].pricing.n_arms
        self.n_arms_advertising = self.msh.subcampaigns_handlers[0].advertising.n_arms
        self.n_subcampaigns = len(self.msh.subcampaigns_handlers)

        self.best_allocation = self.day_zero_initialization()

        self.regret = []

    def day_zero_initialization(self):
        """
            Initialize allocations for day zero
        """
        avg = 1 / self.n_subcampaigns
        return [avg, avg, avg]

    def update(self, opt=False):

        self.msh.update_all_subcampaign_handlers(self.best_allocation)

        table_all_subs = np.ndarray(
            shape=(0, len(self.msh.subcampaigns_handlers[0].advertising.bids)), dtype=np.float32)

        for subcampaign_handler in self.msh.subcampaigns_handlers:

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

        self.allocation = fit_table(table_all_subs)[0]

        if sum(self.allocation) > 1:
            raise Exception("Allocation unfeasible")
