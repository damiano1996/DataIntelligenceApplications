from project.dia_pckg.Config import features_space


# for each user we can observe the value of two binary features
class User():

    def __init__(self, features):
        """
        :param features: binary features of the user
        """
        self.features = features

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
    user = User([1, 1])
    print(user.get_features_meaning())
