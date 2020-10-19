import numpy as np

from project.part_2.Optimizer import fit_table
from project.dia_pckg.Config import *
from project.part_7.SubCampaignHandler import SubCampaignHandler


class FixedPriceBudgetAllocator:

    def __init__(self):

        self.n_updates = 0
        self.subcampaignHandlers = []
        self.bids = np.linspace(0, max_bid, n_arms_advertising)
        self.prices = np.linspace(product_config["base_price"], product_config["max_price"], n_arms_pricing)  # TODO
        for s in range(n_subcamp):
            self.subcampaignHandlers.append(SubCampaignHandler(classes_config.keys()[s], bids, self.prices))

    def update(self, price, allocation, click_per_class, purchases_per_class):
        for subh in self.subcampaignHandlers:
            subh.daily_update(price, allocation[subh.class_name], click_per_class[subh.class_name],
                              purchases_per_class[subh.class_name])
        self.n_updates += 1

    def compute_best_allocation(self, arm_price):
        table_all_subs = np.ndarray(shape=(0, n_arms_advertising),
                                    dtype=np.float32)
        for subh in self.subcampaignHandlers:
            estimated_cr = subh.get_estimated_cr(arm_price)
            estimated_clicks = subh.get_estimated_clicks()
            estimated_purchases = estimated_clicks * estimated_cr
            table_all_subs = np.append(table_all_subs, np.atleast_2d(estimated_purchases.T), 0)

        return fit_table(table_all_subs)

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
        for arm_price in range(n_arms_pricing):
            result = self.compute_best_allocation(arm_price)
            allocation_atprice = np.asarray(result[0])
            purch_atprice = result[1]
            if max_estimated_reward < purch_atprice * self.prices[arm_price]:
                max_estimated_reward = purch_atprice * self.prices[arm_price]
                final_allocation = allocation_atprice
                final_arm_price = arm_price
        allocation_x_class = {}
        for subh, c in zip(self.subcampaignHandlers, range(len(classes_config))):
            allocation_x_class[subh.class_name] = final_allocation[c]
        return final_arm_price, allocation_x_class

    def compute_optimal_reward(self, biddingEnvironment, mch):
        optimal_reward = -1

        for arm_price in range(n_arms_pricing):
            table_all_subs = np.ndarray(shape=(0, n_arms_advertising), dtype=np.float32)
            for idx, subh in enumerate(self.subcampaignHandlers):
                cr = mch.get_conv_rate(subh.class_name, arm_price)
                clicks_x_budget = biddingEnvironment.get_optimal_clicks(idx)
                purchases_x_budget = clicks_x_budget * cr
                table_all_subs = np.append(table_all_subs, np.atleast_2d(purchases_x_budget.T), 0)

            result = fit_table(table_all_subs)
            purch_atprice = result[1]
            if optimal_reward < purch_atprice * self.prices[arm_price]:
                optimal_reward = purch_atprice * self.prices[arm_price]
        return optimal_reward
