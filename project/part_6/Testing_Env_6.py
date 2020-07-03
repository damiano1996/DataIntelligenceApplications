import sys
sys.path.append('C:\\Users\\Andrea\\Desktop\\DataIntelligenceApplications')

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
from project.part_5.CampaignScheduler import CampaignScheduler
from project.dia_pckg.Environment import Environment
from project.part_6.MultiSubCampaignHandler import MultiSubCampaignHandler

np.random.seed(0)
n_arms = 20


def excecute_experiment(args):
    index = args['index']
    env = args['environment']
    mch = args['multiclasshandler']

    handler = MultiSubCampaignHandler(mch)
    #Create and initialize budget allocator

    _ , done = env.reset()

    while not done:
        #Get the budget from budget allocator

        #Handler solve the advertising and pricing
        handler.update_all()

        #Handler return the regret of the day

        #Update the budget allocatore

        _, done = env.step()

    print(str(index) + ' has ended')

    #return The optimals and the collected rewards
    return None


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

    base_env = Environment(initial_date=initial_date, n_days=4)


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
    args = [{'environment': copy.deepcopy(base_env), 'index': idx, 'multiclasshandler': mch}
            for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(excecute_experiment, args, chunksize=1)

    for result in results:
        rewards_per_experiment.append(result['collected_rewards'])
        optimals_per_experiment.append(result['optimal_revenues'])



"""
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
    plt.show()

"""