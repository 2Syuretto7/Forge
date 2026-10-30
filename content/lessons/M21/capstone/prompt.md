# Capstone: a calibrated spam filter

The starter provides `make_corpus(n_docs, seed)` as in e10.

1. `fit(X, y, alpha=1.0)` and `log_odds(model, X)`: naive Bayes with Laplace smoothing.
2. `split(X, y)`: the first 12,000 messages for training, the next 4,000 for calibration and the last 4,000 for testing.
3. `ece(p, y, bins=10)` and `fit_temperature(z, y)` as in e11 and e12.
4. `report(seed=0)`: a dictionary with `"accuracy"` (test accuracy at threshold $\frac12$), `"ece_before"` and `"ece_after"` (test ECE without and with the fitted temperature), and `"temperature"`.
5. `NOTE`: at least 60 words on where the independence assumption fails in this data, how the fitted temperature shows it, and what the calibration does and does not change (it cannot change any decision at threshold $\frac12$).

The tests require accuracy above 0.95, a temperature above 1.2, `ece_after` below 0.015 and below `ece_before`, and a note that mentions the phrases and the temperature.
