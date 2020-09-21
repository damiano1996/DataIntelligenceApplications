import numpy as np
import pandas as pd
import multiprocessing
from multiprocessing import Pool
from project.dia_pckg.Config import *
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_2.GPTS_Learner import GPTS_Learner
from project.part_2.Optimizer import fit_table
from project.part_2.Utils import get_idx_arm_from_allocation, compute_clairvoyant
from project.part_3.Learning_experiment import execute_experiment


np.random.seed(13337)

if __name__ == '__main__':
    bids = np.linspace(0, max_bid, n_arms)
    env = []
    thread_x_l = 5
    args = []

    for i in range(thread_x_l):
        envi = BiddingEnvironment(bids)
        argsi = {}
        argsi['learner'] = GPTS_Learner
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

    learner_clicks_obtained = np.array([0 for i in range(n_days)])
    for t in range(1, thread_x_l):
        learner_clicks_obtained = learner_clicks_obtained + results[t]["click1"] + results[t][
                "click2"] + results[t]["click3"]

    clicks_opt = np.array([0 for d in range(n_days)])
    for t in range(thread_x_l):

        clicks_opt = clicks_opt + compute_clairvoyant(env[t], verbose=True)[1]





    np.cumsum(clicks_opt - learner_clicks_obtained).plot(label="CUMSUM REGRET")

    plt.legend(loc='lower right')
    plt.show()

    plt.show()

    print("TOTAL CLICKS")
    print(np.sum(learner_clicks_obtained[0]))