import copy
from multiprocessing import Pool

import numpy as np

from project.part_7.Env_7 import Env7
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.dia_pckg.Environment import Environment
from project.dia_pckg.Product import Product
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_7.FixedPriceBudgetAllocator import FixedPriceBudgetAllocator
from project.part_4.MultiClassHandler import MultiClassHandler


def test_part7(n_experiments=10,
               demand_chart_path='other_files/testing_part7_demandcurves.png',
               demand_chart_title='Part 7 - Demand Curves',
               results_chart_path='other_files/testing_part7_regrets.png',
               results_chart_title='Part 7 - Regret'):

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

    #
    # plt.title(demand_chart_title)
    # for class_ in mch.classes:
    #     plt.plot(class_.conv_rates['phase_0']['prices'],
    #              class_.conv_rates['phase_0']['probabilities'], label=class_.name.upper(), linestyle='--')
    # plt.plot(mch.aggregate_demand_curve['prices'],
    #          mch.aggregate_demand_curve['probabilities'], label='aggregate')
    #
    # for opt_class_name, opt in mch.classes_opt.items():
    #     plt.scatter(opt['price'],
    #                 opt['probability'], marker='o', label=f'opt {opt_class_name.upper()}')
    # plt.scatter(mch.aggregate_opt['price'],
    #             mch.aggregate_opt['probability'], marker='o', label='opt aggregate')
    #
    # plt.xlabel('Price')
    # plt.ylabel('Conversion Rate')
    # plt.legend()
    # plt.savefig(demand_chart_path)
    # plt.show()

    regret_per_experiment = []

    bids = np.linspace(0,max_bid,n_arms_advertising)
    print(bids)
    env_bid = BiddingEnvironment(bids)
    env_purchases = Env7(mch, n_arms_pricing)

    args = [{
        'index': idx,
        'multiclasshandler': mch,
        "bidding_environment": copy.deepcopy(env_bid),
        'purchases_environment': copy.deepcopy(env_purchases)}
        for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=1) as pool:  # multiprocessing.cpu_count()
        results = pool.map(execute_experiment, args, chunksize=1)

    regret_per_experiment = []
    regret_notfixed_per_experiment = []
    final_loss_per_experiment = []
    final_loss_per_experiment_notfixed = []

    for result in results:
        regret_notfixed_per_experiment.append(result[1])
        regret_per_experiment.append(result[0])
        final_loss_per_experiment.append(sum(result[0]))
        final_loss_per_experiment_notfixed.append(sum(result[1]))

    print('\n\nFINAL LOSS:', np.mean(final_loss_per_experiment))
    print('\n\nFINAL NOT FIXED LOSS:', np.mean(final_loss_per_experiment_notfixed))
    print('\n\nMEAN LOSS:', np.mean(final_loss_per_experiment)/n_days)


    plt.title(results_chart_title, fontsize=20)

    for regret in regret_per_experiment:
        plt.plot(np.cumsum(regret), alpha=0.2, c='C2')
    plt.plot(np.cumsum(np.mean(regret_per_experiment, axis=0)), c='C2',
             label='Mean Regret')
    for regret in regret_notfixed_per_experiment:
        plt.plot(np.cumsum(regret), alpha=0.2, c='C1')
    plt.plot(np.cumsum(np.mean(regret_notfixed_per_experiment, axis=0)), c='C1',
             label='Mean Regret Price Not Fixed X Class')
    plt.xlabel('Time')
    plt.ylabel('Regret')
    plt.ylim([0, np.cumsum(np.mean(regret_per_experiment, axis=0))[-1]])
    plt.legend()
    plt.savefig(results_chart_path)
    plt.show()


def execute_experiment(args):
    index = args['index']
    mch = args['multiclasshandler']
    biddingEnvironment = args['bidding_environment']
    purchasesEnvironment = args['purchases_environment']

    fix_price_budget_allocator = FixedPriceBudgetAllocator()



    current_day = 0
    done = False
    regret = []
    regret_not_fixed = []
    optimal, opt_price = fix_price_budget_allocator.compute_optimal_reward(biddingEnvironment, mch)
    optimal_not_fixed = fix_price_budget_allocator.get_optimal_reward_not_fixedprice(biddingEnvironment, mch)
    print(f"optimal daily reward: {optimal}")
    print(f"optimal arm price: {opt_price}")
    while not done:
        print('day:', current_day)

        arm_price, allocation = fix_price_budget_allocator.next_price()
        click_per_class = biddingEnvironment.round(list(allocation.values()))
        purchases_per_class = purchasesEnvironment.round(arm_price, click_per_class)

        regret_not_fixed.append(optimal_not_fixed - (sum(purchases_per_class.values()) * fix_price_budget_allocator.prices[arm_price]))

        regret.append(optimal - (sum(purchases_per_class.values()) * fix_price_budget_allocator.prices[arm_price]))
        fix_price_budget_allocator.update(arm_price,allocation, click_per_class, purchases_per_class)

        # Day step
        current_day, done = biddingEnvironment.step()


    return regret, regret_not_fixed


if __name__ == '__main__':
    test_part7(n_experiments=5)
