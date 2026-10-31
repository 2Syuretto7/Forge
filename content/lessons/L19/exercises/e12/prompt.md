# Break it: a probe on noise

In high dimensions a linear probe can separate almost any labelling of a small training set. Implement `random_feature_probe(n_train, n_test, d, seed=0)`: random features and random labels for both a training and a test set; train a probe (provided `train_probe`, 2000 steps, no regularization) and return its training and test accuracy.

With more dimensions than training examples the probe fits the noise perfectly and is at chance on new data.

## Hints

1. Draw training features, training labels, test features, test labels from one generator in that order.
2. Training accuracy measures capacity, not what the representation contains.
3. Always report held-out accuracy, and compare with a control task or random features.
