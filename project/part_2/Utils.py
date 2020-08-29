import numpy as np

from project.dia_pckg.Utils import find_nearest
from project.part_2.Optimizer import fit_table


# CLAIRVOYANT REWARD
def compute_clairvoyant(bids, n_subcampaigns, env, verbose=False):
    all_optimal_subs = np.ndarray(shape=(0, len(bids)), dtype=np.float32)
    for i in range(0, n_subcampaigns):
        all_optimal_subs = np.append(all_optimal_subs, np.atleast_2d(env.subs[i].bid(bids)), 0)

    if verbose:
        print(f"Best bidding clairvoyant (arms, reward): {fit_table(all_optimal_subs)}")
    return fit_table(all_optimal_subs)[1]


def get_idx_arm_from_allocation(allocation, bids, max_bid):
    # conversion from percentage to arm index
    allocation_bid = allocation * max_bid
    nearest_allocation = find_nearest(bids, allocation_bid)
    pulled_arm = np.where(bids == nearest_allocation)[0][0]
    return pulled_arm
