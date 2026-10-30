import random


def A(*xs):
    """Left-nested sum of the terms."""
    raise NotImplementedError


def M(*xs):
    """Left-nested product of the factors."""
    raise NotImplementedError


def P(x, n):
    raise NotImplementedError


def S(x, y):
    raise NotImplementedError


def D(x, y):
    raise NotImplementedError


NOTEBOOK = [
    {"title": "Difference of squares", "names": ["a", "b"],
     "steps": [M(A("a", "b"), S("a", "b")), S(A(P("a", 2), M("a", "b")), A(M("b", "a"), P("b", 2))), S(P("a", 2), P("b", 2))]},
    {"title": "Square of a sum", "names": ["x", "y"],
     "steps": [P(A("x", "y"), 2), M(A("x", "y"), A("x", "y")), A(P("x", 2), M(2, "x", "y"), P("y", 2))]},
    {"title": "Completing the square", "names": ["x"],
     "steps": [A(P("x", 2), M(6, "x"), 5), S(A(P(A("x", 3), 2), 5), 9), S(P(A("x", 3), 2), 4)]},
    {"title": "Linear equation, both sides minus 2", "names": ["x"],
     "steps": [S(A(M(3, "x"), 2), 11), S(M(3, "x"), 9), M(3, S("x", 3))]},
    {"title": "Cancel a common factor", "names": ["x"],
     "steps": [D(S(P("x", 2), 1), S("x", 1)), D(M(A("x", 1), S("x", 1)), S("x", 1)), A("x", 1)]},
    {"title": "Distribute a minus sign", "names": ["x", "y"],
     "steps": [S("x", S("y", 3)), S(S("x", "y"), 3), A(S("x", "y"), 3)]},
    {"title": "Add fractions", "names": ["a", "b"],
     "steps": [A(D(1, "a"), D(1, "b")), D(A("b", "a"), M("a", "b"))]},
    {"title": "Cube of a sum", "names": ["a", "b"],
     "steps": [P(A("a", "b"), 3), M(A("a", "b"), P(A("a", "b"), 2)), A(P("a", 3), M(3, P("a", 2), "b"), M(3, "a", P("b", 2)), P("b", 3))]},
    {"title": "Factor a quadratic", "names": ["x"],
     "steps": [A(S(P("x", 2), M(10, "x")), 21), M(S("x", 3), S("x", 7))]},
    {"title": "Sum of a geometric series of three terms", "names": ["r"],
     "steps": [A(1, "r", P("r", 2)), D(S(P("r", 3), 1), S("r", 1))]},
    {"title": "Square of a difference", "names": ["a", "b"],
     "steps": [P(S("a", "b"), 2), A(S(P("a", 2), M(2, "a", "b")), P("b", 2)), A(P("a", 2), P("b", 2))]},
    {"title": "Product of powers", "names": ["x"],
     "steps": [M(P("x", 2), P("x", 3)), P("x", 5)]},
    {"title": "Divide a sum", "names": ["a", "b", "c"],
     "steps": [D(A("a", "b"), "c"), A(D("a", "c"), D("b", "c"))]},
    {"title": "Expand a product of three", "names": ["x"],
     "steps": [M(A("x", 1), A("x", 2), A("x", 3)), M(A(P("x", 2), M(3, "x"), 2), A("x", 3)), A(P("x", 3), M(6, P("x", 2)), M(11, "x"), 6)]},
    {"title": "Average of two averages", "names": ["a", "b", "c", "d"],
     "steps": [D(A(D(A("a", "b"), 2), D(A("c", "d"), 2)), 2), D(A("a", "b", "c", "d"), 4)]},
]


def evaluate(expr, env):
    """Value of expr (number, name, or (op, left, right)) with variables from env."""
    raise NotImplementedError


def agree(e1, e2, names, trials=60, seed=0):
    """True when e1 and e2 agree at every random point in [-5, 5] where both are defined."""
    raise NotImplementedError


def first_bad_step(steps, names):
    """Index of the first step that differs from its predecessor, or None."""
    raise NotImplementedError


def audit(notebook):
    """(derivation index, step index) for each derivation with a bad step."""
    raise NotImplementedError
