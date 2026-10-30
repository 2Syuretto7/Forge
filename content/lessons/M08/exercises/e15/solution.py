from fractions import Fraction


def p_six_in_rolls(n):
    """At least one six in n rolls."""
    return 1 - Fraction(5, 6) ** n


def p_by_adding(n):
    """n / 6, de Mere's reasoning."""
    return Fraction(n, 6)


def first_impossible():
    """Smallest n with n/6 > 1."""
    n = 1
    while p_by_adding(n) <= 1:
        n += 1
    return n


def overcount(n):
    """p_by_adding(n) - p_six_in_rolls(n)."""
    return p_by_adding(n) - p_six_in_rolls(n)


def p_double_six(n):
    """At least one double six in n rolls of two dice."""
    return 1 - Fraction(35, 36) ** n
