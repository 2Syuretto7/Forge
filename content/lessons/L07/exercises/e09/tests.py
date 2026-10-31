import sub

# A small trace in the format above, built for this exercise: two matmuls, many small elementwise
# kernels with gaps between them, and one reduction.
EVENTS = [
    {"name": "gemm", "start": 0.0, "dur": 400.0},
    {"name": "gemm", "start": 410.0, "dur": 400.0},
]
t = 830.0
for i in range(20):
    EVENTS.append({"name": "elementwise", "start": t, "dur": 5.0})
    t += 15.0
EVENTS.append({"name": "reduce", "start": t, "dur": 50.0})


def test_summary():
    s = sub.summarize(EVENTS)
    assert list(s) == ["gemm", "elementwise", "reduce"]
    assert s["gemm"] == (2, 800.0) and s["elementwise"] == (20, 100.0) and s["reduce"] == (1, 50.0)


def test_idle_fraction():
    span = (t + 50.0) - 0.0
    busy = 950.0
    assert abs(sub.gpu_idle_fraction(EVENTS) - (1 - busy / span)) < 1e-12
    assert sub.gpu_idle_fraction([{"name": "a", "start": 0.0, "dur": 3.0}, {"name": "b", "start": 3.0, "dur": 2.0}]) == 0.0


def test_top_fraction():
    assert abs(sub.top_fraction(EVENTS) - 800 / 950) < 1e-12
    assert abs(sub.top_fraction(EVENTS, k=2) - 900 / 950) < 1e-12
