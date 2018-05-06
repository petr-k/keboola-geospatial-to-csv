import filecmp
import pytest
from src.my_component import run


def test_run_00():
    base = '/code/tests/data/00/'
    run(base)
    result = filecmp.cmp(base + "out/tables/destination.csv",
                            base + "_sample_out/tables/destination.csv",
                            False)
    assert True == result
