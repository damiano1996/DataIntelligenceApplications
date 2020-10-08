import multiprocessing
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_2.GPTS_Learner import GPTS_Learner
from project.part_2.Learning_experiment import execute_experiment
from project.part_2.Utils import compute_clairvoyant

np.random.seed(0)

if __name__ == '__main__':
    bids = np.linspace(0, max_bid, n_arms)
    thread_x_l = 10
    args = []

    for i in range(thread_x_l):
        env_i = BiddingEnvironment(bids)
        args_i = {
            'learner': GPTS_Learner,
            'environment': env_i,
            'bids': bids,
            'n_subcamp': n_subcamp,
            'n_arms': n_arms,
            'n_obs': n_days,
            'print_span': print_span}
        args.append(args_i)

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(execute_experiment, args, chunksize=1)

    clicks_per_experiment = []
    opt_clicks_per_experiment = []
    for i, (click_each_day, args) in enumerate(results):
        clicks = np.sum(np.asarray(([click_each_day[f'click{j + 1}'] for j in range(3)])), axis=0)
        clicks_per_experiment.append(clicks)

        opt_clicks = compute_clairvoyant(args['environment'])[1]
        opt_clicks_per_experiment.append(np.asarray(opt_clicks))

    for clicks, opts in zip(clicks_per_experiment, opt_clicks_per_experiment):
        plt.plot(np.cumsum(opts - clicks), alpha=0.2, c='C2')

    plt.plot(np.cumsum(np.mean(opt_clicks_per_experiment) - np.mean(clicks_per_experiment, axis=0)),
             c='C2', label='Mean Regret')
    plt.ylabel('Regret')
    plt.xlabel('Time')
    plt.legend()
    plt.show()
