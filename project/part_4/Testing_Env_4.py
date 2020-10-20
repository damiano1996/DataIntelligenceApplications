import copy
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.User import User
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_4.Env_4 import Env_4
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_4.TS_Learner import TS_Learner


def test_part4(n_experiments=10,
               keep_daily_price=True,
               demand_chart_path='other_files/testing_part4_demandcurves.png',
               demand_chart_title='Part 4 - Demand Curves',
               results_chart_path='other_files/testing_part4_regrets.png',
               results_chart_title='Part 4 - Regret'):
    np.random.seed(0)

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

    env = Env_4(initial_date=initial_date,
                n_days=n_days,
                users_per_day=avg_users_per_day,
                multi_class_handler=mch,
                n_arms=n_arms_pricing)

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

    rewards_per_experiment = []  # collect all the rewards achieved from the TS
    optimals_per_experiment = []  # collect all the optimals of the users generated
    args = [{'environment': copy.deepcopy(env), 'index': idx, 'keep_daily_price': keep_daily_price} for idx in
            range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=1) as pool:  # multiprocessing.cpu_count()
        results = pool.map(execute_experiment, args, chunksize=1)

    for result in results:
        rewards_per_experiment.append(result['collected_rewards'])
        optimals_per_experiment.append(result['optimal_revenues'])

    plt.title(results_chart_title)
    # for opt_class_name, opt in mch.classes_opt.items():
    #     area = opt['price'] * opt['probability']
    #     plt.plot(np.cumsum(np.mean(area - rewards_per_experiment, axis=0)),
    #              label='Regret of the ' + opt_class_name.upper() + ' model')

    # Regret computed UN-knowing the class of the users
    area_aggregate = mch.aggregate_opt['price'] * mch.aggregate_opt['probability']
    for rewards in rewards_per_experiment:
        plt.plot(np.cumsum(np.asarray(area_aggregate) - np.asarray(rewards)), alpha=0.2, c='C0')
    plt.plot(np.cumsum(np.mean(area_aggregate - rewards_per_experiment, axis=0)),
             label='Mean Regret of the Aggregate Model', c='C0')

    # Below the regret computed knowing the optimal for each user
    for opt, rewards in zip(optimals_per_experiment, rewards_per_experiment):
        plt.plot(np.cumsum(np.asarray(opt) - np.asarray(rewards)), alpha=0.2, c='C1')
    plt.plot(np.cumsum(np.mean(optimals_per_experiment, axis=0) - np.mean(rewards_per_experiment, axis=0)),
             label='Mean Regret of the True Evaluation', c='C1')

    plt.xlabel('Time')
    plt.ylabel('Regret')
    plt.legend()
    plt.savefig(results_chart_path)
    plt.show()


def execute_experiment(args):
    index = args['index']
    env = args['environment']
    keep_daily_price = args['keep_daily_price']

    _, done = env.reset()
    ts_learner = TS_Learner(n_arms=n_arms_pricing, arm_prices=env.arm_prices['prices'])
    # ts_learner = SWTS_Learner(n_arms=n_arms, arm_prices=env.arm_prices['prices'], window_size=2000)
    optimal_revenues = np.array([])

    new_day = True
    while not done:
        user = User(random=True)

        if keep_daily_price:
            if new_day:
                pulled_arm = ts_learner.pull_arm_revenue()  # optimize by revenue
        else:
            pulled_arm = ts_learner.pull_arm_revenue()  # optimize by revenue

        reward, current_date, new_day, done, opt_revenue = env.round(pulled_arm, user)
        ts_learner.update(pulled_arm, reward)
        optimal_revenues = np.append(optimal_revenues, opt_revenue)

    print(str(index) + ' has ended')

    return {'collected_rewards': ts_learner.collected_rewards, 'optimal_revenues': optimal_revenues}


if __name__ == '__main__':
    test_part4()
