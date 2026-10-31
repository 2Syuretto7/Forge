# Capstone: a 30-layer network that trains

The L03 digits, your layer norm and Adam are provided. Build a residual MLP with **at least 30 hidden layers**, writing every gradient yourself, and train it on `make_digits(2000, 0)`.

1. `init_model(depth, width, seed=0)` returns a dictionary of parameters, with one `(width, width)` weight matrix per hidden layer.
2. `loss_and_grads(params, X, y)` returns the mean softmax cross-entropy and a gradient for every parameter; it must work for any depth and width that `init_model` produces.
3. `train(seed=0)` builds a model with `DEPTH` hidden layers and trains it, returning `(params, losses)`. Keep it under about 2 seconds of CPU time (250 Adam steps at width 48 are enough).
4. `evaluate(params, X, y)` returns accuracy.
5. `REPORT`: at least 80 words explaining each stabilizing choice (residual connections, normalization and where it sits, initialization, learning rate and schedule) with your test accuracy.

The tests require at least 30 hidden layers, a gradient check, per-layer gradients at initialization within a factor of 30 of each other, a training loss that falls steadily, and at least 85 percent test accuracy on `make_digits(1000, 1)`.
