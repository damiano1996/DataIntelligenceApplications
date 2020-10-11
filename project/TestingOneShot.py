import os
import sys
from datetime import datetime

from project.part_2.Testing_part2 import test_part2
from project.part_3.Testing_part3 import test_part3
from project.part_4.Testing_Env_4 import test_part4
from project.part_5.Testing_Env_5 import test_part5
from project.part_6.Testing_Env_6 import test_part6


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
    n_experiment = 10
    demand_curves_title = 'Demand Curves'
    demand_curves_chart_path = f'{charts_path}/demand_curves.png'
    # ---------------------------------------------------

    # PART 2
    print_('PART 2')
    test_part2(n_experiments=n_experiment,
               chart_path=f'{charts_path}/part2.png')
    print_(f'Test completed.\n'
           f'Time: {datetime.now()}\n')
    print_('-' * 60)
    # ---------------------------------------------------

    # PART 3
    print_('PART 3')
    test_part3(n_experiments=n_experiment,
               chart_path=f'{charts_path}/part3.png')
    print_(f'Test completed.\n'
           f'Time: {datetime.now()}\n')
    print_('-' * 60)
    # ---------------------------------------------------

    # PART 4
    print_('PART 4')
    keep_daily_price = False
    test_part4(n_experiments=n_experiment,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part4_keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 4 - Regret [keep_daily_price:{keep_daily_price}]')
    print_(f'First sub-test completed.\n'
           f'Time: {datetime.now()}\n')

    keep_daily_price = True
    test_part4(n_experiments=n_experiment,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part4_keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 4 - Regret [keep_daily_price:{keep_daily_price}]')
    print_(f'Second sub-test completed.\n'
           f'Time: {datetime.now()}\n')
    print_(f'Test completed.\n'
           f'Time: {datetime.now()}\n')
    print_('-' * 60)
    # ---------------------------------------------------

    # PART 5
    print_('PART 5')
    keep_daily_price = False
    test_part5(n_experiments=n_experiment,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part5_keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 5 - Regret [keep_daily_price:{keep_daily_price}]')
    print_(f'First sub-test completed.\n'
           f'Time: {datetime.now()}\n')

    keep_daily_price = True
    test_part5(n_experiments=n_experiment,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part5_keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 5 - Regret [keep_daily_price:{keep_daily_price}]')
    print_(f'Second sub-test completed.\n'
           f'Time: {datetime.now()}\n')
    print_(f'Test completed.\n'
           f'Time: {datetime.now()}\n')
    print_('-' * 60)
    # ---------------------------------------------------

    # PART 6
    print_('PART 6')
    enable_pricing = True
    keep_daily_price = True
    plot_advertising = True
    test_part6(n_experiments=n_experiment,
               enable_pricing=enable_pricing,
               plot_advertising=plot_advertising,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part6_'
                                  f'enable-pricing{enable_pricing}_'
                                  f'keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 6 - Regret ['
                                   f'enable_pricing:{enable_pricing} '
                                   f'keep_daily_price:{keep_daily_price}]',
               advertising_chart_root_path=f'{charts_path}/part6_')
    print_(f'First sub-test completed.\n'
           f'Time: {datetime.now()}\n')

    enable_pricing = False
    keep_daily_price = True
    plot_advertising = False
    test_part6(n_experiments=n_experiment,
               enable_pricing=enable_pricing,
               plot_advertising=plot_advertising,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part6_'
                                  f'enable-pricing{enable_pricing}_'
                                  f'keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 6 - Regret ['
                                   f'enable_pricing:{enable_pricing} '
                                   f'keep_daily_price:{keep_daily_price}]')
    print_(f'Second sub-test completed.\n'
           f'Time: {datetime.now()}\n')

    enable_pricing = False
    keep_daily_price = False
    test_part6(n_experiments=n_experiment,
               enable_pricing=enable_pricing,
               plot_advertising=plot_advertising,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part6_'
                                  f'enable-pricing{enable_pricing}_'
                                  f'keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 6 - Regret ['
                                   f'enable_pricing:{enable_pricing} '
                                   f'keep_daily_price:{keep_daily_price}]')
    print_(f'Third sub-test completed.\n'
           f'Time: {datetime.now()}\n')

    enable_pricing = True
    keep_daily_price = False
    test_part6(n_experiments=n_experiment,
               enable_pricing=enable_pricing,
               plot_advertising=plot_advertising,
               keep_daily_price=keep_daily_price,
               demand_chart_path=demand_curves_chart_path,
               demand_chart_title=demand_curves_title,
               results_chart_path=f'{charts_path}/part6_'
                                  f'enable-pricing{enable_pricing}_'
                                  f'keep-daily-price{keep_daily_price}.png',
               results_chart_title=f'Part 6 - Regret ['
                                   f'enable_pricing:{enable_pricing} '
                                   f'keep_daily_price:{keep_daily_price}]')
    print_(f'Fourth sub-test completed.\n'
           f'Time: {datetime.now()}\n')
    print_(f'Test completed.\n'
           f'Time: {datetime.now()}\n')
    print_('-' * 60)
