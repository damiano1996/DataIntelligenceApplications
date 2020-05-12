class Week():

    def __init__(self, week_number, MAB_algorithm):
        self.week_number = week_number
        self.MAB = MAB_algorithm

        self.contexts = []
        self.learners = []


class ContextInfo():

    def __init__(self, features):
        self.features = features
