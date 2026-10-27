# Turning recording off: no_grad

Inference does not need a graph. The engine in the starter already asks `is_grad_enabled()` when it creates a tensor: if recording is off, the new tensor gets no parents and no backward closure, so nothing is saved.

Implement the switch:

- `is_grad_enabled()` returns the current state (on at start).
- `no_grad` is a context manager: `with no_grad(): ...` turns recording off and restores the previous state on exit, also when the block raises and when blocks are nested.

## Hints

1. Keep the state in a module-level mutable, such as a one-element list.
2. Save the previous state in `__enter__`, restore it in `__exit__`, and return `False` from `__exit__` so exceptions propagate.
3. Restoring the previous state, rather than setting it to on, is what makes nesting correct.
