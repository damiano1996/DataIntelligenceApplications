"""
    Definition of the campaign.
"""


class Campaign():

    def __init__(self, max_budget, max_n_clicks):
        """
        :param max_budget: maximum amount of budget
        :param max_n_clicks: max number of clicks
        """
        self.max_budget = max_budget
        self.max_n_clicks = max_n_clicks
