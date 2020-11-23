import copy
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.Product import Product
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_6.BudgetAllocator import BudgetAllocator


def test_part6(n_experiments=1,
               enable_pricing=True,
               plot_advertising=False,
               keep_daily_price=True,
               demand_chart_path='other_files/testing_part6_demandcurves.png',
               demand_chart_title='Part 6 - Demand Curves',
               results_chart_path='other_files/testing_part6_regrets.png',
               results_chart_title='Part 6 - Regret',
               advertising_chart_root_path='other_files/testing_part6_'):
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
    args = [{'environment': copy.deepcopy(base_env),
             'index': idx,
             'multiclasshandler': mch,
             'enable_pricing': enable_pricing,
             'keep_daily_price': keep_daily_price,
             'plot_advertising': plot_advertising,
             'advertising_chart_root_path': advertising_chart_root_path}
            for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=10) as pool:  # multiprocessing.cpu_count()
        results = pool.map(execute_experiment, args, chunksize=1)

    for result in results:
        agnostic_regret_per_experiment.append(result['agnostic_regret'])
        regret_per_experiment.append(result['regret'])
        final_loss_per_experiment.append(result['loss'])

    mean_loss = float("{:.2f}".format(np.mean(final_loss_per_experiment) * 100))
    print('\n\nFINAL LOSS:', mean_loss)

    results_chart_title = results_chart_title + " , Loss: " + str(mean_loss) + "%"
    plt.title(results_chart_title, fontsize=20)
    # for agnostic_regret in agnostic_regret_per_experiment:
    #     plt.plot(np.cumsum(agnostic_regret), alpha=0.1, c='C2')
    # plt.plot(np.cumsum(np.mean(agnostic_regret_per_experiment, axis=0)),
    # c='C1', label='Agnostic Regret')

    for regret in regret_per_experiment:
        plt.plot(np.cumsum(regret), alpha=0.2, c='C2')
    plt.plot(np.cumsum(np.mean(regret_per_experiment, axis=0)),
             c='C2', label='Real Regret')  # (Advertising <==> Pricing)')

    plt.xlabel('Time')
    plt.ylabel('Regret')
    # plt.ylim([0, np.cumsum(np.mean(regret_per_experiment, axis=0))[-1]])
    plt.legend()
    plt.savefig(results_chart_path)
    plt.show()


def execute_experiment(args):
    index = args['index']
    env = args['environment']
    mch = args['multiclasshandler']
    enable_pricing = args['enable_pricing']
    keep_daily_price = args['keep_daily_price']
    plot_advertising = args['plot_advertising']
    advertising_chart_root_path = args['advertising_chart_root_path']

    budget_allocator = BudgetAllocator(multi_class_handler=mch,
                                       n_arms_pricing=n_arms_pricing,
                                       n_arms_advertising=n_arms_advertising,
                                       enable_pricing=enable_pricing,
                                       keep_daily_price=keep_daily_price)
    budget_allocator.day_zero_initialization()

    current_day, done = env.reset()

    while not done:
        print('day:', current_day)

        # Handler solve the problem for current day
        budget_allocator.update()

        # Day step
        current_day, done = env.step()

    if plot_advertising:
        for idx, subcampaign_handler in enumerate(budget_allocator.msh.subcampaigns_handlers):
            unknown_clicks_curve = \
                subcampaign_handler.advertising.env.subs[subcampaign_handler.advertising.sub_idx].means['phase_0']
            subcampaign_handler.advertising.learner.plot(unknown_clicks_curve, sigma_scale_factor=10,
                                                         chart_path=advertising_chart_root_path + 'subcamaign_' + str(
                                                             idx))

    print('Total revenue:', int(budget_allocator.msh.total_revenue),
          'Cumulative regret:', int(sum(budget_allocator.regret)),
          'Loss:', sum(budget_allocator.regret) / budget_allocator.msh.total_revenue)

    print(str(index) + ' has ended')

    return {'agnostic_regret': budget_allocator.msh.regret, 'regret': budget_allocator.regret,
            'loss': sum(budget_allocator.regret) / (budget_allocator.msh.total_revenue + sum(budget_allocator.regret))}


if __name__ == '__main__':
    test_part6()
