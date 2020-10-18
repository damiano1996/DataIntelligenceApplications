import numpy as np

from project.part_2.Optimizer import fit_table
from project.part_6.BudgetAllocator import BudgetAllocator
from project.dia_pckg.Config import *
from project.part_7.MultiSubCampaignHandler import MultiSubCampaignHandler


# TODO subh.get_updated_parameters() NON PUO PRENDERSI I CLICK DALL'ENVIRONMENT
# TODO compute_optimal_reward -> compute optimal price based on allocation curves and conversion rates
#  and return optimal reward
# TODO getcr e update su subcampaignHandler

class FixedPriceBudgetAllocator():

    def __init__(self, mch):
        """
        :param multi_class_handler:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """
        self.n_updates = 0
        self.msh = MultiSubCampaignHandler(mch,n_arms_pricing,n_arms_advertising,True)


    def update(self, price,click_per_class,purchases_per_class):
        for subh in self.msh.subcampaigns_handlers:
            subh.update(price, click_per_class[subh.class_name], purchases_per_class[subh.class_name])
        self.n_updates += 1

    def compute_best_allocation(self,price):
        table_all_subs = np.ndarray(shape=(0, len(self.msh.subcampaigns_handlers[0].advertising.env.bids)),
                                    dtype=np.float32)
        for subh in self.msh.subcampaigns_handlers:
            estimated_cr = subh.getcr(price)
            estimated_clicks = subh.get_updated_parameters()
            estimated_purchases = estimated_clicks * estimated_cr
            table_all_subs = np.append(table_all_subs, np.atleast_2d(estimated_purchases.T), 0)

        return fit_table(table_all_subs)

    def next_price(self):
        while self.n_updates < n_arms_pricing:
            return self.n_updates, self.compute_best_allocation(self.n_updates)

        max_estimated_reward = -1
        final_allocation = []
        final_price = -1
        for price in range(n_arms_pricing):
            result = self.compute_best_allocation(price)
            allocation_atprice = np.asarray(result[0])
            purch_atprice = result[1]
            if max_estimated_reward < purch_atprice * price:
                max_estimated_reward = purch_atprice * price
                final_allocation = allocation_atprice
                final_price = price
        return final_price, final_allocation


    def compute_optimal_reward(self):
        pass
