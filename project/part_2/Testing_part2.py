import numpy as np
import pandas as pd

from project.dia_pckg.plot_style.cb91visuals import *
from project.part_2.BiddingEnvironment import BiddingEnvironment
from project.part_2.GP_Learner import GP_Learner
from project.part_2.Optimizer import *
from project.dia_pckg.Config import *

# %%

np.random.seed(88)


# CLAIRVOYANT REWARD
def compute_Clairvoyant(bids, n_subcamp, env):
    all_optimal_subs = np.ndarray(shape=(0, len(bids)), dtype=float)
    for i in range(0, n_subcamp):
        all_optimal_subs = np.append(all_optimal_subs, np.atleast_2d(env.subs[i].bid(bids)), 0)

    print(f"Best bidding clairvoyant (arms, reward): {fit_table(all_optimal_subs)}")
    return fit_table(all_optimal_subs)[1]


# EXPLORATION PHASE
def exploration(total_click, learners, env):
    pulled = [0, 0, 0]
    pulled[0] = 9
    pulled[1] = 9
    pulled[2] = 9
    n_obs_exploration = 3

    clicks = env.round(pulled[0], pulled[1], pulled[2])

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

    print("Days used for exploration: ", n_obs_exploration)

    return n_obs_exploration, total_click


# EXPLOITATION PHASE
def exploitation(total_click, learners, env, n_obs_exploitation):
    print(f"running exploitation for {n_obs_exploitation} days")
    for i in range(0, n_obs_exploitation):

        table_all_Subs = np.ndarray(shape=(0, len(bids)), dtype=float)
        for l in learners:
            table_all_Subs = np.append(table_all_Subs, np.atleast_2d(l.means.T), 0)

        pulled = fit_table(table_all_Subs)[0]

        clicks = env.round(pulled[0], pulled[1], pulled[2])

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

    for s in range(0, len(learners)):
        learners[s].plot(env.subs[s].bid)

    print(f"Best bidding computed (arms, reward): {fit_table(table_all_Subs)}")

    return total_click


## Regret Computation
def plot_Regret(total_click, opt):
    # list of the collected reward
    rewards_per_experiment = []

    for i in range(0, n_obs_exploitation):
        num_clicks_day_i = total_click.values[i][3] \
                           + total_click.values[i][4] \
                           + total_click.values[i][5]
        rewards_per_experiment.append(num_clicks_day_i)

    plt.figure(0)
    plt.ylabel("Regret")
    plt.xlabel("t")
    plt.plot(np.cumsum(opt - rewards_per_experiment, axis=0), 'r')
    plt.show()

    print(f"total reward:{np.sum(rewards_per_experiment)}")
    print(f"average daily reward:{np.sum(rewards_per_experiment) / n_obs}")


if __name__ == '__main__':

    bids = np.linspace(0, max_bid, n_arms)
    print(f"arms: {bids}")

    total_click_each_day = pd.DataFrame(columns=['bid_sub1', 'bid_sub2', 'bid_sub3', "click1", "click2", "click3"])

    env = BiddingEnvironment(bids)

    learners = []
    # one learner for each sub campaign
    for i in range(0, n_subcamp):
        learners.append(GP_Learner(n_arms, bids))

    opt = compute_Clairvoyant(bids, n_subcamp, env)

    n_obs_exploration, total_click_each_day = exploration(total_click_each_day, learners, env)

    n_obs_exploitation = n_obs - n_obs_exploration

    total_click_each_day = exploitation(total_click_each_day, learners, env, n_obs_exploitation)
    plot_Regret(total_click_each_day, opt)
