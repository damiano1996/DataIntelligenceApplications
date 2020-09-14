import numpy as np
import pandas as pd

from project.dia_pckg.Config import *
from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_2.GPTS_Learner import GPTS_Learner
from project.part_2.Optimizer import fit_table
from project.part_2.Utils import get_idx_arm_from_allocation, compute_clairvoyant

np.random.seed(0)


def initialization(total_click, learners, env):
    pulled = [n_arms - 1, n_arms - 1, n_arms - 1]
    clicks = env.round(pulled)

    for x in range(0, n_subcamp):
        learners[x].update(pulled[x], clicks[x])

    total_click = total_click.append({
        'bid_sub1': pulled[0],
        'bid_sub2': 0,
        'bid_sub3': 0,
        "click1": clicks[0],
        "click2": 0,
        "click3": 0
    }, ignore_index=True)
    total_click = total_click.append({
        'bid_sub1': 0,
        'bid_sub2': pulled[1],
        'bid_sub3': 0,
        "click1": 0,
        "click2": clicks[1],
        "click3": 0
    }, ignore_index=True)
    total_click = total_click.append({
        'bid_sub1': 0,
        'bid_sub2': 0,
        'bid_sub3': pulled[2],
        "click1": 0,
        "click2": 0,
        "click3": clicks[2]
    }, ignore_index=True)

    return total_click


def running(total_click, learners, env, n_obs_exploitation):
    print(f"running exploitation for {n_obs_exploitation} days")
    for i in range(0, n_obs_exploitation):

        table_all_subs = np.ndarray(shape=(0, len(bids)), dtype=np.float32)
        for l in learners:
            table_all_subs = np.append(table_all_subs, np.atleast_2d(l.means.T), 0)

        allocations = fit_table(table_all_subs)[0]
        # conversion to arm index
        pulled = [get_idx_arm_from_allocation(allocation, bids) for allocation in allocations]

        clicks = env.round(pulled)

        for x in range(0, n_subcamp):
            learners[x].update(pulled[x], clicks[x])
        total_click = total_click.append({
            'bid_sub1': pulled[0],
            'bid_sub2': pulled[1],
            'bid_sub3': pulled[2],
            "click1": clicks[0],
            "click2": clicks[1],
            "click3": clicks[2]
        }, ignore_index=True)

    for i in range(0, len(learners)):
        learners[i].plot(env.subs[i].phase_curve(bids))

    print(f"Best bidding computed (arms, reward): {fit_table(table_all_subs)}")

    return total_click


## Regret Computation
def plot_regret(total_click, opt):
    # list of the collected reward
    rewards_per_experiment = []

    for i in range(0, n_obs):
        num_clicks_day_i = total_click.values[i][3] \
                           + total_click.values[i][4] \
                           + total_click.values[i][5]
        rewards_per_experiment.append(num_clicks_day_i)

    plt.figure(0)
    plt.ylabel("Regret")
    plt.xlabel("t")
    plt.plot(np.cumsum(opt - rewards_per_experiment, axis=0))
    plt.show()

    print(f"total reward: {np.sum(rewards_per_experiment)}")
    print(f"average daily reward: {np.sum(rewards_per_experiment) / n_obs}")


if __name__ == '__main__':

    bids = np.linspace(0, max_bid, n_arms)
    print(f"arms: {bids}")

    total_click_each_day = pd.DataFrame(columns=['bid_sub1', 'bid_sub2', 'bid_sub3', "click1", "click2", "click3"])

    env = BiddingEnvironment(bids)

    learners = []
    # one learner for each sub campaign
    for i in range(0, n_subcamp):
        learners.append(GPTS_Learner(n_arms, bids))

    opt = compute_clairvoyant(env, verbose=True)[1]

    total_click_each_day = initialization(total_click_each_day, learners, env)

    total_click_each_day = running(total_click_each_day, learners, env, n_obs)
    plot_regret(total_click_each_day, opt)
