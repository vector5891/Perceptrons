# matchdna.py

# This code is intended to find the locations of certain segments in
# (potentially very long) DNA sequences, represented as Python
# strings. DNA consists of a sequence of nucleotides, which are
# represented as the characters 'A', 'C', 'G', and 'T' -- they may be
# upper or lower-case in different data sets.

def listMatchLocations(haystack, needle):
    """Returns a list of each index where NEEDLE may be found in HAYSTACK.
    Both parameters must be strings containing nucleotide characters
    in "ACGTacgt". Below is a doctest example.

    >>> seq1 = "CTCCTGACTTTCCTCGCTTGGTGGTTTGAGTGGACTTCCCAGGCC"
    >>> listMatchLocations(seq1, "TCCTC")
    [10]
    >>> listMatchLocations(seq1, "GACT")
    [5, 32]

    For easier checking of these results, here's the DNA string with
    the indices printed underneath it:

        CTCCTGACTTTCCTCGCTTGGTGGTTTGAGTGGACTTCCCAGGCC
        01234567890123456789012345678901234567890123456789
                  1         2         3         4

    So you can confirm that index 10 does indeed contain "TCCTC" and
    indexes 5 and 32 both contain "GACT". So yay, it works!! Or does
    it...?

    """
    matches = []
    withinMatch = False
    start = 0
    n = 0                          # 'n' is index into 'needle'
    for h in range(len(haystack)): # 'h' is index into 'haystack'
        if n == len(needle):  # At end of needle, so it's a match!
            matches.append(start)
            start = h           # Start over
            n = 0
        elif needle[n] != haystack[h]: # Mismatched character
            start = h                  # Start over
            n = 0
        n += 1
    return matches

if __name__ == "__main__":
    import doctest
    fails, tests = doctest.testmod()
    assert fails == 0 and tests > 0
    print("Passed", tests, "doc tests.")
