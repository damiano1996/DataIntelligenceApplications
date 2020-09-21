import numpy as np

from project.part_2.GPTS_Learner import GPTS_Learner


# Extension of the standard GP_Learner for implementing a sliding-window combinatorial
# bandit algorithm due to the presence of multiple abrupt phases
class DLChangeDetect(GPTS_Learner):
    def __init__(self, n_arms, arms):
        super().__init__(n_arms, arms)
        self.minlen = 3

    def indexisofarm(self, pulled_arm):
        indexis = np.array([])
        for i in range(0, len(self.pulled_arms)):
            if (self.pulled_arms[i] == self.arms[pulled_arm]):
                indexis = np.append(indexis, i)
        return indexis

    def update_observations(self, pulled_arm, reward):
        # CHECK FOR CHANGES
        if (len(self.rewards_per_arm[pulled_arm]) > self.minlen):

            meandiff = reward - np.array(self.rewards_per_arm[pulled_arm]).mean()
            std = np.array(self.rewards_per_arm[pulled_arm]).std()
            import warnings
            warnings.filterwarnings("ignore")
            try:
                test = np.abs(meandiff / std)
            except:
                test = 0

            if test > 3:
                print("CAMBIO len=" + str(len(self.rewards_per_arm[pulled_arm])) + " std=" + str(std) + " test=" + str(
                    test))
                self.rewards_per_arm[pulled_arm].clear()
                indexToDelete = self.indexisofarm(pulled_arm)
                self.collected_rewards = np.delete(self.collected_rewards, indexToDelete)
                self.pulled_arms = np.delete(self.pulled_arms, indexToDelete)

        self.rewards_per_arm[pulled_arm].append(reward)
        self.pulled_arms = np.append(self.pulled_arms, self.arms[pulled_arm])
        self.collected_rewards = np.append(self.collected_rewards, reward)
