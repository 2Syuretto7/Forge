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
    raise NotImplementedError


def percent_bigger(a, b):
    """How much bigger unit a is than unit b, in percent."""
    raise NotImplementedError


def best_unit(value, unit):
    """Return (number, unit) in the unit of the same dimension giving the smallest result >= 1."""
    raise NotImplementedError
