# Modules, parameters and an optimizer

Add the object layer on top of the engine:

- `Module.parameters()` returns every parameter of the module and of its submodules, found among its attributes: a Tensor marked `is_param` (created with `Parameter`), a `Module`, or a list or tuple of modules. `zero_grad()` sets each parameter's gradient to `None`.
- `Linear(n_in, n_out, rng)`: weight `W` of shape `(n_in, n_out)` drawn with He initialization (normal times $\sqrt{2/n_\text{in}}$), bias `b` of zeros; `forward(x)` returns `x @ W + b`.
- `MLP(sizes, seed=0)`: a list `self.layers` of `Linear` layers created with one `np.random.default_rng(seed)`, ReLU between layers and none after the last.
- `SGD(params, lr)`: `step()` subtracts `lr * grad` from each parameter that has a gradient; `zero_grad()` clears them.

## Hints

1. Iterate over `self.__dict__.values()` in `parameters()`; attributes keep their assignment order, so `W` comes before `b`.
2. `Parameter(data)` is given; it marks the tensor with `is_param = True`.
3. Update `p.data` in place in `step()`; the tensor object must stay the same so the module still refers to it.
