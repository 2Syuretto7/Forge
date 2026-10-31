import sub

SIZES = [5, 3, 7]


def test_every_item_once_per_epoch():
    order = sub.epoch_order(SIZES, 0, 42)
    assert sorted(order) == sorted((s, i) for s in range(3) for i in range(SIZES[s]))
    assert order == sub.epoch_order(SIZES, 0, 42)
    assert order != sub.epoch_order(SIZES, 1, 42)


def test_resume_matches_an_uninterrupted_run():
    state = {"epoch": 0, "index": 0}
    straight = []
    for _ in range(12):
        batch, state = sub.next_batch(SIZES, 4, 7, state)
        straight += batch
    assert state == {"epoch": 3, "index": 3}
    state = {"epoch": 0, "index": 0}
    resumed = []
    for _ in range(5):
        batch, state = sub.next_batch(SIZES, 4, 7, state)
        resumed += batch
    saved = dict(state)
    for _ in range(7):
        batch, saved = sub.next_batch(SIZES, 4, 7, saved)
        resumed += batch
    assert resumed == straight
