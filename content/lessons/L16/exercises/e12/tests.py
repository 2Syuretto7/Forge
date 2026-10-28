import sub

stream = list(range(100))


def run(total, state):
    return [sub.shuffle_step(stream, state) for _ in range(total)]


def test_exact_resume():
    straight = run(100, sub.new_state(10, 0))
    assert sorted(straight) == stream
    state = sub.new_state(10, 0)
    first = run(37, state)
    saved = sub.checkpoint(state)
    run(5, state)
    resumed = first + run(63, sub.restore(saved))
    assert resumed == straight
    assert sub.shuffle_step(stream, state) is not None


def test_naive_resume_loses_items():
    state = sub.new_state(10, 0)
    first = run(37, state)
    naive = first + sub.naive_resume(stream, 10, 0, state["pos"], 63)
    assert sorted(naive) != stream
