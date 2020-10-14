import os
import sys
from datetime import datetime

from project.my_part_7.Testing_Env_7 import test_part7
from project.part_2.Testing_part2 import test_part2
from project.part_3.Testing_part3 import test_part3
from project.part_4.Testing_Env_4 import test_part4
from project.part_5.Testing_Env_5 import test_part5
from project.part_6.Testing_Env_6 import test_part6

n_experiment = 5

testing_setup = {
    'part2': True,
    'part3': True,
    'part4': True,
    'part5': True,
    'part6': True,
    'part7': True
}


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def print_(text):
    enable_print()
    print(text)
    with open(logs_path, "a") as file:
        file.write(text + '\n')
    block_print()


def read_configs():
    with open('dia_pckg/Config.py', 'r') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    dt_now = datetime.now()
    charts_path = os.path.join('results_charts', 'test_' + str(dt_now.strftime('%Y-%m-%d_%H-%M')))
    os.mkdir(charts_path)

    logs_path = os.path.join(charts_path, 'logs.txt')

    file = open(logs_path, 'w')
    file.close()

    print_(read_configs())
    print_('=' * 60)
    print_('Testing all parts!')
    print_(f'Time: {dt_now}')
    # ---------------------------------------------------
    demand_curves_title = 'Demand Curves'
    demand_curves_chart_path = f'{charts_path}/demand_curves.png'
    # ---------------------------------------------------

    if testing_setup['part2']:
        # PART 2
        print_('PART 2')
        test_part2(n_experiments=n_experiment,
                   chart_path=f'{charts_path}/part2.png')
        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------

    if testing_setup['part3']:
        # PART 3
        print_('PART 3')

        min_lens = [3, 7]
        test_stats = [2.5, 5]

        for min_len in min_lens:
            for test_stat in test_stats:
                test_part3(n_experiments=n_experiment,
                           chart_path=f'{charts_path}/part3_min-len{min_len}_test-stat{test_stat}.png',
                           title=f'Part 3 - Regret with Three Abrupt Phases [min_len:{min_len} test_stat:{test_stat}]',
                           dl_change_detect_min_len=min_len,
                           dl_change_detect_test_stat=test_stat)
                print_(f'Sub-test completed.\n'
                       f'Time: {datetime.now()}\n')
        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------

    if testing_setup['part4']:
        # PART 4
        print_('PART 4')

        keep_daily_prices = [False, True]

        for keep_daily_price in keep_daily_prices:
            test_part4(n_experiments=n_experiment,
                       keep_daily_price=keep_daily_price,
                       demand_chart_path=demand_curves_chart_path,
                       demand_chart_title=demand_curves_title,
                       results_chart_path=f'{charts_path}/part4_keep-daily-price{keep_daily_price}.png',
                       results_chart_title=f'Part 4 - Regret [keep_daily_price:{keep_daily_price}]')
            print_(f'Sub-test completed.\n'
                   f'Time: {datetime.now()}\n')
        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------

    if testing_setup['part5']:
        # PART 5
        print_('PART 5')

        keep_daily_prices = [False, True]

        for keep_daily_price in keep_daily_prices:
            test_part5(n_experiments=n_experiment,
                       keep_daily_price=keep_daily_price,
                       demand_chart_path=demand_curves_chart_path,
                       demand_chart_title=demand_curves_title,
                       results_chart_path=f'{charts_path}/part5_keep-daily-price{keep_daily_price}.png',
                       results_chart_title=f'Part 5 - Regret [keep_daily_price:{keep_daily_price}]')
            print_(f'Sub-test completed.\n'
                   f'Time: {datetime.now()}\n')

        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------

    if testing_setup['part6']:
        # PART 6
        print_('PART 6')

        enable_pricings = [True, False]
        keep_daily_prices = [True, False]

        for enable_pricing in enable_pricings:
            for keep_daily_price in keep_daily_prices:
                test_part6(n_experiments=n_experiment,
                           enable_pricing=enable_pricing,
                           plot_advertising=True,
                           keep_daily_price=keep_daily_price,
                           demand_chart_path=demand_curves_chart_path,
                           demand_chart_title=demand_curves_title,
                           results_chart_path=f'{charts_path}/part6_'
                                              f'enable-pricing{enable_pricing}_'
                                              f'keep-daily-price{keep_daily_price}.png',
                           results_chart_title=f'Part 6 - Regret ['
                                               f'enable_pricing:{enable_pricing} '
                                               f'keep_daily_price:{keep_daily_price}]',
                           advertising_chart_root_path=f'{charts_path}/part6_'
                                                       f'enable-pricing{enable_pricing}_'
                                                       f'keep-daily-price{keep_daily_price}_')
                print_(f'Sub-test completed.\n'
                       f'Time: {datetime.now()}\n')

        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------

    if testing_setup['part7']:
        # PART 7
        print_('PART 7')

        n_days_same_prices = [2, 3]
        enable_pricings = [True, False]

        for n_days_same_price in n_days_same_prices:
            for enable_pricing in enable_pricings:
                test_part7(n_experiments=n_experiment,
                           enable_pricing=enable_pricing,
                           plot_advertising=False,
                           n_days_same_price=n_days_same_price,
                           demand_chart_path=demand_curves_chart_path,
                           demand_chart_title=demand_curves_title,
                           results_chart_path=f'{charts_path}/part7_'
                                              f'enable-pricing{enable_pricing}_'
                                              f'n-days-same-price{n_days_same_price}.png',
                           results_chart_title=f'Part 7 - Regret ['
                                               f'enable_pricing:{enable_pricing} '
                                               f'n-days-same-price:{n_days_same_price}]',
                           advertising_chart_root_path=f'{charts_path}/part7_',
                           best_price_chart=f'{charts_path}/part7_best-prices_'
                                            f'enable-pricing:{enable_pricing}_'
                                            f'n-days-same-price{n_days_same_price}.png',
                           best_price_title='Part 7 - Best Candidate Price ['
                                            f'enable_pricing:{enable_pricing} '
                                            f'n-days-same-price:{n_days_same_price}]')
                print_(f'Sub-test completed.\n'
                       f'Time: {datetime.now()}\n')

        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------
