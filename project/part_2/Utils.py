import numpy as np

from project.dia_pckg.Utils import find_nearest


def get_idx_arm_from_allocation(allocation, bids, max_bid):
    # conversion from percentage to arm index
    allocation_bid = allocation * max_bid
    nearest_allocation = find_nearest(bids, allocation_bid)
    pulled_arm = np.where(bids == nearest_allocation)[0][0]
    return pulled_arm
