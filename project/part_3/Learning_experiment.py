import pandas as pd
import numpy as np
from project.part_2.Optimizer import fit_table


def execute_experiment(args):
    learner = args['learner']
    env = args['environment']
    bids = args['bids']
    n_arms = args['n_arms']
    n_subcamp = args['n_subcamp']
    n_obs = args['n_obs']
    print_span = args['print_span']

    env.reset()
    init_days = 1
    learners = []
    click_each_day = pd.DataFrame(columns=['bid_sub1', 'bid_sub2', 'bid_sub3', "click1", "click2", "click3"])

    for i in range(0, n_subcamp):
        learners.append(learner(n_arms, bids))

    # todo
    for d in range(0, n_obs):
        pulled = [0, 0, 0]
        # per i primi init_days giorni si pullano in modo causale, successivamente si usa la tabella
        if init_days > 0:  # or d % random_sampling == 0: #or d % int(len_window/2) == 0:
            init_days = init_days - 1
            first = d % 3
            pulled[first] = 9  # learners[first].pull_arm()
            pulled[(first + 1) % 3] = 9  # np.random.randint(0,n_arms - pulled[first])
            pulled[(first + 2) % 3] = 9  # n_arms - pulled[first] - pulled[(first + 1 )% 3] - 1
        else:
            # uso l'algoritmo della tabella per selezionare gli arm che mi danno un reward massimo
            table_all_Subs = np.ndarray(shape=(0, len(bids)), dtype=float)
            for l in learners:
                table_all_Subs = np.append(table_all_Subs, np.atleast_2d(l.means.T), 0)
            pulled = fit_table(table_all_Subs)[0]

        clicks = env.round(pulled[0], pulled[1], pulled[2])

        for x in range(0, n_subcamp):
            learners[x].update(pulled[x], clicks[x])

        click_each_day = click_each_day.append({
            'bid_sub1': pulled[0],
            'bid_sub2': pulled[1],
            'bid_sub3': pulled[2],
            "click1": clicks[0],
            "click2": clicks[1],
            "click3": clicks[2]
        }, ignore_index=True)

        if (d + 1) % print_span == 0:
            # TIME TO PRINT THE PLOTS
            print(f"DAY: {d}\nPULLED:{pulled}\nCLICKS: {clicks}\nTOT: {clicks.sum()}\n")

    return click_each_day
