import multiprocessing
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.GPTS_Learner import GPTS_Learner as Learner
from project.part_2.Optimizer import fit_table
from project.part_3.AbruptBiddingEnvironment import AbruptBiddingEnvironment
from project.part_3.DLChangeDetect import DLChangeDetect
from project.part_3.DynamicLearner import DynamicLearner
from project.part_3.Learning_experiment import execute_experiment

np.random.seed(13337)

if __name__ == '__main__':
    bids = np.linspace(0, max_bid, n_arms)
    env = []
    thread_x_l = 5
    args = []
    learners_types = [Learner, DynamicLearner, DLChangeDetect]
    for i in range(thread_x_l):
        envi = AbruptBiddingEnvironment(bids)
        for l in learners_types:
            argsi = {}
            argsi['learner'] = l
            argsi['environment'] = envi
            argsi['bids'] = bids
            argsi['n_subcamp'] = n_subcamp
            argsi['n_arms'] = n_arms
            argsi['n_obs'] = n_obs
            argsi['print_span'] = print_span
            args.append(argsi)
        env.append(envi)

    with Pool(processes=multiprocessing.cpu_count()) as phase:
        results = phase.map(execute_experiment, args)

    learner_clicks_obtained = [results[0]["click1"] +
                               results[0]["click2"] +
                               results[0]["click3"],
                               results[1]["click1"] +
                               results[1]["click2"] +
                               results[1]["click3"],
                               results[2]["click1"] +
                               results[2]["click2"] +
                               results[2]["click3"]
                               ]

    for t in range(1, thread_x_l):
        for l in range(len(learners_types)):
            learner_clicks_obtained[l] = learner_clicks_obtained[l] + results[t + l]["click1"] + results[t + l][
                "click2"] + results[t + l]["click3"]

    clicks_opt = [0 for d in range(n_days)]
    for t in range(thread_x_l):
        day = 0
        for phase in range(0, n_phases):
            all_optimal_subs = np.ndarray(shape=(0, len(bids)), dtype=np.float32)
            for i in range(0, n_subcamp):
                all_optimal_subs = np.append(all_optimal_subs, np.atleast_2d(env[t].subs[i].means[f'phase_{phase}']), 0)
            opt = fit_table(all_optimal_subs)[1]
            for days in range(0, phaselen):
                clicks_opt[day] = clicks_opt[day] + opt
                day = day + 1
    clicks_opt = np.array(clicks_opt)
    print(clicks_opt)


    np.cumsum(clicks_opt - learner_clicks_obtained[0]).plot(label="Without SW")
    np.cumsum(clicks_opt - learner_clicks_obtained[1]).plot(label="Sliding Window")
    np.cumsum(clicks_opt - learner_clicks_obtained[2]).plot(label="Change Detect")

    plt.legend(loc='lower right')
    plt.show()

    plt.show()

    print("WITHOUT SLIDING WINDOWS")
    print(np.sum(learner_clicks_obtained[0]))

    print("\n\nSLIDING WINDOWS")
    print(np.sum(learner_clicks_obtained[1]))

    print("\n\nCHANGE DETECT")
    print(np.sum(learner_clicks_obtained[2]))
