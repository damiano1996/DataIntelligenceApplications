import numpy as np


class MultiClassHandler:

    def __init__(self, *classes):
        """
        :param classes: undefined number of Class objects
        """
        self.classes = classes  # list of class objects
        self.classes_opt = self.get_classes_optimals()  # dictionary of opts. The keys are the real name of the classes

        self.aggregate_demand_curve = self.get_aggregate_curve()
        self.aggregate_opt = self.get_optimal_price(self.aggregate_demand_curve)

    def get_aggregate_curve(self, phase='phase_0'):
        """
        :return: the aggregate curve
        """
        prices = self.classes[0].conv_rates[phase]['prices']

        stack = [class_.conv_rates[phase]['probabilities'] for class_ in self.classes]

        stack = np.stack(stack, axis=1)
        aggr_proba = np.mean(stack, axis=-1)
        return {'prices': prices, 'probabilities': aggr_proba}

    def get_classes_optimals(self, phase='phase_0'):
        """
        :return: (aggregate_optimal, class_1_optimal, class_2_optimal, class_3_optimal)
        """
        opts = {}
        for class_ in self.classes:
            opts[class_.name] = self.get_optimal_price(class_.conv_rates[phase])
        return opts

    def get_optimal_price(self, conv_rate):
        """
            This method computes the max area
        :param conv_rate: (price, probability)
        :return:
        """
        areas = conv_rate['prices'] * conv_rate['probabilities']
        idx = np.argmax(areas)
        return {'price': conv_rate['prices'][idx],
                'probability': conv_rate['probabilities'][idx]}

    def get_class(self, class_name):
        for class_ in self.classes:
            if class_name == class_.name:
                return class_

    def get_optimal(self, class_name):
        return self.classes_opt[class_name]
