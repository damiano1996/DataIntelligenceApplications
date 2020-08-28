from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.GP_Learner import GP_Learner as Learner
from project.part_2.Optimizer import fit_table
from project.part_3.AbruptBiddingEnvironment import AbruptBiddingEnvironment
from project.part_3.DynamicLearner import DynamicLearner
from project.part_3.Learning_experiment import execute_experiment

np.random.seed(8972)

if __name__ == '__main__':
    bids = np.linspace(0, max_bid, n_arms)
    env = AbruptBiddingEnvironment(bids)
    args1 = {}
    args1['learner'] = Learner
    args1['environment'] = env
    args1['bids'] = bids
    args1['n_subcamp'] = n_subcamp
    args1['n_arms'] = n_arms
    args1['n_obs'] = n_obs
    args1['print_span'] = print_span

    args2 = {}
    args2['learner'] = DynamicLearner
    args2['environment'] = env
    args2['bids'] = bids
    args2['n_subcamp'] = n_subcamp
    args2['n_arms'] = n_arms
    args2['n_obs'] = n_obs
    args2['print_span'] = print_span

    with Pool(2) as p:
        basic_total_click_each_day, sw_total_click_each_day = p.map(execute_experiment, [args1, args2])

    clicks_opt = np.array([])

    for p in range(0, n_phases):
        all_optimal_subs = np.ndarray(shape=(0, len(bids)), dtype=np.float32)
        for i in range(0, n_subcamp):
            all_optimal_subs = np.append(all_optimal_subs, np.atleast_2d(env.subs[i](bids, p)), 0)
        opt = fit_table(all_optimal_subs)[1]
        for days in range(0, phaselen):
            clicks_opt = np.append(clicks_opt, opt)

    sw_clicks_obtained = sw_total_click_each_day["click1"] + \
                         sw_total_click_each_day["click2"] + \
                         sw_total_click_each_day["click3"]

    basic_clicks_obtained = basic_total_click_each_day["click1"] + \
                            basic_total_click_each_day["click2"] + \
                            basic_total_click_each_day["click3"]

    np.cumsum(clicks_opt - sw_clicks_obtained).plot(label="Sliding window")
    np.cumsum(clicks_opt - basic_clicks_obtained).plot(label="Without sw")
    plt.legend(loc='lower right')
    plt.show()

    plt.show()

    print("SLIDING WINDOWS")
    print(np.sum(sw_clicks_obtained))

    print("\n\nWITHOUT SLIDING WINDOWS")
    print(np.sum(basic_clicks_obtained))
