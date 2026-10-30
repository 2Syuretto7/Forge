def count_strings(alphabet, length):
    """Strings of the given length, repetition allowed."""
    return alphabet ** length


def count_distinct_strings(alphabet, length):
    """Strings with no repeated symbol."""
    n = 1
    for i in range(length):
        n *= max(0, alphabet - i)
    return n


def count_either(*sizes):
    """Options from one of several disjoint groups."""
    return sum(sizes)


def count_staged(*sizes):
    """Outcomes of a choice in stages."""
    n = 1
    for s in sizes:
        n *= s
    return n
