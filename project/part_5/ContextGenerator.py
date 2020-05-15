from project.part_5.Context import Context
import math
import numpy as np


class ContextGenerator:

    def __init__(self, class_1, class_2, class_3, feature_1, feature_2, multi_class_handler, mab_algorithm, mab_args):
        """

        :param class_1: class object
        :param class_2: class object
        :param class_3: class object
        """
        self.classes = {class_1.features: class_1, class_2.features: class_2, class_3.features: class_3, }
        self.features = {feature_1, feature_2}
        self.mab_algorithm = mab_algorithm
        self.mab_args = mab_args
        self.mch = multi_class_handler
        pass

    def get_weekly_contexts(self, users, contexts, sales):
        """
        :param users: dictionary of class->number of users, they are users collected from the beginning of the campaign
        :param contexts: the list of contexts used in the previous iteration
        :param sales: dictionary class->sold items during the week
        :return: dictionary of the following shape:
                {'context_1': features, 'context_2': features, ...}
                    where features is a list containing the features of the context: e.g. ['<30', 'worker]
        """
        if contexts.len() == 0:
            #create aggregate context
            new_contexts = {'context_1': Context(classes=self.classes, feature='aggregate', context_name='aggregate',
                                                 mch=self.mch, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)}
        elif contexts.len() == 1:
            cont = {}
            not_cont = {}
            low_bound = {}
            for feature in self.features:
                cont[feature], not_cont[feature] = self.split(feature, contexts['context_1'])
                low_bound[feature] = self.get_low_bound(cont, not_cont, users, sales)
            best_feature = np.argmax(low_bound)
            if low_bound[best_feature] > self.get_low_bound(contexts['context_1'].classes, [], users, sales):
                #split
                new_contexts = {
                    'context_1': Context(classes=cont[best_feature], feature=best_feature, context_name='giuseppe',
                                         mch=self.mch, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args),
                    'context_2': Context(classes=not_cont[best_feature], feature=best_feature, context_name='giuseppe',
                                         mch=self.mch, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)}
            else:
                #no split
                new_contexts = {'context_1': Context(classes=contexts['context_1'].classes,
                                                     feature=contexts['context_1'].feature,
                                                     context_name=contexts['context_1'].context_name,
                                                     mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)}

        elif contexts.len() == 2:
            if contexts['context_1'].feature == 'age':
                cont, not_cont = self.split('profession', contexts['context_1'])
                feature = 'profession'
                low_bound = self.get_low_bound(cont, not_cont, users, sales)
            else:
                cont, not_cont = self.split('age', contexts['context_1'])
                feature = 'age'
                low_bound = self.get_low_bound(cont, not_cont, users, sales)
            # add possibility to recombine contexts
            if low_bound > self.get_low_bound(contexts[0].classes, [], users, sales):
                #split
                new_contexts = {
                    'context_1': Context(classes=cont, feature=feature, context_name='giuseppe',
                                         mch=self.mch, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args),
                    'context_2': Context(classes=not_cont, feature=feature, context_name='giuseppe',
                                         mch=self.mch, mab_algorithm=self.mab_algorithm, mab_args=self.mab_args),
                    'context_3': Context(classes=contexts['context_2'].classes, feature=contexts['context_2'].feature,
                                         context_name=contexts['context_2'].context_name, mch=self.mch,
                                         mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)
                }
            else:
                #no split
                new_contexts = {
                    'context_1': Context(classes=contexts['context_1'].classes, feature=contexts['context_1'].feature,
                                         context_name=contexts['context_1'].context_name, mch=self.mch,
                                         mab_algorithm=self.mab_algorithm, mab_args=self.mab_args),
                    'context_2': Context(classes=contexts['context_2'].classes, feature=contexts['context_2'].feature,
                                         context_name=contexts['context_2'].context_name, mch=self.mch,
                                         mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)
                }
        else:
            # add possibility to recombine contexts
            new_contexts = {
                'context_1': Context(classes=contexts['context_1'].classes, feature=contexts['context_1'].feature,
                                     context_name=contexts['context_1'].context_name, mch=self.mch,
                                     mab_algorithm=self.mab_algorithm, mab_args=self.mab_args),
                'context_2': Context(classes=contexts['context_2'].classes, feature=contexts['context_2'].feature,
                                     context_name=contexts['context_2'].context_name, mch=self.mch,
                                     mab_algorithm=self.mab_algorithm, mab_args=self.mab_args),
                'context_3': Context(classes=contexts['context_3'].classes, feature=contexts['context_3'].feature,
                                     context_name=contexts['context_3'].context_name, mch=self.mch,
                                     mab_algorithm=self.mab_algorithm, mab_args=self.mab_args)
            }

        return new_contexts

    def split(self, feature, context):
        """
        this function splits according to the considered feature
        :param feature: the feature we want to evaluate
        :param context: the context we want to split
        :return:
        """
        class_cont = {}
        class_not_cont = {}
        if context.n_classes == 3:
            if feature == 'age':
                class_cont = {'class_1': self.classes[{0, 0}], 'class_2': self.classes[{0, 1}]}
                class_not_cont = self.classes[{1, 1}]
            else:
                class_cont = {'class_1': self.classes[{1, 1}], 'class_2': self.classes[{0, 1}]}
                class_not_cont = self.classes[{0, 0}]

        elif context.n_classes == 2:
            if feature == 'age':
                class_cont = self.classes[{1, 1}]
                class_not_cont = self.classes[{0, 0}]
            else:
                class_cont = self.classes[{0, 1}]
                class_not_cont = self.classes[{0, 0}]

        return class_cont, class_not_cont

    def get_low_bound(self, cont, not_cont, users, sales):
        """
        this function evaluates a feature based on the classes that it splits
        :param sales:
        :param users: number of users in the last week for each class
        :param cont: the class we want to put in the context
        :param not_cont: the class we don't want to put in the context
        :return: the lower bound of the context to be generated
        """
        delta_1 = 5
        z_1 = 0
        x_1 = 0
        delta_2 = 5
        z_2 = 0
        x_2 = 0
        for classe in cont:
            z_1 += users[classe]
            x_1 += sales[classe]
        for classe in not_cont:
            z_2 += users[classe]
            x_2 += sales[classe]
        tot = z_1 + z_2
        return z_1/tot *(x_1 - math.sqrt(-math.log(delta_1) / 2 * z_1)) + z_2/tot*(x_2 - math.sqrt(-math.log(delta_2) / 2 * z_2))
