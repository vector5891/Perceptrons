# 3-armed bandit
import random
import numpy as np

class Bandit(object):
    def numLevers(self):
        return 3

    def pull(self, lever):
        r = random.random()
        if lever == 0:
            if r < 0.25:
                return 4.0
            else:
                return 0.0
        elif lever == 1:
            if r < 0.10:
                return 90.0
            elif r < 0.20:
                return 15.0
            else:
                return 0.0
        elif lever == 2:
            if r < 0.20:
                return 6.0
            else:
                return 0.0
        else:
            print("ERROR: no lever ", lever)

class Agent(object):
    def __init__(self, bandit):
        self.learningRate = 0.1
        self.exploreRate = 0.6
        self.expectedPayouts = np.zeros([bandit.numLevers()])
        self.bandit = bandit

    def playOneRound(self):
        r = random.random()
        if r < self.exploreRate:
            # We're going to explore, so choose
            # uniform-random from possible moves.
            k = random.randrange(self.bandit.numLevers())
            reward = self.bandit.pull(k)
            print("Explore ", k, reward)
            # Update estimate of expected payouts
            self.expectedPayouts[k] += self.learningRate * (reward - self.expectedPayouts[k])
        else:
            # We're going to exploit (argmax)
            k = self.expectedPayouts.argmax()
            reward = self.bandit.pull(k)
            print("Exploit ", k, reward)
        print(self.expectedPayouts)
        return reward

    def playMultipleRounds(self, n):
        rewards = 0
        for _ in range(n):
            rewards += self.playOneRound()
        print("Total rewards: ", rewards)
        return rewards

if __name__ == "__main__":
    b = Bandit()
    a = Agent(b)
    a.playMultipleRounds(1000)
