"""
    Definition of the User.
"""

import numpy as np

from project.dia_pckg.Config import features_space, classes_config


# for each user we can observe the value of two binary features
class User:

    def __init__(self, features=None, class_name=None, random=False):
        """
        :param features: binary features of the user
        :param class_name: name of the class of the user
        :param random: to create a user with random params
        """
        self.class_name = class_name
        if features is None and class_name is not None:
            self.features = classes_config[self.class_name]

        if random:
            self.generate_random()

    def generate_random(self):
        """
            to generate an user with random parameters
        :return:
        """
        self.class_name = np.random.choice(list(classes_config.keys()))
        self.features = classes_config[self.class_name]

    def get_features_meaning(self):
        """
        :return: list of values of the features
        """
        features_meaning = []
        for i, bin in enumerate(self.features):
            feat_value = features_space[list(features_space.keys())[i]][bin]
            features_meaning.append(feat_value)
        return features_meaning


if __name__ == '__main__':
    # example
    user = User(class_name='elegant')
    print(user.get_features_meaning())
