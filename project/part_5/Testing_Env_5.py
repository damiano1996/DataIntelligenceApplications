import copy
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.User import User
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_4.MultiClassHandler import MultiClassHandler
from project.part_4.SWTS_Learner import SWTS_Learner
from project.part_5.CampaignScheduler import CampaignScheduler
from project.part_5.Env_5 import Env_5


def test_part5(n_experiments=10,
               keep_daily_price=True,
               demand_chart_path='other_files/testing_part5_demandcurves.png',
               demand_chart_title='Part 5 - Demand Curves',
               results_chart_path='other_files/testing_part5_regrets.png',
               results_chart_title='Part 5 - Regret'):
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

    env = Env_5(initial_date=initial_date,
                n_days=n_days,
                users_per_day=avg_users_per_day,
                multi_class_handler=mch,
                n_arms=n_arms_pricing)

    campaign_scheduler = CampaignScheduler(mch, SWTS_Learner, n_arms_pricing, env.arm_prices['prices'], 5000)

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
    args = [{'environment': copy.deepcopy(env), 'campaign_scheduler': copy.deepcopy(campaign_scheduler), 'index': idx,
             'keep_daily_price': keep_daily_price}
            for idx in range(n_experiments)]  # create arguments for the experiment

    with Pool(processes=1) as pool:  # multiprocessing.cpu_count()
        results = pool.map(execute_experiment, args, chunksize=1)

    for result in results:
        rewards_per_experiment.append(result['collected_rewards'])
        optimals_per_experiment.append(result['optimal_revenues'])

    # to plot every 7 days a vertical line
    # note: the lines may not match with the generation of a new context since the generation depends by the week day
    idx = np.arange(0, int(n_days * avg_users_per_day), int(7 * avg_users_per_day))
    for i in idx:
        plt.axvline(i, 0, 1, alpha=0.1, color='k')

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
    campaign_scheduler = args['campaign_scheduler']
    keep_daily_price = args['keep_daily_price']

    new_week, (_, done) = env.reset()
    campaign_scheduler.reset()
    optimal_revenues = np.array([])

    new_day = True
    while not done:
        if new_week:  # in this case we can generate new contexts and new learners
            campaign_scheduler.context_update()

        user = User(random=True)

        pulled_arm = campaign_scheduler.pull_arm_from_user(user, keep_daily_price, new_day)

        new_week, reward, current_date, new_day, done, opt_revenue = env.round(pulled_arm, user)
        campaign_scheduler.update(user, pulled_arm, reward)
        optimal_revenues = np.append(optimal_revenues, opt_revenue)

    print(str(index) + ' has ended')

    return {'collected_rewards': campaign_scheduler.collected_rewards, 'optimal_revenues': optimal_revenues}


if __name__ == '__main__':
    test_part5()
