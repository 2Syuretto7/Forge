def rates(tp, fn, fp, tn):
    """Sensitivity, specificity and predictive values."""
    return {"sensitivity": tp / (tp + fn), "specificity": tn / (tn + fp), "ppv": tp / (tp + fp), "npv": tn / (tn + fn)}


def ppv_at(prevalence, sensitivity, specificity):
    """Positive predictive value at another prevalence."""
    a = sensitivity * prevalence
    return a / (a + (1 - specificity) * (1 - prevalence))
