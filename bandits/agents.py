import random
import numpy as np

class NaiveGambler(object):
    """The naive gambler just randomly selects a lever on each play."""
    def __init__(self, numLevers):
        self.numLevers = numLevers

    def play(self, pull):
        pull(random.randrange(self.numLevers))

    def report(self):
        return ""

class ExactAverageGambler(object):
    def __init__(self, numLevers):
        self.exploreRate = 0.1
        self.actualPayouts = np.zeros([numLevers])
        self.numPulls = np.ones([numLevers])
        self.stopLearningAt = 10000

    def play(self, pull):
        r = random.random()
        numPulls = self.numPulls.sum()
        explore = r < self.exploreRate and numPulls < self.stopLearningAt
        if explore:
            lever = random.randrange(len(self.actualPayouts))
        else:
            lever = (self.actualPayouts / self.numPulls).argmax()
        payout = pull(lever)
        self.numPulls[lever] += 1
        self.actualPayouts[lever] += payout

    def report(self):
        return str(self.actualPayouts / self.numPulls)

class BasicEstimatingGambler(object):
    def __init__(self, numLevers):
        self.learningRate = 0.1
        self.exploreRate = 0.1
        self.estimatedPayouts = np.zeros([numLevers])

    def play(self, pull):
        r = random.random()
        explore = r < self.exploreRate
        if explore:
            # We're going to explore, so choose uniform-random from possible moves.
            lever = random.randrange(len(self.estimatedPayouts))
            payout = pull(lever)
            # Update estimate of expected payouts
            difference = payout - self.estimatedPayouts[lever]
            self.estimatedPayouts[lever] += self.learningRate * difference
        else:
            # We're going to exploit (use the maximum)
            # http://stackoverflow.com/questions/42071597/numpy-argmax-random-tie-breaking
            lever = np.random.choice(np.flatnonzero(self.estimatedPayouts == self.estimatedPayouts.max()))
            payout = pull(lever)

    def report(self):
        return str(self.estimatedPayouts)

if __name__ == "__main__":
    from kbandit import bandit5a
    from casino import evaluate
    evaluate(NaiveGambler, bandit5a)
    evaluate(BasicEstimatingGambler, bandit5a)
    evaluate(ExactAverageGambler, bandit5a)
