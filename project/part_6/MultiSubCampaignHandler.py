class MultiSubCampaignHandler:
    """
        As we have created the part_4.MultiClassHandler,
        here we handle the SubCampaignHandler
    """

    def __init__(self, *subcampaign_handlers):
        """
        :param subcampaign_handlers: undefined number of SubCampaignHandler objects
        """
        self.schs = subcampaign_handlers

    def update_all(self, *budgets):
        """
        :param budgets: list of tuples (learned_budget_allocation, real_budget_allocation)
        :return:
        """
        results = []
        for (learned_budget_allocation, real_budget_allocation), sch in zip(budgets, self.schs):
            n_daily_clicks_learned, daily_regret = sch.daily_update(learned_budget_allocation, real_budget_allocation)
            # I leave the tuple until the other implementations aren't completed.
            # -> dictionaries must be implemented.
            results.append((n_daily_clicks_learned, daily_regret))
        return results
