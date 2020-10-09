import copy
import multiprocessing
from multiprocessing import Pool

import numpy as np

from project.dia_pckg.Config import *
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.GPTS_Learner import GPTS_Learner as Learner
from project.part_2.Learning_experiment import execute_experiment
from project.part_2.Utils import compute_clairvoyant
from project.part_3.AbruptBiddingEnvironment import AbruptBiddingEnvironment
from project.part_3.DLChangeDetect import DLChangeDetect
from project.part_3.DynamicLearner import DynamicLearner

np.random.seed(0)

if __name__ == '__main__':
    bids = np.linspace(0, max_bid, n_arms)
    thread_x_l = 10
    args = []
    learners_types = [Learner, DynamicLearner, DLChangeDetect]
    for i in range(thread_x_l):
        env_i = AbruptBiddingEnvironment(bids)
        for learner in learners_types:
            args_i = {
                'learner': learner,
                'environment': copy.deepcopy(env_i),
                'bids': bids,
                'n_subcamp': n_subcamp,
                'n_arms': n_arms,
                'n_obs': n_days,
                'print_span': print_span}
            args.append(args_i)

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(execute_experiment, args, chunksize=1)

    clicks_per_experiments = {}
    opt_clicks_per_experiments = {}
    for i, (click_each_day, args) in enumerate(results):
        # for each result we get the name of the used learner
        learner_name = args['learner'].__name__

        clicks = np.sum(np.asarray(([click_each_day[f'click{j + 1}'] for j in range(3)])), axis=0)
        # adding to the dictionary
        # if the dictionary already contains the given key, we can append it
        # otherwise we have to initialize the array
        if learner_name in list(clicks_per_experiments.keys()):
            clicks_per_experiments[learner_name].append(clicks)
        else:
            clicks_per_experiments[learner_name] = [clicks]

        # the optimal number of clicks depends by the phase, thus we have to compute the optimal for each phase
        opt_clicks = np.arange(0, n_days, 1)
        for phase in range(n_abrupts_phases):
            opt_phase_clicks = compute_clairvoyant(args['environment'], phase=phase)[1]
            opt_clicks[int(phase * phase_len):int((phase + 1) * phase_len)] = opt_phase_clicks
        # adding to dictionary
        if learner_name in list(opt_clicks_per_experiments.keys()):
            opt_clicks_per_experiments[learner_name].append(opt_clicks)
        else:
            opt_clicks_per_experiments[learner_name] = [opt_clicks]

    # plot
    for i, ((learner_name, clicks_per_experiment), (opt_clicks_per_experiment)) in enumerate(
            zip(clicks_per_experiments.items(), opt_clicks_per_experiments.values())):

        for clicks, opts in zip(clicks_per_experiment, opt_clicks_per_experiment):
            plt.plot(np.cumsum(opts - clicks), alpha=0.2, c=f'C{i + 1}')

        plt.plot(np.cumsum(np.mean(opt_clicks_per_experiment, axis=0) - np.mean(clicks_per_experiment, axis=0)),
                 c=f'C{i + 1}', label=f'{learner_name} - Mean Regret')

    plt.ylabel('Regret')
    plt.xlabel('Time')
    plt.legend()
    plt.savefig('other_files/testing_part3.png')
    plt.show()
