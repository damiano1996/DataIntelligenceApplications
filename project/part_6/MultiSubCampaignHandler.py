import numpy as np

from project.dia_pckg.Utils import find_nearest
from project.part_6.SubCampaignHandler import SubCampaignHandler
from project.part_6.TemporaryConfig import classes_config, max_bid


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

        self.subcampaigns_handlers = []
        for class_ in self.mch.classes:
            subcampaign_handler = SubCampaignHandler(class_name=class_.name,
                                                     multi_class_handler=self.mch,
                                                     subcampaign_name=classes_config[class_.name],
                                                     n_arms_pricing=self.n_arms_pricing,
                                                     n_arms_advertising=self.n_arms_advertising)
            self.subcampaigns_handlers.append(subcampaign_handler)

        self.results = []
        self.total_revenue = 0
        self.total_regret = 0

    def update_all_subcampaign_handlers(self, allocations):
        """
            Execute one day round:
            Update advertising and pricing model
            Update budget allocation
        :return:
        """

        # Learn about data of the current day, given the budget allocations
        learners = []
        regrets = []
        for subcampaign_handler, allocation in zip(self.subcampaigns_handlers, allocations):
            # conversion from percentage to arm index
            allocation_bid = allocation * max_bid
            nearest_allocation = find_nearest(subcampaign_handler.advertising.bids, allocation_bid)
            pulled_arm = np.where(subcampaign_handler.advertising.bids == nearest_allocation)[0][0]

            daily_regret, daily_revenue = subcampaign_handler.daily_update(pulled_arm)
            learner = subcampaign_handler.get_updated_parameters()
            learners.append(learner)
            regrets.append(daily_regret)
            self.total_revenue += daily_revenue
            self.total_regret += daily_regret

        # Save daily regret
        self.results.append(sum(regrets))

        return learners
