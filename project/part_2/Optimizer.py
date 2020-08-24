import numpy as np


# Optimization problem:
# maximization of the number of clicks solved as a variation of the Multi-Choice Knapsack Problem

def fit_table(table_all_Subs):
    rows = table_all_Subs.shape[0]  # sub-campaigns
    cols = table_all_Subs.shape[1]  # budget allocations
    algorithm_table = np.ndarray(shape=(0, cols), dtype=float)

    # initialization
    for r in range(0, rows):
        algorithm_table = np.append(algorithm_table, np.atleast_2d(np.zeros(cols)), 0)

    # Initially we consider only the first sub-campaign
    # Successively we will expand the optimization problem by considering incrementally a new sub-campaign
    algorithm_table[0, :] = table_all_Subs[0, :]

    allocations_table = [[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]]

    # We are optimizing the budget allocation over the three sub-campaigns
    # in order to maximize the total number of clicks.
    for i in range(1, rows):
        allocations_table.append([[], [], [], [], [], [], [], [], [], [], []])

        for j in range(0, cols):
            possibilities = np.array([])
            poss_allocation = []
            for p in range(0, j + 1):
                possibilities = np.append(possibilities, table_all_Subs[i, p] + algorithm_table[i - 1, j - p])
                poss_allocation.append(allocations_table[i - 1][j - p] + [p])

            max_index = np.argmax(possibilities)

            algorithm_table[i, j] = possibilities[max_index]
            allocations_table[i][j] = poss_allocation[max_index]

    # the allocations_table contains the best budget allocation able to maximize the total number of clicks.
    return allocations_table[rows - 1][cols - 1], max(algorithm_table[rows - 1])
