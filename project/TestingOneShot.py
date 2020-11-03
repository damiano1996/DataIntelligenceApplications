import os
import sys
from datetime import datetime
import numpy as np

from project.dia_pckg.Config import *
from project.part_2.Testing_part2 import test_part2
from project.part_3.Testing_part3 import test_part3
from project.part_4.Testing_Env_4 import test_part4
from project.part_5.Testing_Env_5 import test_part5
from project.part_6.Testing_Env_6 import test_part6
from project.part_7.Testing_Env_7 import test_part7 as t7_binomial
from project.part_7_normal.Testing_Env_7 import test_part7 as t7_normal

n_experiment = 15
np.random.seed(0)

testing_setup = {
    'part2': False,
    'part3': False,
    'part4': False,
    'part5': False,
    'part6': False,
    'part7_binomial': True,
    'part7_normal': True

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
    # block_print()


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

        for min_len in min_lens:
            for lw in multiple_len_window:
                test_part3(n_experiments=n_experiment,
                           chart_path=f'{charts_path}/part3_min-len{min_len}_z_score{z_score}.png',
                           title=f'Part 3 - Regret with {n_abrupts_phases} Abrupt Phases [min_len:{min_len} z_score:{z_score} window_length:{lw}]',
                           win_length=lw,
                           dl_change_detect_min_len=min_len,
                           dl_change_detect_test_stat=z_score)
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

    if testing_setup['part7_binomial']:
        # PART 7
        print_('PART 7 BINOMIAL')

        artificial_noise_ADVs = [0.0, 0.02, 0.05, 0.1]

        for artificial_noise_ADV in artificial_noise_ADVs:
            t7_binomial(n_experiments=n_experiment,
                        execution_type="binomial",
                        demand_chart_path=demand_curves_chart_path,
                        demand_chart_title=demand_curves_title,
                        artificial_noise_ADV=artificial_noise_ADV,
                        results_chart_path=f'{charts_path}/part7_binomial_'
                                           f'ADV_noise{artificial_noise_ADV}_.png',
                        results_chart_title=f'Part 7 ['
                                            f'ADV_noise:{artificial_noise_ADV}] ')
            print_(f'Sub-test completed.\n'
                   f'Time: {datetime.now()}\n')

        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------

        if testing_setup['part7_normal']:
            # PART 7
            print_('PART 7 NORMAL')

            artificial_noise_ADVs = [0.0, 0.02, 0.05]
            artificial_noise_CRs = [0.0, 0.02, 0.05]

            for artificial_noise_ADV in artificial_noise_ADVs:
                for artificial_noise_CR in artificial_noise_CRs:
                    t7_normal(n_experiments=n_experiment,
                              execution_type="normal",
                              demand_chart_path=demand_curves_chart_path,
                              demand_chart_title=demand_curves_title,
                              artificial_noise_ADV=artificial_noise_ADV,
                              artificial_noise_CR=artificial_noise_CR,
                              results_chart_path=f'{charts_path}/part7_normal_'
                                                 f'artificial-noise-ADV{artificial_noise_ADV}_'
                                                 f'artificial-noise-CR{artificial_noise_CR}.png',
                              results_chart_title=f'Part 7 ['
                                                  f'ADV_noise:{artificial_noise_ADV} '
                                                  f'CR_noise:{artificial_noise_CR}] ')
                    print_(f'Sub-test completed.\n'
                           f'Time: {datetime.now()}\n')

            print_(f'Test completed.\n'
                   f'Time: {datetime.now()}\n')
            print_('-' * 60)
            # ---------------------------------------------------
