from project.dia_pckg.Config import features_space


# for each user we can observe the value of two binary features
class User():
    def __init__(self, feature_1_value, feature_2_value):
        """
        :param feature_1_value: value of the first feature
        :param feature_2_value: value of the second feature
        """
        self.features = {
            features_space.keys()[0]: feature_1_value,
            features_space.keys()[1]: feature_2_value
        }
