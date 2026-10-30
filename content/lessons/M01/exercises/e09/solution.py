def matvec(W, x):
    """Multiply list-of-rows W by list x with loops; return (y, flops)."""
    y, flops = [], 0
    for row in W:
        acc = 0.0
        for w, xj in zip(row, x):
            acc = acc + w * xj
            flops += 2
        y.append(acc)
    return y, flops


def mlp_flops(widths, batch=1):
    """Forward-pass FLOPs of dense layers with these widths, for batch inputs."""
    return sum(2 * a * b for a, b in zip(widths[:-1], widths[1:])) * batch


def mlp_params(widths):
    """Weights plus biases of dense layers with these widths."""
    return sum(a * b + b for a, b in zip(widths[:-1], widths[1:]))


def train_flops(n_params, n_tokens):
    """About 6 N D FLOPs to train N parameters on D tokens."""
    return 6 * n_params * n_tokens
