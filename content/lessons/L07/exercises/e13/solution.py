def forward_flops(sizes, B):
    return sum(2 * B * a * b for a, b in zip(sizes, sizes[1:]))


def backward_flops(sizes, B):
    layers = list(zip(sizes, sizes[1:]))
    total = sum(4 * B * a * b for a, b in layers)
    a0, b0 = layers[0]
    return total - 2 * B * a0 * b0


def params(sizes):
    return sum(a * b + b for a, b in zip(sizes, sizes[1:]))


def flops_per_param_per_example(sizes, B):
    return (forward_flops(sizes, B) + backward_flops(sizes, B)) / (params(sizes) * B)
