# Capstone: a calibrated multi-class classifier

`make_dataset()` in the starter generates 900 examples with 8 features on very different scales (one is in the thousands, one in tenths) and 3 classes. Use the first 600 rows for training and the last 300 for testing; never let the test rows influence training, including standardization statistics.

Implement `train_and_evaluate(X_train, y_train, X_test, y_test)`, choosing the learning rate, number of steps and L2 strength yourself. Return a dict with:

- `"accuracy"`, `"log_loss"`, `"ece"` (10 bins) on the test set,
- `"confusion"`: the 3 x 3 test confusion matrix (`C[true, predicted]`),
- `"W"` and `"b"`: the trained parameters (for standardized inputs).

Targets: test accuracy at least 0.87, log loss at most 0.30, ECE at most 0.06.

Then write `REPORT` (at least 80 words): your hyperparameters and why, the three numbers, which classes are confused with which, and whether the model is over- or under-confident according to the calibration bins.
