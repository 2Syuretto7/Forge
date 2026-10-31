import numpy as np
import sub

clean = np.zeros(6)
clean[[0, 3]] = 1
corrupt = np.zeros(6)
corrupt[[1, 3]] = 1


def test_finds_the_responsible_unit():
    e = sub.patch_effects(clean, corrupt)
    assert e.shape == (4,)
    assert np.argmax(np.abs(e)) == 0 and e[0] > 0.9
    assert e[1] == 0 and e[3] == 0
