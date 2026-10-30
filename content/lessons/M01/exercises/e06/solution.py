UNITS = {
    "s": ("time", 1),
    "min": ("time", 60),
    "h": ("time", 3600),
    "day": ("time", 86400),
    "B": ("data", 1),
    "KB": ("data", 10 ** 3),
    "MB": ("data", 10 ** 6),
    "GB": ("data", 10 ** 9),
    "TB": ("data", 10 ** 12),
    "KiB": ("data", 2 ** 10),
    "MiB": ("data", 2 ** 20),
    "GiB": ("data", 2 ** 30),
    "TiB": ("data", 2 ** 40),
    "FLOP": ("work", 1),
    "GFLOP": ("work", 10 ** 9),
    "TFLOP": ("work", 10 ** 12),
    "PFLOP": ("work", 10 ** 15),
}


def convert(value, frm, to):
    """Convert value from unit frm to unit to; ValueError across dimensions."""
    (dim_a, size_a), (dim_b, size_b) = UNITS[frm], UNITS[to]
    if dim_a != dim_b:
        raise ValueError(f"cannot convert {dim_a} to {dim_b}")
    return value * size_a / size_b


def percent_bigger(a, b):
    """How much bigger unit a is than unit b, in percent."""
    if UNITS[a][0] != UNITS[b][0]:
        raise ValueError("different dimensions")
    return 100 * (UNITS[a][1] / UNITS[b][1] - 1)


def best_unit(value, unit):
    """Return (number, unit) in the unit of the same dimension giving the smallest result >= 1."""
    dim = UNITS[unit][0]
    options = [(convert(value, unit, u), u) for u, (d, _) in UNITS.items() if d == dim]
    big_enough = [o for o in options if o[0] >= 1]
    if big_enough:
        return min(big_enough)
    return max(options)
