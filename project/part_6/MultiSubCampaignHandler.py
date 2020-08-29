from project.part_2.Utils import get_idx_arm_from_allocation
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
        for i, class_ in enumerate(self.mch.classes):
            subcampaign_handler = SubCampaignHandler(class_name=class_.name,
                                                     multi_class_handler=self.mch,
                                                     subcampaign_idx=i,
                                                     n_arms_pricing=self.n_arms_pricing,
                                                     n_arms_advertising=self.n_arms_advertising)
            self.subcampaigns_handlers.append(subcampaign_handler)

        self.regret = []
        self.total_revenue = 0
        self.total_regret = 0

    def update_all_subcampaign_handlers(self, allocations, opt=False):
        """
            Execute one day round:
            Update advertising and pricing model
            Update budget allocation
        :return:
        """

        # Learn about data of the current day, given the budget allocations
        learners = []
        total_daily_regret = 0
        for subcampaign_handler, allocation in zip(self.subcampaigns_handlers, allocations):
            # conversion from percentage to arm index
            pulled_arm = get_idx_arm_from_allocation(allocation=allocation,
                                                     bids=subcampaign_handler.advertising.bids,
                                                     max_bid=max_bid)

            daily_regret, daily_revenue = subcampaign_handler.daily_update(pulled_arm, opt=opt)
            learner = subcampaign_handler.get_updated_parameters()
            learners.append(learner)
            total_daily_regret += daily_regret
            self.total_revenue += daily_revenue

        self.total_regret += total_daily_regret
        # Save daily regret
        self.regret.append(total_daily_regret)

        return learners
