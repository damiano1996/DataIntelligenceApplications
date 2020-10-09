import copy
import multiprocessing
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Campaign import Campaign
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.User import User
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_4.SWTS_Learner import SWTS_Learner
from project.part_5.CampaignScheduler_5 import CampaignScheduler_5
from project.part_5.Env_5 import Env_5

np.random.seed(0)
n_arms = 20


def execute_experiment(args):
    index = args['index']
    env = args['environment']
    campaign_scheduler = args['campaign_scheduler']

    new_week, (_, done) = env.reset()
    campaign_scheduler.reset()
    optimal_revenues = np.array([])

    while not done:
        if new_week:  # in this case we can generate new contexts and new learners
            campaign_scheduler.context_update()

        user = User(random=True)

        pulled_arm = campaign_scheduler.pull_arm_from_user(user)

        new_week, reward, current_date, done, opt_revenue = env.round(pulled_arm, user)

        campaign_scheduler.update(user, pulled_arm, reward)
        optimal_revenues = np.append(optimal_revenues, opt_revenue)

    print(str(index) + ' has ended')

    return {'collected_rewards': campaign_scheduler.collected_rewards, 'optimal_revenues': optimal_revenues}


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

    env = Env_5(initial_date=initial_date,
                n_days=n_days,
                users_per_day=avg_users_per_day,
                multi_class_handler=mch,
                n_arms=n_arms)

    campaign_scheduler = CampaignScheduler_5(mch, SWTS_Learner, n_arms, env.arm_prices['prices'], 5000)

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
    rewards_per_experiment = []  # collect all the rewards achieved from the TS
    optimals_per_experiment = []  # collect all the optimals of the users generated
    args = [{'environment': copy.deepcopy(env), 'campaign_scheduler': copy.deepcopy(campaign_scheduler), 'index': idx}
            for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(execute_experiment, args, chunksize=1)

    for result in results:
        rewards_per_experiment.append(result['collected_rewards'])
        optimals_per_experiment.append(result['optimal_revenues'])

    # to plot every 7 days a vertical line
    # note: the lines may not match with the generation of a new context since the generation depends by the week day
    idx = np.arange(0, int(n_days * avg_users_per_day), int(7 * avg_users_per_day))
    for i in idx:
        plt.axvline(i, 0, 1, alpha=0.1, color='k')

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
    plt.savefig('other_files/testing_part5.png')
    plt.show()
