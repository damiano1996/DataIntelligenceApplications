import os

import matplotlib.pyplot as plt
from matplotlib.figure import figaspect

from project.dia_pckg.Config import features_space, demand_path
from project.dia_pckg.FunctionDesigner import load_function, design_function, save_function
from project.dia_pckg.Utils import check_if_dir_exists, check_if_file_exists


class Class:

    def __init__(self, class_name, class_config, product, n_abrupt_phases, summary=True):
        """
        :param class_name: name of the class
        :param class_features: binary features of the class
        :param product: Product object
        :param n_abrupt_phases: number of abrupt phases
        :param summary: boolean to print the summary of the information of the class
        """
        self.name = class_name
        self.features = class_config['features']

        self.product = product
        self.n_abrupt_phases = n_abrupt_phases

        # here we generate one conversion curve for each phase
        self.conv_rate_phases()

        if summary:
            self.print_summary()

    def conv_rate_phases(self):
        """
            Creating dictionary to store the abrupt phases
        :return:
        """
        self.conv_rates = {}
        for phase_i in range(self.n_abrupt_phases):
            phase_name = f'phase_{phase_i}'
            self.conv_rates[phase_name] = self.load_or_design_function(self.name, phase_name)

    def get_filename(self, class_name, phase):
        return f'{class_name}_{phase}.npy'

    def load_or_design_function(self, class_name, phase):
        """
            load data from directory if available, otherwise you have to design the function
        :param class_name:
        :param phase:
        :return:
        """
        check_if_dir_exists(demand_path, create=True)
        fname = self.get_filename(class_name, phase)
        path_file = os.path.join(demand_path, fname)
        exists = check_if_file_exists(path_file, create=False)
        if exists:
            x, y = load_function(path_file)
        else:
            print(f'Draw for: {class_name.upper()} - {phase}')
            x, y = design_function(x_interval=[self.product.base_price, self.product.max_price],
                                   y_interval=[0, 1],  # probability
                                   density=1,
                                   poly_apprx=True,
                                   rank=10,
                                   plot_result=True)
            save_function(x, y, path_file)
        return {'prices': x, 'probabilities': y}

    def plot_conversion_rate(self):
        """
            This function plots the curves of the different abrupt phases
        :return:
        """
        w, h = figaspect(0.2)

        fig, axs = plt.subplots(1, self.n_abrupt_phases, figsize=(w, h))
        fig.suptitle(f'Conversion Curves - Class name: {self.name}', y=1.)

        for phase_i, conv_rate in enumerate(self.conv_rates.values()):
            axs[phase_i].set_title(f'Phase: {phase_i}')
            axs[phase_i].set_ylim(0, 1)
            axs[phase_i].plot(conv_rate['prices'],
                              conv_rate['probabilities'])
            axs[phase_i].set_xlabel('Price')
            axs[phase_i].set_ylabel('Conversion Rate')

        fig.show()

    def print_summary(self):
        """
            This function prints a summary of this class
        :return:
        """
        features_meaning = []
        for i, bin in enumerate(self.features):
            feat_value = features_space[list(features_space.keys())[i]][bin]
            features_meaning.append(feat_value)

        summary = f'---------------------------------\n' \
                  f'Class name: {self.name}\n' \
                  f'Feature values: {features_meaning}\n' \
                  f'Number of abrupt phases: {self.n_abrupt_phases}\n' \
                  f'---------------------------------\n'
        print(summary)
