def seconds_in_days(days):
    """Return the number of seconds in `days` days."""
    return days * 24 * 60 * 60


def average(xs):
    """Return the mean of a non-empty list of numbers."""
    return sum(xs) / len(xs)


def percent_change(old, new):
    """Return the change from old to new as a percentage of old."""
    return 100 * (new - old) / old


def compound(amount, rate, years):
    """Return amount grown by the fraction rate per year for the given years."""
    return amount * (1 + rate) ** years
