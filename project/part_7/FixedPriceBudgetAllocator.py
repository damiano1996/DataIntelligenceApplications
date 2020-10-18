import numpy as np

from project.part_2.Optimizer import fit_table
from project.dia_pckg.Config import *
from project.part_7.SubCampaignHandler import SubCampaignHandler


# TODO compute_optimal_reward -> compute optimal price based on allocation curves and conversion rates
#  and return optimal reward

class FixedPriceBudgetAllocator:

    def __init__(self):

        self.n_updates = 0
        self.subcampaignHandlers = []
        bids = np.linspace(0, max_bid, n_arms_advertising)
        prices = None  # TODO
        for s in range(n_subcamp):
            self.subcampaignHandlers.append(SubCampaignHandler(classes_config.keys()[s], bids, prices))

    def update(self, price, allocation, click_per_class, purchases_per_class):
        for subh in self.subcampaignHandlers:
            subh.daily_update(price, allocation[subh.class_name], click_per_class[subh.class_name],
                              purchases_per_class[subh.class_name])
        self.n_updates += 1

    def compute_best_allocation(self, price):
        table_all_subs = np.ndarray(shape=(0, n_arms_advertising),
                                    dtype=np.float32)
        for subh in self.subcampaignHandlers:
            estimated_cr = subh.get_estimated_cr(price)
            estimated_clicks = subh.get_estimated_clicks()
            estimated_purchases = estimated_clicks * estimated_cr
            table_all_subs = np.append(table_all_subs, np.atleast_2d(estimated_purchases.T), 0)

        return fit_table(table_all_subs)

    # TODO CASH_PRICE = PRICES[PRICE]
    def next_price(self):
        while self.n_updates < n_arms_pricing:

            if self.n_updates > 1:
                allocation = self.compute_best_allocation(self.n_updates)
            else:
                avg = 1 / n_subcamp
                allocation = [avg, avg, avg]

            return self.n_updates, allocation
        max_estimated_reward = -1
        final_allocation = []
        final_arm_price = -1
        for price in range(n_arms_pricing):
            result = self.compute_best_allocation(price)
            allocation_atprice = np.asarray(result[0])
            purch_atprice = result[1]
            if max_estimated_reward < purch_atprice * price:  # PRICE
                max_estimated_reward = purch_atprice * price  # PRICE
                final_allocation = allocation_atprice
                final_arm_price = price
        allocation_x_class = {}
        for subh, c in zip(self.subcampaignHandlers, range(len(classes_config))):
            allocation_x_class[subh.class_name] = final_allocation[c]
        return final_arm_price, allocation_x_class

    def compute_optimal_reward(self):
        pass
