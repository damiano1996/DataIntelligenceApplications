import numpy as np

class TableAlgorithm(np):

    def fit_table(table_all_Subs):
        raws = table_all_Subs.shape[0]
        cols = table_all_Subs.shape[1]
        algorithm_table = np.ndarray(shape=(0, cols), dtype=float)

        for x in raws:
            algorithm_table = np.append(algorithm_table, np.atleast_2d(np.zeros(cols)), 0)

        algorithm_table[0, :] = table_all_Subs[0, :]

        allocations_table = [[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]]

        for i in range(1, raws):
            allocations_table.append([[], [], [], [], [], [], [], [], [], [], []])

            for j in range(0, cols):
                possibilities = np.array([])
                poss_allocation = []
                for p in range(0, j + 1):
                    # if bids[p] + bids[j-p] <= bids[j] :
                    possibilities = np.append(possibilities, table_all_Subs[i, p] + algorithm_table[i - 1, j - p])
                    poss_allocation.append(allocations_table[i - 1][j - p] + [p])
                    # print(str(i)+" "+ str(p) + " "+ str(j-p))

                max_index = np.argmax(possibilities)
                # print(poss_allocation)
                # print(possibilities)

                # print(max_index)
                algorithm_table[i, j] = possibilities[max_index]
                allocations_table[i][j] = poss_allocation[max_index]
        return allocations_table[raws-1][cols-1],max(algorithm_table[cols-1])
