import numpy as np


def fit_table(table_all_subs):
    rows, cols = table_all_subs.shape

    algorithm_table = np.zeros(shape=table_all_subs.shape)
    algorithm_table[0, :] = table_all_subs[0, :]

    allocations_table = [[[i] for i in range(cols)]]

    for i in range(1, rows):
        empty = [[] for i in range(cols)]
        allocations_table.append(empty)

        for j in range(0, cols):
            possibilities = np.array([])
            poss_allocation = []
            for p in range(0, j + 1):
                possibilities = np.append(possibilities, table_all_subs[i, p] + algorithm_table[i - 1, j - p])
                poss_allocation.append(allocations_table[i - 1][j - p] + [p])

            max_index = np.argmax(possibilities)

            algorithm_table[i, j] = possibilities[max_index]
            allocations_table[i][j] = poss_allocation[max_index]

    best_allocation = allocations_table[rows - 1][cols - 1]
    best_allocation = [cell / (cols - 1) for cell in best_allocation]

    return best_allocation, np.max(algorithm_table[rows - 1])
