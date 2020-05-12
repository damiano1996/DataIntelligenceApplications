class Week():

    def __init__(self, week_number, contexts, learners):
        """
        :param week_number: number of the current week. This param plays a role of identifier.
        :param contexts: dictionary of the following shape:
                {'context_1': features, 'context_2': features, ...}
                    where features is a list containing the features of the context: e.g. ['<30', 'worker]
        :param learners: list of learners, one learner for each context
        """
        self.number = week_number
        if len(list(contexts.keys())) != len(learners):
            print(f'The number of contexts is not equal to the number of learners.\n'
                  f'Contexts passed: {len(list(contexts.keys()))}\tLearners: {len(learners)}.')

        else:
            self.pairs = []
            for (context_name, context_features), learner in zip(contexts.items(), learners):
                pair = {context_name: context_features, 'learner': learner}
                self.pairs.append(pair)

    def get_learner(self, user_features):
        """
            During the week we have to propose to the users a candidate price,
            basing our choice on the user's features and the contexts generated.
            From the contexts we select the associated learner
        :param user_features: list of the features of the user
        :return: Learner object -> the learner of the context of the user
        """
        # How many features of the user are in each contexts?
        counters = []
        for pair in self.pairs:
            context_name = list(pair.keys())[0]  # to get the name of the context
            context_features = pair[context_name]
            counter = 0
            for user_feature in user_features:
                if user_feature in context_features:
                    counter += 1
            # adding the counter to the list
            counters.append(counter)
        # getting the index of the max counter
        idx = counters.index(max(counters))
        # returning the learner associated to the context in which the user falls
        return self.pairs[idx]['learner']
