# Finding planted features

Plant 12 sparse features in 8 dimensions, more features than dimensions, and see whether a sparse autoencoder finds them. `sae_loss` (exercise 7), `make_activations` and `recovered` are provided.

Implement `train_sae(X, m, l1, steps=1000, lr=0.01, seed=0, batch=256)`: Adam on minibatches; decoder rows initialized as random unit vectors, the encoder as a copy of them, $b_e = 0$ and $b_d$ at the data mean; after every step, rescale the decoder rows to unit length.

## Hints

1. Without the rescaling, the L1 penalty could be dodged by shrinking $z$ and growing the decoder.
2. Draw the minibatch indices and the initialization from one generator.
3. Too small an L1 weight gives a dense code that reconstructs well and recovers little; sparsity is what makes the latents line up with features.
