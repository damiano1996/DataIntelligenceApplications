import copy
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Campaign import Campaign
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.Product import Product
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_7.MultiSubcampaignHandler import CampaignHandler
from project.part_7.BudgetAllocator import BudgetAllocator

# np.random.seed(0)

enable_pricing = True
plot_advertising = False

pricing_arms = 10


def execute_experiment(args):
    index = args['index']
    env = args['environment']
    mch = args['multiclasshandler']
    budget_allocators = []

    msh = CampaignHandler()

    for pricing_arm in range(0, pricing_arms):
        budget_allocators.append(BudgetAllocator(pricing_arm, msh, n_arms_advertising, 3))

    for d in range(0, n_days):
        for ba in budget_allocators:
            allocation, click = ba.compute_best_allocation()
            _, daily_clicks = msh.update_all_subcampaign_handlers(allocation)
            env.round(ba.arm_pricing, daily_clicks)

    if plot_advertising:
        for subcampaign_handler in budget_allocator.msh.subcampaigns_handlers:
            unknown_clicks_curve = subcampaign_handler.advertising.env.subs[
                subcampaign_handler.advertising.sub_idx].means['phase_0']
            subcampaign_handler.advertising.learner.plot(unknown_clicks_curve, sigma_scale_factor=10)

    print('Total revenue:', int(budget_allocator.msh.total_revenue),
          'Cumulative regret:', int(sum(budget_allocator.regret)),
          'Final loss:', sum(budget_allocator.regret) / budget_allocator.msh.total_revenue)

    print(str(index) + ' has ended')

    return {'agnostic_regret': budget_allocator.msh.regret, 'regret': budget_allocator.regret}


if __name__ == '__main__':
    campaign = Campaign(max_budget=seller_max_budget, max_n_clicks=max_n_clicks)

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
    # plt.show()

    n_experiments = 10  # the number is small to do a raw test, otherwise set it to 1000
    agnostic_regret_per_experiment = []  # collect all the regrets achieved
    regret_per_experiment = []
    args = [{'environment': copy.deepcopy(base_env), 'index': idx, 'multiclasshandler': mch}
            for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=1) as pool:  # multiprocessing.cpu_count()
        results = pool.map(execute_experiment, args, chunksize=1)

    for result in results:
        agnostic_regret_per_experiment.append(result['agnostic_regret'])
        regret_per_experiment.append(result['regret'])

    title = ' & Pricing' if enable_pricing else ''
    title = f'Testing_Env_7 - Advertising{title}'
    plt.title(title, fontsize=20)

    for agnostic_regret in agnostic_regret_per_experiment:
        plt.plot(np.cumsum(agnostic_regret), alpha=0.4, c='C2')
    plt.plot(np.cumsum(np.mean(agnostic_regret_per_experiment, axis=0)),
             c='C2',
             label='Regret (Advertising <=!=> Pricing)')

    for regret in regret_per_experiment:
        plt.plot(np.cumsum(regret), alpha=0.4, c='C3')
    plt.plot(np.cumsum(np.mean(regret_per_experiment, axis=0)), c='C3', label='Regret (Advertising <==> Pricing)')
    plt.xlabel('Time')
    plt.ylabel('Regret')
    plt.legend()

    plt.savefig('other_files/' + title + '.png')
    plt.show()
