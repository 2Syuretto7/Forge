def pascal_rows(n):
    """Rows 0..n of Pascal's triangle."""
    rows = [[1]]
    for _ in range(n):
        prev = rows[-1]
        rows.append([1] + [prev[i - 1] + prev[i] for i in range(1, len(prev))] + [1])
    return rows


def expand(a, b, n):
    """Terms C(n, k) a**k b**(n - k) for k = 0..n."""
    row = pascal_rows(n)[-1]
    return [row[k] * a ** k * b ** (n - k) for k in range(n + 1)]


def poly_power(n):
    """Coefficients of (1 + x)**n, lowest power first."""
    return pascal_rows(n)[-1]
