import numpy as np

from project.dia_pckg.Config import max_bid
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_2.Utils import get_idx_arm_from_allocation
from project.part_6.SubCampaignHandler import SubCampaignHandler


class MultiSubCampaignHandler:

    def __init__(self,
                 multi_class_handler,
                 n_arms_pricing,
                 n_arms_advertising):
        """
        :param multi_class_handler:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """
        self.mch = multi_class_handler

        self.n_arms_pricing = n_arms_pricing
        self.n_arms_advertising = n_arms_advertising

        self.bidding_environment = BiddingEnvironment(np.linspace(0, max_bid, self.n_arms_advertising))

        self.subcampaigns_handlers = []
        for i, class_ in enumerate(self.mch.classes):
            subcampaign_handler = SubCampaignHandler(class_name=class_.name,
                                                     multi_class_handler=self.mch,
                                                     subcampaign_idx=i,
                                                     n_arms_pricing=self.n_arms_pricing,
                                                     n_arms_advertising=self.n_arms_advertising,
                                                     bidding_environment=self.bidding_environment)
            self.subcampaigns_handlers.append(subcampaign_handler)

        self.regret = []
        self.daily_revenue = 0
        self.total_revenue = 0

    def update_all_subcampaign_handlers(self, allocations):
        """
            Execute one day round:
            Update advertising and pricing model
            Update budget allocation
        :return:
        """

        # Learn about data of the current day, given the budget allocations
        learners = []
        total_daily_regret = 0
        self.daily_revenue = 0
        for subcampaign_handler, allocation in zip(self.subcampaigns_handlers, allocations):
            # conversion from percentage to arm index
            pulled_arm = get_idx_arm_from_allocation(allocation=allocation,
                                                     bids=subcampaign_handler.advertising.env.bids)

            subcampaign_daily_regret, subcampaign_daily_revenue = subcampaign_handler.daily_update(pulled_arm)
            learner = subcampaign_handler.get_updated_parameters()
            learners.append(learner)
            total_daily_regret += subcampaign_daily_regret
            self.daily_revenue += subcampaign_daily_revenue

        # saving revenue and regret
        self.total_revenue += self.daily_revenue
        self.regret.append(total_daily_regret)

        return learners
