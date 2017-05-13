# Perceptrons!
import random

class TwoStepFun(object):
    """A step function with configurable threshold.

    >>> 3+3
    6
    >>> f1 = TwoStepFun()
    >>> f1.threshold
    0.5
    >>> f1(0.4)
    0
    >>> f1(0.6)
    1

    >>> f2 = TwoStepFun(1)
    >>> f2(0.99)
    0
    >>> f2(-1.2)
    0
    >>> f2(1.001)
    1
    """
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def __call__(self, value):
        if value < self.threshold:
            return 0
        else:
            return 1

class Perceptron(object):
    """Represent a perceptron with N inputs, bias.

    >>> p1 = Perceptron(transfer=TwoStepFun(1))
    >>> p1.weights = [0.6, 0.6, 0.0]
    >>> bits = [0,1]
    >>> [p1([a,b]) for a in bits for b in bits]
    [0, 0, 0, 1]

    >>> p2 = Perceptron(transfer=TwoStepFun(1))
    >>> p2.weights = [1.1, 1.1, 0.0]
    >>> bits = [0,1]
    >>> [p2([a,b]) for a in bits for b in bits]
    [0, 1, 1, 1]
    """
    def __init__(self, numInputs=2, learningRate=0.2,
                 transfer=TwoStepFun()):
        self.transfer = transfer
        self.weights = [random.random()*4-2 for _ in range(numInputs+1)]
        self.learningRate = learningRate

    def __call__(self, xs):
        assert(len(xs)+1 == len(self.weights))
        avg = self.weights[len(self.weights)-1] # bias input
        for i in range(len(xs)):
            avg += xs[i] * self.weights[i]
        return self.transfer(avg)

    def fuzzWeightAt(self, i):
        self.weights[i] += (random.random()*2*self.learningRate) - self.learningRate
    def fuzzOne(self):
        self.fuzzWeightAt(random.randrange(len(self.weights)))

    def fuzzAll(self):
        for i in range(len(self.weights)):
            self.fuzzWeightAt(i)

    def learn(self, xs, target):
        out = self(xs)
        err = target - out
        print(xs,target,out,err)
        for i in range(len(self.weights)):
            x = xs[i] if i < len(xs) else 1
            delta = self.learningRate * err * x
            self.weights[i] += delta
        return err

if __name__ == "__main__":
    from datetime import datetime
    import doctest
    random.seed(datetime.now())
    fails, tests = doctest.testmod()
    assert fails == 0 and tests > 0

    # Learn AND gate
    p = Perceptron(transfer=TwoStepFun(0.5))
    print(p.weights)
    bits = [0,1]
    k = 0
    while True:
        wrong = 0
        for a in bits:
            for b in bits:
                wrong += abs(p.learn([a, b], a and b))  # AND
                print(p.weights)
        k += 1
        if wrong == 0:
            print("DONE in %d cycles" % k)
            break
