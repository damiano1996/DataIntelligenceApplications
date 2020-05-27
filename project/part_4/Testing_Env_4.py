import copy
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Campaign import Campaign
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.User import User
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_4.Env_4 import Env_4
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_4.TS_Learner import TS_Learner

np.random.seed(0)
n_arms = 20


def excecute_experiment(args):
    index = args['index']
    env = args['environment']

    _, done = env.reset()
    ts_learner = TS_Learner(n_arms=n_arms, arm_prices=env.arm_prices['prices'])
    # ts_learner = SWTS_Learner(n_arms=n_arms, arm_prices=env.arm_prices['prices'], window_size=2000)
    optimal_revenues = np.array([])

    while not done:
        user = User(random=True)

        # pulled_arm = ts_learner.pull_arm() #optimize by demand
        pulled_arm = ts_learner.pull_arm_revenue()  # optimize by revenue

        reward, _, done, opt_revenue = env.round(pulled_arm, user)

        ts_learner.update(pulled_arm, reward)
        optimal_revenues = np.append(optimal_revenues, opt_revenue)

    print(str(index) + ' has ended')

    return {'collected_rewards': ts_learner.collected_rewards, 'optimal_revenues': optimal_revenues}


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

    env = Env_4(initial_date=initial_date,
                n_days=n_days,
                users_per_day=avg_users_per_day,
                mutli_class_handler=mch,
                n_arms=n_arms)

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

    n_experiments = 10  # the number is small to do a raw test, otherwise set it to 1000
    rewards_per_experiment = []  # collect all the rewards achieved from the TS
    optimals_per_experiment = []  # collect all the optimals of the users generated
    args = [{'environment': copy.deepcopy(env), 'index': idx} for idx in
            range(n_experiments)]  # create arguments for the experiment

    with Pool(
            processes=8) as pool:  # make sure that 'processes' is less or equal than your actual number of logic cores
        results = pool.map(excecute_experiment, args, chunksize=1)

    for result in results:
        rewards_per_experiment.append(result['collected_rewards'])
        optimals_per_experiment.append(result['optimal_revenues'])

    # for opt_class_name, opt in mch.classes_opt.items():
    #     area = opt['price'] * opt['probability']
    #     plt.plot(np.cumsum(np.mean(area - rewards_per_experiment, axis=0)),
    #              label='Regret of the ' + opt_class_name.upper() + ' model')

    # Regret computed UN-knowing the class of the users
    area_aggregate = mch.aggregate_opt['price'] * mch.aggregate_opt['probability']
    plt.plot(np.cumsum(np.mean(area_aggregate - rewards_per_experiment, axis=0)),
             label='Regret of the aggregate model')

    # Below the regret computed knowing the optimal for each user
    plt.plot(np.cumsum(np.mean(optimals_per_experiment, axis=0) - np.mean(rewards_per_experiment, axis=0)),
             label='Regret of the true evaluation')

    plt.xlabel('Time')
    plt.ylabel('Regret')
    plt.legend()
    plt.show()
