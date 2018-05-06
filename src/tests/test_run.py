import filecmp
import os
from my_component import run


def test_run_00():
    base = os.path.dirname(os.path.realpath(__file__)) + '/data/00/'
    run(base)
    result = filecmp.cmp(base + "out/tables/destination.csv",
                         base + "_sample_out/tables/destination.csv",
                         False)
    assert result is True
