from project.dia_pckg.Config import *
from project.part_2.Utils import *
from project.part_7_normal.SubCampaignHandler import SubCampaignHandler


class FixedPriceBudgetAllocator:

    def __init__(self,
                 artificial_noise_ADV,
                 artificial_noise_CR):

        self.artificial_noise_ADV = artificial_noise_ADV
        self.artificial_noise_CR = artificial_noise_CR

        self.n_updates = 0
        self.subcampaignHandlers = []
        self.bids = np.linspace(0, max_bid, n_arms_advertising)
        self.prices = np.linspace(product_config["base_price"], product_config["max_price"], n_arms_pricing)

        for s in range(n_subcamp):
            self.subcampaignHandlers.append(SubCampaignHandler(list(classes_config.keys())[s], self.bids, self.prices))

    def update(self, price, allocation, click_per_class, purchases_per_class):
        print(
            f"UPDATE price={price} "
            f"allocation_arms={list(allocation.values())} "
            f"clicks={click_per_class} "
            f"purch={list(purchases_per_class.values())}")
        for idx, subh in enumerate(self.subcampaignHandlers):
            subh.daily_update(price, allocation[subh.class_name], click_per_class[idx],
                              purchases_per_class[subh.class_name])
        self.n_updates += 1

    def compute_best_allocation(self, arm_price):
        table_all_subs = np.ndarray(shape=(0, n_arms_advertising),
                                    dtype=np.float32)

        for subh in self.subcampaignHandlers:
            estimated_cr = subh.get_estimated_cr(arm_price, self.artificial_noise_CR)
            estimated_clicks = subh.get_estimated_clicks(self.artificial_noise_ADV)
            estimated_purchases = estimated_clicks * estimated_cr
            table_all_subs = np.append(table_all_subs, np.atleast_2d(estimated_purchases.T), 0)

        result = fit_table(table_all_subs)
        return result

    def next_price(self):
        while self.n_updates < n_arms_pricing:

            if self.n_updates > 0:
                allocation = self.compute_best_allocation(self.n_updates)[0]
            else:
                avg = 1 / n_subcamp
                allocation = [avg, avg, avg]
            allocation_x_class = {}
            for subh, c in zip(self.subcampaignHandlers, range(len(classes_config))):
                allocation_x_class[subh.class_name] = get_idx_arm_from_allocation(allocation[c], self.bids)
            return self.n_updates, allocation_x_class

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
            allocation_x_class[subh.class_name] = get_idx_arm_from_allocation(final_allocation[c], self.bids)
        return final_arm_price, allocation_x_class

    def compute_optimal_reward(self, biddingEnvironment, mch):
        optimal_reward = -1
        best_price = -1
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
                best_price = arm_price
                optimal_reward = purch_atprice * self.prices[arm_price]
        return optimal_reward, best_price

    def get_optimal_reward_not_fixedprice(self, biddingEnvironment, mch):
        """
            This function is to compute the total optimal revenue, for the computation of the non-agnostic regret.
            Note: the so called "agnostic" regret is the regret in which the optimal revenue
                is computed using the "optimal number of clicks",
                but the "optimal number of clicks" is NOT computed knowing the pricing.
                Below, we compute the "optimal number of clicks" using the pricing!
        """
        table_all_subs = np.ndarray(shape=(0, len(self.bids)),
                                    dtype=np.float32)

        # for loop to initialize the table with the product between the unknown curves and the optimal revenues
        for sub_idx, subcampaign_handler in enumerate(self.subcampaignHandlers):
            unknown_clicks_curve = biddingEnvironment.get_optimal_clicks(sub_idx)
            opt = mch.get_optimal(class_name=subcampaign_handler.class_name)
            optimal_revenue = opt['price'] * opt['probability']

            revenue_clicks = np.multiply(unknown_clicks_curve, optimal_revenue)
            table_all_subs = np.append(table_all_subs, np.atleast_2d(revenue_clicks.T), 0)

        # computation of the optimal allocation
        optimal_allocation = fit_table(table_all_subs)[0]

        # Once we have computed the optimal allocation, we can compute the total revenue
        # using the pricing
        optimal_total_revenue = 0
        for sub_idx, (allocation, subcampaign_handler) in enumerate(zip(optimal_allocation,
                                                                        self.subcampaignHandlers)):
            hypothetical_pulled_arm = get_idx_arm_from_allocation(
                allocation=allocation,
                bids=self.bids)
            opt = mch.get_optimal(class_name=subcampaign_handler.class_name)
            optimal_revenue = opt['price'] * opt['probability']
            optimal_clicks = biddingEnvironment.get_optimal_clicks(sub_idx)[hypothetical_pulled_arm]
            optimal_total_revenue += optimal_clicks * optimal_revenue

        return optimal_total_revenue
