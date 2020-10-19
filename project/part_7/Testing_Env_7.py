import copy
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.Product import Product
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_7.FixedPriceBudgetAllocator import FixedPriceBudgetAllocator
from project.part_4.MultiClassHandler import MultiClassHandler


def test_part7(n_experiments=10,
               enable_pricing=True,
               plot_advertising=True,
               n_days_same_price=2,
               demand_chart_path='other_files/testing_part7_demandcurves.png',
               demand_chart_title='Part 7 - Demand Curves',
               results_chart_path='other_files/testing_part7_regrets.png',
               results_chart_title='Part 7 - Regret',
               advertising_chart_root_path='other_files/testing_part7_',
               best_price_chart='other_files/test_part7_bestprices.png',
               best_price_title='Part 7 - Best Candidate Price'):
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

    base_env = Environment(initial_date=initial_date, n_days=n_days)

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

    final_loss_per_experiment = []  # collect all the regrets achieved
    agnostic_regret_per_experiment = []  # collect all the regrets achieved
    regret_per_experiment = []
    best_prices_experiment = []
    args = [{'environment': copy.deepcopy(base_env),
             'index': idx,
             'multiclasshandler': mch,
             'enable_pricing': enable_pricing,
             'plot_advertising': plot_advertising,
             'advertising_chart_root_path': advertising_chart_root_path,
             'n_days_same_price': n_days_same_price}
            for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=1) as pool:  # multiprocessing.cpu_count()
        results = pool.map(execute_experiment, args, chunksize=1)

    for result in results:
        agnostic_regret_per_experiment.append(result['agnostic_regret'])
        regret_per_experiment.append(result['regret'])
        final_loss_per_experiment.append(result['loss'])
        best_prices_experiment.append(result['best_prices'])
    print('\n\nFINAL LOSS:', np.mean(final_loss_per_experiment))

    plt.title(results_chart_title, fontsize=20)
    # for agnostic_regret in agnostic_regret_per_experiment:
    #     plt.plot(np.cumsum(agnostic_regret), alpha=0.1, c='C2')
    # plt.plot(np.cumsum(np.mean(agnostic_regret_per_experiment, axis=0)),
    #          c='C2', label='Regret (Advertising <=!=> Pricing)')

    for regret in regret_per_experiment:
        plt.plot(np.cumsum(regret), alpha=0.2, c='C2')
    plt.plot(np.cumsum(np.mean(regret_per_experiment, axis=0)), c='C2',
             label='Mean Regret')  # (Advertising <==> Pricing)')
    plt.xlabel('Time')
    plt.ylabel('Regret')
    plt.ylim([0, np.cumsum(np.mean(regret_per_experiment, axis=0))[-1]])
    plt.legend()
    plt.savefig(results_chart_path)
    plt.show()

    plt.title(best_price_title, fontsize=14)
    for best_prices in best_prices_experiment:
        plt.plot(best_prices, alpha=0.2, c='C2')
    plt.plot(np.mean(best_prices_experiment, axis=0), c='C2')
    plt.xlabel('Time')
    plt.ylabel('Price USD')
    # plt.ylim([0, np.max(np.mean(np.asarray(best_prices_experiment), axis=0))])
    # plt.legend()
    plt.savefig(best_price_chart)
    plt.show()


def execute_experiment(args):
    index = args['index']
    mch = args['multiclasshandler']
    biddingEnvironment = args['bidding_environment']
    purchasesEnvironment = args['purchases_environment']
    plot_advertising = args['plot_advertising']
    advertising_chart_root_path = args['advertising_chart_root_path']

    fix_price_budget_allocator = FixedPriceBudgetAllocator()



    current_day = 0
    done = False
    regret = []
    optimal = fix_price_budget_allocator.compute_optimal_reward(biddingEnvironment, mch)
    while not done:
        print('day:', current_day)
        purchases_per_class = {}
        # Handler solve the problem for current day
        arm_price, allocation = fix_price_budget_allocator.next_price()
        click_per_class = biddingEnvironment.round(allocation.values())
        purchases_per_class = purchasesEnvironment.round(arm_price, click_per_class)

        regret.append(optimal - (sum(purchases_per_class.values()) * fix_price_budget_allocator.prices[arm_price]))

        fix_price_budget_allocator.update(arm_price,allocation, click_per_class, purchases_per_class)

        # Day step
        current_day, done = biddingEnvironment.step()
        purchasesEnvironment.step()

    if plot_advertising:
        for idx, subcampaign_handler in enumerate(fix_price_budget_allocator.msh.subcampaigns_handlers):
            unknown_clicks_curve = subcampaign_handler.advertising.env.subs[
                subcampaign_handler.advertising.sub_idx].means['phase_0']
            subcampaign_handler.advertising.learner.plot(unknown_clicks_curve,
                                                         sigma_scale_factor=10,
                                                         chart_path=advertising_chart_root_path +
                                                                    'subcampaign_' +
                                                                    str(idx))

    print('Total revenue:', int(fix_price_budget_allocator.msh.total_revenue),
          'Cumulative regret:', int(sum(fix_price_budget_allocator.regret)),
          'Loss:', sum(fix_price_budget_allocator.regret) / fix_price_budget_allocator.msh.total_revenue)

    print(str(index) + ' has ended')

    print(fix_price_budget_allocator.best_prices)

    return {'agnostic_regret': fix_price_budget_allocator.msh.regret,
            'regret': fix_price_budget_allocator.regret,
            'loss': sum(fix_price_budget_allocator.regret) / fix_price_budget_allocator.msh.total_revenue,
            'best_prices': fix_price_budget_allocator.best_prices}


if __name__ == '__main__':
    test_part7(n_experiments=4, plot_advertising=False, enable_pricing=True)
