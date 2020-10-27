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


def test_part3(n_experiments=3,
               chart_path='other_files/testing_part3.png',
               title='Part 3 - Regret with Three Abrupt Phases',
               dl_change_detect_min_len=3,
               dl_change_detect_test_stat=3):
    np.random.seed(0)

    bids = np.linspace(0, max_bid, n_arms_advertising)
    args = []

    # learners_types = [Learner, DynamicLearner, DLChangeDetect]
    # learners_types = [DynamicLearner, DLChangeDetect, Learner]
    learners_types = [DLChangeDetect, Learner, DynamicLearner]
    for i in range(n_experiments):
        env_i = AbruptBiddingEnvironment(bids)
        for learner in learners_types:
            args_i = {
                'learner': learner,
                'environment': copy.deepcopy(env_i),
                'bids': bids,
                'n_subcamp': n_subcamp,
                'n_arms': n_arms_advertising,
                'n_obs': n_days,
                'dl_change_detect_min_len': dl_change_detect_min_len,
                'dl_change_detect_test_stat': dl_change_detect_test_stat
            }
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

    ylim = 0
    plt.title(title, fontsize=14)
    # plot
    for i, ((learner_name, clicks_per_experiment), (opt_clicks_per_experiment)) in enumerate(
            zip(clicks_per_experiments.items(), opt_clicks_per_experiments.values())):

        for clicks, opts in zip(clicks_per_experiment, opt_clicks_per_experiment):
            plt.plot(np.cumsum(opts - clicks), alpha=0.2, c=f'C{i + 1}')

        curve = np.cumsum(np.mean(opt_clicks_per_experiment, axis=0) - np.mean(clicks_per_experiment, axis=0))
        ylim = curve[-1] if curve[-1] > ylim else ylim
        plt.plot(curve, c=f'C{i + 1}', label=f'{learner_name} - Mean Regret')

    plt.ylabel('Regret')
    plt.xlabel('Time')
    plt.legend()
    plt.ylim([0, ylim])

    plt.savefig(chart_path)
    plt.show()


if __name__ == '__main__':
    min_lens = [1, 2, 3, 4, 5]
    #test_stats = [2.5, 3, 4, 5]
    test_stat = 2.58

    for min_len in min_lens:
        #for test_stat in test_stats:
        test_part3(n_experiments=10,
                   chart_path=f'other_files/part3_min-len{min_len}_test-stat{test_stat}.png',
                   title=f'Part 3 - Regret with Three Abrupt Phases [min_len:{min_len} test_stat:{test_stat}]',
                   dl_change_detect_min_len=min_len,
                   dl_change_detect_test_stat=test_stat)
