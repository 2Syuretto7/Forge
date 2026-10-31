import numpy as np


def fit_standardizer(X_train):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    return mean, np.where(std == 0, 1.0, std)


def transform(X, mean, std):
    return (X - mean) / std


def fit_transform_both(X_train, X_test):
    mean, std = fit_standardizer(X_train)
    return transform(X_train, mean, std), transform(X_test, mean, std)
