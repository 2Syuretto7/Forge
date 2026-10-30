# Functions as sets of pairs

A function from a finite domain is a list of pairs `(input, output)`. Write:

- `is_function(pairs, domain)`: every element of `domain` appears exactly once as an input, and nothing else does.
- `apply(pairs, x)`: the output paired with `x`.
- `is_injective(pairs)`: no two inputs share an output.
- `is_surjective(pairs, codomain)`: every element of `codomain` is an output.
- `compose(f, g)`: the function "first `g`, then `f`" as a list of pairs, for every input of `g`.
- `all_functions(domain, codomain)`: the list of every function from the domain to the codomain, each as a list of pairs. There are $|\text{codomain}|^{|\text{domain}|}$ of them.

## Hints

1. Collect the inputs `[a for a, _ in pairs]` and compare with the domain, counting repeats.
2. `compose(f, g)` is `[(x, apply(f, y)) for x, y in g]`.
3. `itertools.product(codomain, repeat=len(domain))` lists every choice of outputs.
