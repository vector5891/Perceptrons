# stringops.py
# String processing functions

# Test-Driven Development (TDD): write failing tests FIRST, then write
# code to make tests pass.
from hypothesis import given, assume
from hypothesis.strategies import text

def capitalizeWord(word):
    """Make the first character of word uppercase. If first character is
    not a letter, or the word is the empty string, just return the
    word as-is.

    >>> capitalizeWord('Chris')
    'Chris'
    >>> capitalizeWord('chris')
    'Chris'
    >>> capitalizeWord('42')
    '42'
    >>> capitalizeWord('-6')
    '-6'
    >>> capitalizeWord('  ')
    '  '
    >>> capitalizeWord(' hello')
    ' hello'
    >>> capitalizeWord('étienne')
    'Étienne'
    >>> capitalizeWord('δx')
    'Δx'
    >>> capitalizeWord('')
    ''
    """
    if len(word) == 0:
        return word
    else:
        return word[0].upper() + word[1:]

def trimSpaces(s):
    """Remove trailing and leading spaces, but leave interior spaces alone.

    >>> trimSpaces('  yes  ')
    'yes'
    >>> trimSpaces('   not   here   ')
    'not   here'
    """
    return s.strip()

# Example of using unittest module
# Often, unittest code is put into a *separate* file.
import unittest
class StringOpsTests(unittest.TestCase):
    # Each test is written as a separate method in this class.
    def test_trim_spaces(self):
        self.assertEqual('hello world',
                         trimSpaces('     hello world    '))
    def test_trim_preserves_interior_spaces(self):
        self.assertEqual(trimSpaces('wow!  it works.   '),
                         'wow!  it works.')
    # Can specify some initialization code that runs before/after each
    # test.
    def setUp(self):
        print("BEFORE")
    def tearDown(self):
        print("AFTER")
    # We're still within the unittest-derived class, but we're going
    # to use hypothesis for specifying properties.
    @given(s=text())
    def test_first_char_is_capital(self, s):
        assume(len(s) > 0) # if false, this test case won't count
        lc_latin_b_curls = [0x221, 0x234, 0x235, 0x236]
        assume(s[0].isalpha() and ord(s[0]) < 128) # ascii only
        assert capitalizeWord(s)[0].isupper()

    @given(s=text())
    def test_rest_of_string_unchanged(self, s):
        assume(len(s) > 0)
        assert capitalizeWord(s)[1:] == s[1:]


if __name__ == "__main__":
    # This block runs only if this script is being run directly, not
    # if it's being imported into another module.
    import doctest
    fails, tests = doctest.testmod()
    assert fails == 0 and tests > 0
    print("Passed", tests, "doc tests.")
    unittest.main()
