def naive_reading(sensitivity):
    """The confused answer."""
    return sensitivity


def correct(prevalence, sensitivity, specificity):
    """P(ill | positive)."""
    a = sensitivity * prevalence
    return a / (a + (1 - specificity) * (1 - prevalence))


def overstatement(prevalence, sensitivity, specificity):
    """Naive over correct."""
    return naive_reading(sensitivity) / correct(prevalence, sensitivity, specificity)


def prosecutor(match_prob, population):
    """P(guilty | match) after searching the whole population."""
    return 1 / (1 + match_prob * (population - 1))
