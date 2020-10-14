import numpy as np

from project.part_2.Optimizer import fit_table
from project.part_6.BudgetAllocator import BudgetAllocator


class FixedPriceBudgetAllocator(BudgetAllocator):

    def __init__(self,
                 multi_class_handler,
                 n_arms_pricing,
                 n_arms_advertising,
                 enable_pricing=True,
                 n_days_same_price=2):
        """
        :param multi_class_handler:
        :param n_arms_pricing:
        :param n_arms_advertising:
        """
        super(FixedPriceBudgetAllocator, self).__init__(multi_class_handler=multi_class_handler,
                                                        n_arms_pricing=n_arms_pricing,
                                                        n_arms_advertising=n_arms_advertising,
                                                        enable_pricing=enable_pricing,
                                                        keep_daily_price=None)

        self.fixed_price = 0
        self.n_updates = 0
        self.n_days_same_price = n_days_same_price

        self.cc_prices = {'candidate_prices': np.asarray(self.msh.subcampaigns_handlers[0].pricing.learner.arm_prices),
                          'collected_revenues': np.zeros(shape=(n_arms_pricing,))}

        self.best_prices = []

    def day_zero_initialization(self):
        """
            Initialize allocations for day zero
        """
        avg = 1 / self.n_subcampaigns
        allocation = [avg, avg, avg]
        self.msh.update_all_subcampaign_handlers(allocation, pull_fix_arm=self.fixed_price)
        return allocation

    def update(self):

        table_all_subs = np.ndarray(shape=(0, len(self.msh.subcampaigns_handlers[0].advertising.env.bids)),
                                    dtype=np.float32)

        for subcampaign_handler in self.msh.subcampaigns_handlers:
            # update renvenues:
            self.cc_prices['collected_revenues'][self.fixed_price] += subcampaign_handler.daily_revenue

            # compute allocation:
            learner_clicks = subcampaign_handler.get_updated_parameters()

            n_clicks = subcampaign_handler.total_clicks
            v = subcampaign_handler.total_revenue / n_clicks if n_clicks != 0 else 0

            revenue_clicks = np.multiply(learner_clicks, v) if self.enable_pricing else learner_clicks

            table_all_subs = np.append(table_all_subs, np.atleast_2d(revenue_clicks.T), 0)

        # self.best_allocation = fit_table(table_all_subs)[0]
        self.best_allocation = np.asarray(fit_table(table_all_subs)[0])
        print('BEST ALLOCATION FOUND:', self.best_allocation)

        if round(sum(self.best_allocation), 3) != 1:
            raise Exception("Allocation unfeasible")

        # updates
        self.msh.update_all_subcampaign_handlers(self.best_allocation, pull_fix_arm=self.fixed_price)
        self.regret.append(self.optimal_total_revenue - self.msh.daily_revenue)

        # get best price
        candidate_price = self.cc_prices['candidate_prices'][self.fixed_price]
        print(f'CURRENT CANDIDATE PRICE: {candidate_price}')

        # next price:
        if self.n_updates % self.n_days_same_price == 0:
            self.fixed_price += 1
            if self.fixed_price >= self.n_arms_pricing:
                self.fixed_price = 0
                # all prices have been tested, now we can compute the most promising price
                best_price = self.cc_prices['candidate_prices'][
                    int(np.argmax(np.asarray(self.cc_prices['collected_revenues'])))]
                print(f'BEST PRICE: {best_price}')
                self.best_prices.append(best_price)
                print(self.best_prices)

                # we can reset or not the collected revenue for the interval
                # self.cc_prices['collected_revenues'] = np.zeros(shape=(self.n_arms_pricing,))
                # after testing: this doesn't affect the results

        self.n_updates += 1
