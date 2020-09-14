import numpy as np

from project.dia_pckg.Utils import find_nearest
from project.part_2.Optimizer import fit_table


# CLAIRVOYANT REWARD
def compute_clairvoyant(env, phase=0, verbose=False):
    all_optimal_subs = np.ndarray(shape=(0, len(env.bids)), dtype=np.float32)
    for i in range(0, len(env.subs)):
        all_optimal_subs = np.append(all_optimal_subs,
                                     np.atleast_2d(env.subs[i].means[f'phase_{phase}']), 0)

    best_allocation, n_clicks = fit_table(all_optimal_subs)

    if verbose:
        print(f"Best bidding clairvoyant (best_allocation, n_clicks): {best_allocation}, {n_clicks}")
    return best_allocation, n_clicks


def get_idx_arm_from_allocation(allocation, bids):
    # conversion from percentage to arm index
    allocation_bid = allocation * bids[-1]
    nearest_allocation = find_nearest(bids, allocation_bid)
    pulled_arm = np.where(bids == nearest_allocation)[0][0]
    return int(pulled_arm)
