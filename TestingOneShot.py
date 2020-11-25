"""
    Here we test all the parts of the project with different parameters configuration.
"""

import argparse
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
from project.part_7.Testing_Env_7 import test_part7


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action="store",
                        help='Number of part to start (2, 3, 4, 5, 6, 7_b or 7_n), type \'all\' to start them all',
                        dest="part", type=check_part, required=True)
    parser.add_argument('-e', action="store", help='Number of different experiment per part to perform',
                        dest="experiments", type=check_experiments, required=True)
    parser.add_argument('-s', action="store", help='Seed of experiments', dest="seed", type=check_experiments,
                        default='0')
    args = parser.parse_args()
    return build_setup(args)


def check_part(value):
    if value != "2" and value != "3" and value != "4" and value != "5" and value != "6" and value != "7_b" and value != "7_n" and value != "all":
        raise argparse.ArgumentTypeError("Invalid part argument")
    return value


def check_experiments(value):
    try:
        return int(value)
    except ValueError:
        argparse.ArgumentTypeError("Invalid number of experiments argument")


def build_setup(args):
    n_experiment = args.experiments
    seed = args.seed
    testing_setup = {
        'part2': True if args.part == "2" or args.part == "all" else False,
        'part3': True if args.part == "3" or args.part == "all" else False,
        'part4': True if args.part == "4" or args.part == "all" else False,
        'part5': True if args.part == "5" or args.part == "all" else False,
        'part6': True if args.part == "6" or args.part == "all" else False,
        'part7_binomial': True if args.part == "7_b" or args.part == "all" else False,
        'part7_normal': True if args.part == "7_n" or args.part == "all" else False,
    }
    return n_experiment, seed, testing_setup


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
    with open('project/dia_pckg/Config.py', 'r') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    n_experiment, seed, testing_setup = parse_arguments()
    np.random.seed(seed)

    dt_now = datetime.now()
    charts_path = os.path.join('project/results_charts', 'test_' + str(dt_now.strftime('%Y-%m-%d_%H-%M')))
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

        test_part3(n_experiments=n_experiment,
                   chart_path=f'{charts_path}/part3_regret.png',
                   title=f'Part 3 - Regret with {n_abrupts_phases} Abrupt Phases [min_len:{min_len} z_score:{z_score} window_length:{window_length}]',
                   win_length=window_length,
                   dl_change_detect_min_len=min_len,
                   dl_change_detect_test_stat=z_score)
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

        keep_daily_prices = [True, False]

        for keep_daily_price in keep_daily_prices:
            test_part6(n_experiments=n_experiment,
                       plot_advertising=True,
                       keep_daily_price=keep_daily_price,
                       demand_chart_path=demand_curves_chart_path,
                       demand_chart_title=demand_curves_title,
                       results_chart_path=f'{charts_path}/part6_'
                                          f'keep-daily-price{keep_daily_price}.png',
                       results_chart_title=f'Part 6 - Regret ['
                                           f'keep_daily_price:{keep_daily_price}]',
                       advertising_chart_root_path=f'{charts_path}/part6_'
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

        test_part7(n_experiments=n_experiment,
                   execution_type="binomial",
                   demand_chart_path=demand_curves_chart_path,
                   demand_chart_title=demand_curves_title,
                   results_chart_path=f'{charts_path}/part7_binomial.png',
                   results_chart_title=f'Part 7 ')

        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------

    if testing_setup['part7_normal']:
        # PART 7
        print_('PART 7 NORMAL')

        test_part7(n_experiments=n_experiment,
                   execution_type="normal",
                   demand_chart_path=demand_curves_chart_path,
                   demand_chart_title=demand_curves_title,
                   artificial_noise_ADV=artificial_noise_ADV,
                   artificial_noise_CR=artificial_noise_CR,
                   results_chart_path=f'{charts_path}/part7_normal_'
                                      f'ADV_noise{artificial_noise_ADV}_'
                                      f'CR_noise{artificial_noise_CR}.png',
                   results_chart_title=f'Part 7 ['
                                       f'ADV_noise:{artificial_noise_ADV} '
                                       f'CR_noise:{artificial_noise_CR}] ')
        print_(f'Sub-test completed.\n'
               f'Time: {datetime.now()}\n')

        print_(f'Test completed.\n'
               f'Time: {datetime.now()}\n')
        print_('-' * 60)
        # ---------------------------------------------------
