import copy
import multiprocessing
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Campaign import Campaign
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Environment import Environment
from project.dia_pckg.Product import Product
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_6.BudgetAllocator import BudgetAllocator

np.random.seed(0)


def execute_experiment(args):
    index = args['index']
    env = args['environment']
    mch = args['multiclasshandler']

    budget_allocator = BudgetAllocator(multi_class_handler=mch,
                                       n_arms_pricing=20,
                                       n_arms_advertising=11)

    current_day, done = env.reset()

    while not done:
        print('day:', current_day)

        # Handler solve the problem for current day
        budget_allocator.update()

        # Day step
        current_day, done = env.step()
        print()

    print('Total revenue:', budget_allocator.msh.total_revenue)
    print(str(index) + ' has ended')

    return {'daily_regrets': budget_allocator.msh.results}


if __name__ == '__main__':
    campaign = Campaign(max_budget=seller_max_budget, max_n_clicks=max_n_clicks)

    # one product to sell
    product = Product(product_config=product_config)

    # initialization of the three classes
    class_names = list(classes_config.keys())
    class_1 = Class(class_name=class_names[0], class_config=classes_config[class_names[0]], product=product,
                    n_abrupt_phases=n_abrupts)
    class_2 = Class(class_name=class_names[1], class_config=classes_config[class_names[1]], product=product,
                    n_abrupt_phases=n_abrupts)
    class_3 = Class(class_name=class_names[2], class_config=classes_config[class_names[2]], product=product,
                    n_abrupt_phases=n_abrupts)

    mch = MultiClassHandler(class_1, class_2, class_3)

    base_env = Environment(initial_date=initial_date, n_days=50)

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
    plt.show()

    n_experiments = 1  # the number is small to do a raw test, otherwise set it to 1000
    regrets_per_experiment = []  # collect all the regrets achieved 
    args = [{'environment': copy.deepcopy(base_env), 'index': idx, 'multiclasshandler': mch}
            for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(execute_experiment, args, chunksize=1)

    for result in results:
        regrets_per_experiment.append(result['daily_regrets'])

    plt.plot(np.cumsum(np.mean(regrets_per_experiment, axis=0)))
    plt.xlabel('Time')
    plt.ylabel('Regret')
    # plt.legend()
    plt.show()
