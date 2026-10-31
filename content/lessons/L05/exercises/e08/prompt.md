# Optimizers for a whole network

Parameters now live in a dictionary like L03's (`"W1"`, `"b1"`, ...), and every optimizer has a method `step(params, grads, lr=None)` that updates the arrays **in place**, using `lr` instead of its own rate when one is passed (so a schedule can drive it). Weight decay applies to the weight matrices only, the keys starting with `"W"`.

1. `SGD(lr, momentum=0.0, weight_decay=0.0)`: weight decay adds `weight_decay * W` to the gradient (for SGD that is the same as decay); with momentum, keep a velocity per parameter, $v \leftarrow \beta v + g$, and step by $\eta v$.
2. `Adam(lr, b1=0.9, b2=0.999, eps=1e-8, weight_decay=0.0, decoupled=True, bias_correction=True)`: with `decoupled=True` this is AdamW, shrinking each weight by `lr * weight_decay * W` outside the adaptive step; with `decoupled=False` the decay term is added to the gradient before the moments are updated (L2 inside Adam).

## Hints

1. Keep state in dictionaries keyed like `params`; `self.v.get(k, 0.0)` starts a velocity at zero.
2. Adam's step counter is shared by all parameters: increment it once per `step` call.
3. Update in place with `params[k] -= ...` so the caller's dictionary sees the change.
