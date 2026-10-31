def forward_flops(sizes, B):
    raise NotImplementedError


def backward_flops(sizes, B):
    raise NotImplementedError


def params(sizes):
    raise NotImplementedError


def flops_per_param_per_example(sizes, B):
    raise NotImplementedError
