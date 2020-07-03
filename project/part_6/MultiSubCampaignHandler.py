from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_6.SubCampaignHandler import SubCampaignHandler

class MultiSubCampaignHandler:
    """
        As we have created the part_4.MultiClassHandler,
        here we handle the SubCampaignHandler
    """

    def __init__(self, multi_class_handler):
        """
        :param subcampaign_handlers: undefined number of SubCampaignHandler objects
        """
        self.mch = multi_class_handler
        
        self.sub_campaigns = list()
        for classe in self.mch.classes:
            self.sub_campaigns.append(SubCampaignHandler(classe.name, self.mch))
       

    def update_all(self, *budgets):
        """
        :param budgets: list of tuples (learned_budget_allocation, real_budget_allocation)
        :return:
        """
        #For test, use only one subcampaign
        #for sub_campaign in self.sub_campaigns:
            #sub_campaign.daily_update(5,5)
        self.sub_campaigns[0].daily_update(5,5) # for test

        """
        results = []
        for (learned_budget_allocation, real_budget_allocation), sch in zip(budgets, self.schs):
            n_daily_clicks_learned, daily_regret = sch.daily_update(learned_budget_allocation, real_budget_allocation)
            # I leave the tuple until the other implementations aren't completed.
            # -> dictionaries must be implemented.
            results.append((n_daily_clicks_learned, daily_regret))
        return results
        """