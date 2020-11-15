import copy
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_7.FixedPriceBudgetAllocator import FixedPriceBudgetAllocator as PBAbinomial
from project.part_7.part_7_normal.Normal_FixedPriceBudgetAllocator import Normal_FixedPriceBudgetAllocator as PBAnormal
from project.part_7.part_7_normal.Env_7 import Env7


def test_part7(n_experiments=10,
               execution_type="binomial",
               demand_chart_path='other_files/testing_part7_demandcurves.png',
               demand_chart_title='Part 7 - Demand Curves',
               artificial_noise_ADV=0.0,
               artificial_noise_CR=0.0,
               results_chart_path='other_files/testing_part7_regrets.png',
               results_chart_title='Part 7'):
    # one product to sell
    product = Product(product_config=product_config)

    # initialization of the three classes
    class_names = list(classes_config.keys())
    class_1 = Class(class_name=class_names[0], class_config=classes_config[class_names[0]], product=product,
                    n_abrupt_phases=n_abrupts_phases)
    class_2 = Class(class_name=class_names[1], class_config=classes_config[class_names[1]], product=product,
                    n_abrupt_phases=n_abrupts_phases)
    class_3 = Class(class_name=class_names[2], class_config=classes_config[class_names[2]], product=product,
                    n_abrupt_phases=n_abrupts_phases)

    mch = MultiClassHandler(class_1, class_2, class_3)

    plt.title(demand_chart_title)
    for class_ in mch.classes:
        plt.plot(class_.conv_rates['phase_0']['prices'],
                 class_.conv_rates['phase_0']['probabilities'], label=class_.name.upper(), linestyle='--')
    plt.plot(mch.aggregate_demand_curve['prices'],
             mch.aggregate_demand_curve['probabilities'], label='aggregate')

    for opt_class_name, opt in mch.classes_opt.items():
        plt.scatter(opt['price'],
                    opt['probability'], marker='o', label=f'opt {opt_class_name.upper()}')
    plt.scatter(mch.aggregate_opt['price'],
                mch.aggregate_opt['probability'], marker='o', label='opt aggregate')

    plt.xlabel('Price')
    plt.ylabel('Conversion Rate')
    plt.legend()
    plt.savefig(demand_chart_path)
    plt.show()

    bids = np.linspace(0, max_bid, n_arms_advertising)
    print(bids)
    if execution_type == "binomial":
        execute_experiment = execute_experiment_binomial
        args = [{
            'multiclasshandler': mch,
            'bidding_environment': BiddingEnvironment(bids),
            'artificial_noise_ADV': artificial_noise_ADV,
            'artificial_noise_CR': artificial_noise_CR
        } for idx in range(n_experiments)]
    elif execution_type == "normal":
        execute_experiment = execute_experiment_normal
        args = [{
            'multiclasshandler': mch,
            "bidding_environment": BiddingEnvironment(bids),
            'purchases_environment': Env7(mch, n_arms_pricing),
            'artificial_noise_ADV': artificial_noise_ADV,
            'artificial_noise_CR': artificial_noise_CR}
            for idx in range(n_experiments)]
    else:
        raise NotImplementedError()

    with Pool(processes=1) as pool:  # multiprocessing.cpu_count()
        results = pool.map(execute_experiment, args, chunksize=1)

    regret_per_experiment = []
    percentage_loss_per_experiment = []
    final_loss_per_experiment = []

    for result in results:
        regret_per_experiment.append(result[0])
        final_loss_per_experiment.append(sum(result[0]))
        percentage_loss_per_experiment.append(sum(result[0]) / (n_days * result[1]))

    print('\n\nMEAN LOSS:', np.mean(percentage_loss_per_experiment))

    plt.title(results_chart_title + f"{execution_type} "
                                    f"REGRET: {int(np.mean(percentage_loss_per_experiment) * 10000) / 100.0}%",
              fontsize=20)

    for regret in regret_per_experiment:
        plt.plot(np.cumsum(regret), alpha=0.2, c='C2')
    plt.plot(np.cumsum(np.mean(regret_per_experiment, axis=0)), c='C2',
             label='Mean Regret')
    plt.xlabel('Time')
    plt.ylabel('Regret')
    plt.ylim([0, np.max(final_loss_per_experiment)])
    plt.legend()
    plt.savefig(results_chart_path)
    plt.show()


def execute_experiment_binomial(args):
    mch = args['multiclasshandler']
    bidding_environment = args['bidding_environment']
    artificial_noise_adv = args['artificial_noise_ADV']
    artificial_noise_cr = args['artificial_noise_CR']

    fix_price_budget_allocator = PBAbinomial(artificial_noise_ADV=artificial_noise_adv,
                                             artificial_noise_CR=artificial_noise_cr,
                                             multiclasshandler=mch)

    done = False
    regret = []
    optimal, opt_price = fix_price_budget_allocator.compute_optimal_reward(bidding_environment, mch)
    print(f'Optimal arm: {opt_price}\n'
          f'Optimal daily revenue: {optimal}')

    while not done:
        # predict the best price and allocation for the day
        arm_price, allocation = fix_price_budget_allocator.next_price()

        # gather the daily information about click and purchases for each class
        click_per_class = bidding_environment.round(list(allocation.values()))
        reward_per_class = fix_price_budget_allocator.pull_arm_price(arm_price, click_per_class)

        # compute daily regret
        daily_revenue = sum(reward_per_class.values())
        regret.append(optimal - daily_revenue)

        # update budget allocator with the gathered information
        fix_price_budget_allocator.update(allocation, click_per_class)

        # Day step
        current_day, done = bidding_environment.step()

    print(f'daily regret: {np.sum(regret) / n_days}\n')
    return regret, optimal


def execute_experiment_normal(args):
    mch = args['multiclasshandler']
    bidding_environment = args['bidding_environment']
    purchases_environment = args['purchases_environment']
    artificial_noise_adv = args['artificial_noise_ADV']
    artificial_noise_cr = args['artificial_noise_CR']

    fix_price_budget_allocator = PBAnormal(artificial_noise_ADV=artificial_noise_adv,
                                           artificial_noise_CR=artificial_noise_cr,
                                           multiclasshandler=mch)

    done = False
    regret = []
    optimal, opt_price = fix_price_budget_allocator.compute_optimal_reward(bidding_environment, mch)

    print(f'Optimal arm: {opt_price}\n'
          f'Optimal daily revenue: {optimal} ')

    while not done:
        # predict the best price and allocation for the day
        arm_price, allocation = fix_price_budget_allocator.next_price()

        # gather the daily information about click and purchases for each class
        click_per_class = bidding_environment.round(list(allocation.values()))
        purchases_per_class = purchases_environment.round(arm_price, click_per_class)

        # compute daily regret
        daily_revenue = sum(purchases_per_class.values()) * fix_price_budget_allocator.prices[arm_price]
        regret.append(optimal - daily_revenue)

        # update budget allocator with the gathered information
        fix_price_budget_allocator.complete_update(arm_price, allocation, click_per_class, purchases_per_class)

        # Day step
        current_day, done = bidding_environment.step()

    print(f'daily regret: {np.sum(regret) / n_days}\n')
    return regret, optimal


if __name__ == '__main__':
    test_part7(n_experiments=3, execution_type="normal")
