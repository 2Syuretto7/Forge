# Training at depth 20

Adam (`adam_init`, `adam_step`), `evaluate` and the stack are provided. Implement `train(depth, width, mode, lr, steps, warmup=0, seed=0, batch=50, branch_scale=1.0)`:

- data `make_digits(2000, 0)`, parameters `init_stack(depth, width, seed, branch_scale=branch_scale)`, `rng = np.random.default_rng(seed)`;
- each epoch draws `rng.permutation(2000)` and visits it in full batches, until `steps` steps have run;
- step `t` (from 1) uses the rate `lr * min(1, t / warmup)` if `warmup > 0`, else `lr`;
- return `(params, losses)` with every minibatch loss.

Then train the plain and the pre-norm stacks at depth 20 and width 32 for 300 steps at rate 0.003 and compare.

## Hints

1. Wrap the loop in `with np.errstate(all="ignore"):` so a diverging variant does not flood the output.
2. Follow the order exactly (permutation, then batches, then the update) so your runs match the tests.
3. The pre-norm run takes about twice as long as the plain one: it computes two layer norms per layer.
