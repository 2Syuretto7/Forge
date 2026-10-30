def naive_reading(sensitivity):
    """The confused answer."""
    raise NotImplementedError


def correct(prevalence, sensitivity, specificity):
    """P(ill | positive)."""
    raise NotImplementedError


def overstatement(prevalence, sensitivity, specificity):
    """Naive over correct."""
    raise NotImplementedError


def prosecutor(match_prob, population):
    """P(guilty | match) after searching the whole population."""
    raise NotImplementedError
