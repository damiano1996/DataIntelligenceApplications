from project.dia_pckg.Config import *
from project.part_2.Utils import *
from project.part_7_binomial.FixedPriceBudgetAllocator import FixedPriceBudgetAllocator as fp_binomial
from project.part_7_normal.SubCampaignHandler import SubCampaignHandler


class FixedPriceBudgetAllocator(fp_binomial):

    def __init__(self,
                 artificial_noise_ADV,
                 artificial_noise_CR, multiclasshandler):
        super().__init__(artificial_noise_ADV, multiclasshandler)
        self.artificial_noise_CR = artificial_noise_CR

        self.n_updates = 0
        self.subcampaignHandlers = []

        for s in range(n_subcamp):
            self.subcampaignHandlers.append(
                SubCampaignHandler(list(classes_config.keys())[s], self.bids, self.prices, multiclasshandler))

    def complete_update(self, price, allocation, click_per_class, purchases_per_class):
        print(
            f"UPDATE price={price} "
            f"allocation_arms={list(allocation.values())} "
            f"clicks={click_per_class} "
            f"purch={list(purchases_per_class.values())}")
        for idx, subh in enumerate(self.subcampaignHandlers):
            subh.comlete_daily_update(price, allocation[subh.class_name], click_per_class[idx],
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
