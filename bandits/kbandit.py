import random

class KBandit(object):
    def __init__(self, *args):
        """Create a k-armed bandit with specified payout probabilities.

        For example, b1 here has 2 levers. The first one (L0) has a
        50% chance of a $4 payout. The second one (L1) has a 20%
        chance of $3 payout, and 10% chance of $6. The expected values
        of these levers are as shown.

        >>> b1 = KBandit([(.5, 4)], [(.2, 3), (.1, 6)])
        KBandit with 2 levers:
          E(L0) =   2.00
          E(L1) =   1.20

        >>> iterations=10000
        >>> pulls0 = [b1.pull(0) for _ in range(iterations)]
        >>> round(sum(pulls0)/iterations, 1)
        2.0

        The above result should be 2.0 most of the time, but it is
        probabilistic, so there is a small chance it would be 1.9 or
        2.1 or so. Now let's try the other lever.

        >>> pulls1 = [b1.pull(1) for _ in range(iterations)]
        >>> round(sum(pulls1)/iterations, 1)
        1.2

        """
        self.levers = list(args)
        print("KBandit with %d levers:" % len(args))
        for i in range(len(args)):
            expected = 0.0
            for probability, payout in self.levers[i]:
                expected += probability * payout
            print("  E(L%d) = %6.2f" % (i, expected))

    def pull(self, lever):
        """Simulate pulling given lever, return the payout."""
        r = random.random()
        for probability, payout in self.levers[lever]:
            if r < probability:
                return payout
            else:
                r -= probability
        return 0.0


# Here's a sample bandit object we can use for testing.
bandit5a = KBandit([(.3, 2), (.1, 3)], # E(L0) = 0.9
                   [(.1, 7), (.1, 6)], # E(L1) = 1.3
                   [(.1, 4), (.2, 3)], # E(L2) = 1.0
                   [(.1, 6), (.2, 5)], # E(L3) = 1.6
                   [(.2, 3), (.2, 1)]) # E(L4) = 0.8

# Run doctests if we invoke this module directly.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
