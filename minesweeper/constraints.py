# constraints.py    -*- coding: utf-8 -*-
import sys

class Constraints(object):
    """Represent Boolean constraints for (eg) Minesweeper.

    Simple use-case: track both known values (0/1) and sums.

    >>> cs = Constraints()
    >>> cs.add(0, "jkl")
    >>> cs.add(1, "a")
    >>> cs.add(2, "bcd")
    >>> cs.show()
    k=j=l=0
    a=1
    Σ c b d = 2

    We collapse the sum of N variables where the value is N.

    >>> cs = Constraints()
    >>> cs.add(3, "abc")
    >>> cs.show()
    a=c=b=1

    It should substitute known values into given equations.

    >>> cs = Constraints()
    >>> cs.add(0, "a")
    >>> cs.add(1, "b")
    >>> cs.add(3, "abcde")
    >>> cs.show()
    a=0
    b=1
    Σ c e d = 2
    """

    def __init__(self):
        # Dict with key representing variable name, value representing 0/1.
        self.known = {}
        # Set of equations represented as a pair: (value, variable-set)
        self.equations = set()

    def add(self, value, variables):
        if value == 0:            # If value is zero, all components known 0
            for var in variables:
                self.known[var] = 0
        elif len(variables) == value: # Same #variables as value
            for var in variables:
                self.known[var] = 1
        else:                   # Otherwise add to equations
            vs = set(variables)
            for var in self.known: # Subtract out known values
                if var in vs:
                    vs.remove(var)
                    if self.known[var] == 1:
                        value -= 1
            self.equations.add((value, frozenset(vs)))
            # frozenset is because the values within set may not be modified.

    def show(self):
        # First output zeros
        ok = False
        for var in self.known:
            if self.known[var] == 0:
                ok = True
                sys.stdout.write(str(var) + "=")
        if ok:
            sys.stdout.write("0\n")
        # Then output ones
        ok = False
        for var in self.known:
            if self.known[var] == 1:
                ok = True
                sys.stdout.write(str(var) + "=")
        if ok:
            sys.stdout.write("1\n")
        # Then output equations
        for value, variables in self.equations:
            sys.stdout.write("Σ ")
            for var in variables:
                sys.stdout.write(str(var) + " ")
            sys.stdout.write("= %d\n" % value)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
