"""Implementation of Knuth Moris Pratt algorithm for finding all occurrences of string in text."""


def knp_iterator(text, pattern):
    """
    Implementation of Knuth-Moris-Pratt algorithm. David Eppstein, UC Irvine, 1 Mar 2002.

    Yields all starting positions of the pattern.
    """
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    # do the actual search
    start_pos = 0
    match_len = 0
    for c in text:
        while match_len == len(pattern) or match_len >= 0 and pattern[match_len] != c:
            start_pos += shifts[match_len]
            match_len -= shifts[match_len]
        match_len += 1
        if match_len == len(pattern):
            yield start_pos
