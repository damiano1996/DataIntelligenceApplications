from project.part_6.SubCampaignHandler import SubCampaignHandler
from project.part_6.TemporaryConfig import classes_config


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

    def update_all(self, allocations):
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
            daily_regret, daily_revenue = subcampaign_handler.daily_update(allocation)
            learner = subcampaign_handler.get_update_parameters()

            learners.append(learner)
            regrets.append(daily_regret)
            self.total_revenue += daily_revenue

        # Save daily regret
        self.results.append(sum(regrets))

        return learners
