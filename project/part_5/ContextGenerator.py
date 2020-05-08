class ContextGenerator():

    def __init__(self):
        pass

    def get_weekly_contexts(self, features, users):
        """
        :param features: features admissible
        :param users: list of User object: they are users collected from the beginning of the campaign
        :return: dictionary of the following shape:
                {'context_1': features, 'context_2': features, ...}
                    where features is a list containing the features of the context: e.g. ['<30', 'worker]
        """
        pass
