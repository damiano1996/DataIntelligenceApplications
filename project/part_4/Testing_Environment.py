import copy
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np

from project.dia_pckg.Campaign import Campaign
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.User import User
from project.part_4.Env_4 import Env_4
from project.part_4.TS_Learner import TS_Learner

np.random.seed(23)
n_arms = 20


def excecute_experiment(args):
    index = args['index']
    env = args['environmnet']

    _, done = env.reset()
    ts_learner = TS_Learner(n_arms=n_arms, arm_prices=env.arm_prices['prices'])
    optimal_revenues = np.array([])

    while not done:
        # pulled_arm = ts_learner.pull_arm() #optimize by demand
        pulled_arm = ts_learner.pull_arm_revenue()  # optimize by revenue

        user = User(random=True)
        reward, _, done, opt_revenue = env.user_step(pulled_arm, user)

        ts_learner.update(pulled_arm, reward)
        optimal_revenues = np.append(optimal_revenues, opt_revenue)

    print(str(index) + 'has ended')

    return {'collected_rewards': ts_learner.collected_rewards, 'optimal_revenues': optimal_revenues}


if __name__ == '__main__':
    campaign = Campaign(max_budget=seller_max_budget, max_n_clicks=max_n_clicks)

    # one product to sell
    product = Product(product_config=product_config)

    # initialization of the three classes
    class_1 = Class(class_config=classes_config['elegant'], product=product, n_abrupt_phases=n_abrupts)
    class_2 = Class(class_config=classes_config['casual'], product=product, n_abrupt_phases=n_abrupts)
    class_3 = Class(class_config=classes_config['sports'], product=product, n_abrupt_phases=n_abrupts)

    env = Env_4(initial_date=initial_date,
                n_days=n_days,
                # users_per_day=avg_users_per_day,
                users_per_day=50,
                class_1=class_1,
                class_2=class_2,
                class_3=class_3,
                n_arms=n_arms)

    optimals = env.get_optimals()

    plt.plot(env.classes['class_1'].conv_rates['phase_0']['prices'],
             env.classes['class_1'].conv_rates['phase_0']['probabilities'], label=class_1.name, linestyle='--')
    plt.plot(env.classes['class_2'].conv_rates['phase_0']['prices'],
             env.classes['class_2'].conv_rates['phase_0']['probabilities'], label=class_2.name, linestyle='--')
    plt.plot(env.classes['class_3'].conv_rates['phase_0']['prices'],
             env.classes['class_3'].conv_rates['phase_0']['probabilities'], label=class_3.name, linestyle='--')
    plt.plot(env.aggregate_demand_curve['prices'],
             env.aggregate_demand_curve['probabilities'], label='aggregate')

    plt.scatter(optimals['class_1']['price'],
                optimals['class_1']['probability'], marker='o', label=f'opt {class_1.name}')
    plt.scatter(optimals['class_2']['price'],
                optimals['class_2']['probability'], marker='o', label=f'opt {class_2.name}')
    plt.scatter(optimals['class_3']['price'],
                optimals['class_3']['probability'], marker='o', label=f'opt {class_3.name}')
    plt.scatter(optimals['aggregate']['price'],
                optimals['aggregate']['probability'], marker='o', label='opt aggregate')

    plt.xlabel('Price')
    plt.ylabel('Conversion Rate')
    plt.legend()
    plt.show()

    n_experiments = 200  # the number is small to do a raw test, otherwise set it to 1000
    rewards_per_experiment = []  # collect all the rewards achieved from the TS
    optimals_per_experiment = []  # collect all the optimals of the users generated
    args = [{'environmnet': copy.deepcopy(env), 'index': idx} for idx in
            range(n_experiments)]  # create arguments for the experiment

    with Pool(
            processes=8) as pool:  # make sure that 'processes' is less or equal than your actual number of logic cores
        results = pool.map(excecute_experiment, args, chunksize=1)

    for result in results:
        rewards_per_experiment.append(result['collected_rewards'])
        optimals_per_experiment.append(result['optimal_revenues'])

    aggregate_opt = optimals['aggregate']['price'] * optimals['aggregate']['probability']
    class1_opt = optimals['class_1']['price'] * optimals['class_1']['probability']
    class2_opt = optimals['class_2']['price'] * optimals['class_2']['probability']
    class3_opt = optimals['class_3']['price'] * optimals['class_3']['probability']

    plt.plot(np.cumsum(np.mean(class1_opt - rewards_per_experiment, axis=0)),
             label='Regret of the ' + class_1.name + ' model')
    plt.plot(np.cumsum(np.mean(class2_opt - rewards_per_experiment, axis=0)),
             label='Regret of the ' + class_2.name + ' model')
    plt.plot(np.cumsum(np.mean(class3_opt - rewards_per_experiment, axis=0)),
             label='Regret of the ' + class_3.name + ' model')
    plt.plot(np.cumsum(np.mean(aggregate_opt - rewards_per_experiment, axis=0)), label='Regret of the aggregate model')
    plt.plot(np.cumsum(np.mean(optimals_per_experiment, axis=0) - np.mean(rewards_per_experiment, axis=0)),
             label='Regret of the true evaluation')

    plt.xlabel('Time')
    plt.ylabel('Regret')
    plt.legend()
    plt.show()

# test over 200 experiments with 17500 epochs
# 3:46 1_core (default)
# 0:43 8_core
