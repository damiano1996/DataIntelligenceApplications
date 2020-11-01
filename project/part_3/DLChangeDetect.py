import numpy as np

from project.part_2.GP_Learner import GP_Learner


# Extension of the standard GP_Learner for implementing a sliding-window combinatorial
# bandit algorithm due to the presence of multiple abrupt phases
class DLChangeDetect(GP_Learner):
    def __init__(self, arms, min_len=3, z_score=2.58):
        super().__init__(arms)
        self.min_len = min_len  # minimum number of data in the arm
        self.z_score = z_score
        self.day = 0

    def index_is_of_arm(self, pulled_arm):
        indices = np.array([])
        for i in range(0, len(self.pulled_arms)):
            if self.pulled_arms[i] == self.arms[pulled_arm]:
                indices = np.append(indices, i)
        return indices.astype(dtype=np.uint8)

    def update_observations(self, pulled_arm, reward):
        # CHECK FOR CHANGES
        if len(self.rewards_per_arm[pulled_arm]) > self.min_len:

            mean_diff = reward - np.array(self.rewards_per_arm[pulled_arm]).mean()
            std = np.array(self.rewards_per_arm[pulled_arm]).std()

            test = np.abs(mean_diff / std) if std != 0 else 0

            if test > self.z_score:
                print("Change detected (DAY: " + str(self.day) + "): len=" +
                      str(len(self.rewards_per_arm[pulled_arm])) +
                      " std=" + str(std) +
                      " test=" + str(test))
                self.rewards_per_arm[pulled_arm].clear()
                indices2delete = self.index_is_of_arm(pulled_arm)
                self.collected_rewards = np.delete(self.collected_rewards, indices2delete)
                self.pulled_arms = np.delete(self.pulled_arms, indices2delete)

        self.rewards_per_arm[pulled_arm].append(reward)
        self.collected_rewards = np.append(self.collected_rewards, reward)

        self.pulled_arms = np.append(self.pulled_arms, self.arms[pulled_arm])

        self.day = self.day + 1
