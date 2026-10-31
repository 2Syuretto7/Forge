# Capstone: a two-hidden-layer MLP on digit-like images

`make_digits(n, seed)` in the starter renders 8 by 8 images of ten digit-like glyphs with random one-pixel shifts, random fading, missing pixels and Gaussian noise. Train on `make_digits(2000, 0)` and test on `make_digits(1000, 1)`.

Implement, writing every gradient yourself (no autograd library):

1. `init(sizes, seed)` and `loss_and_grads(params, X, y)` for a ReLU network with **two hidden layers** and a softmax cross-entropy output.
2. `train(X, y, seed)`: minibatch SGD with hyperparameters of your choice; return the trained `params`. Keep it under about 3 seconds of CPU time.
3. `evaluate(params, X, y)`: test accuracy.
4. `REPORT`: at least 60 words with your architecture, hyperparameters, test accuracy, and the accuracy of a linear softmax classifier on the same split for comparison (the tests compute it too), plus one sentence on why the MLP does better on shifted images.

The tests require two hidden layers, a test accuracy of at least 0.88, a gradient check of your backward pass, and an MLP that beats the linear baseline by at least 10 points.
