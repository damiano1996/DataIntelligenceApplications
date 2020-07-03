class BudgetAllocator():

    def __init__(self, multi_subcampaign_handler):
        """
        :param multi_subcampaign_handler: MultiSubCampaignHandler Object
        """
        # we can update the subcampaigns directly from here or from another super class...
        self.msh = multi_subcampaign_handler

    def day_zero_initialization(self):
        pass

    def update(self):
        """
            Here we update n_j, v_j and the total regret
        :return:
        """
        pass

    def get_best_budgets(self):
        """
            Calcutate the best budget for the subcampaigns
        :return:
        """
        pass
