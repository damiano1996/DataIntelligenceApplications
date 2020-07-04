from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_6.SubCampaignHandler import SubCampaignHandler
from project.part_6.BudgetAllocator import BudgetAllocator




class MultiSubCampaignHandler:

    def __init__(self, multi_class_handler):
        """
        :param subcampaign_handlers: undefined number of SubCampaignHandler objects
        """
        self.mch = multi_class_handler

        self.n_arms_pricing = 20
        self.n_arms_advertising = 11

        self.budget_allocator = BudgetAllocator(self.n_arms_advertising, len(self.mch.classes))
        
        self.sub_campaigns = list()
        for classe in self.mch.classes:
            self.sub_campaigns.append(SubCampaignHandler(classe.name, self.mch, self.n_arms_pricing, self.n_arms_advertising))
       

    def update_all(self):
        """
        Execute one day round:
        Select the best budget allocation from the previous day
        Update advertising and pricing model
        Update budget allocation
        :return:
        """
        #Get the best budget allocation from the information of the previous day
        allocations = self.budget_allocator.get_best_allocations()
        
        print ('best allocations: ', allocations)

        #Learn about data of the current day, given the budget allocations
        learners = []
        for i in range(len(self.sub_campaigns)):
            learner = self.sub_campaigns[i].daily_update(allocations[i]) 
            learners.append(learner)

        #Update the budget allocations for the next day
        self.budget_allocator.update_v1(learners)

        print ()


        """
        results = []
        for (learned_budget_allocation, real_budget_allocation), sch in zip(budgets, self.schs):
            n_daily_clicks_learned, daily_regret = sch.daily_update(learned_budget_allocation, real_budget_allocation)
            # I leave the tuple until the other implementations aren't completed.
            # -> dictionaries must be implemented.
            results.append((n_daily_clicks_learned, daily_regret))
        return results
        """