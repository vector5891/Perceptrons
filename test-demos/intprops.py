# intprops.py
from hypothesis import given, assume
import hypothesis.strategies as st
import unittest

def even(x):
    return x%2 == 0

def odd(x):
    return x%2 == 1

class IntPropertyTests(unittest.TestCase):
    @given(i=st.integers())
    def test_even_or_odd(self, i):
        assert even(i) or odd(i)

    @given(i=st.integers())
    def test_succ_odd_is_even(self, i):
        assume(odd(i))
        assert even(i+1)

if __name__ == "__main__":
    unittest.main()
