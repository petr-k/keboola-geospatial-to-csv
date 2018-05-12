import pytest
import shutil
import os
from processor import run


data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'data')

out_tables_dir = os.path.join(data_dir, "out/tables")


@pytest.fixture(autouse=True)
def clean_out_tables_dir():
    def clean():
        for _, dirs, _ in os.walk(out_tables_dir):
            for d in dirs:
                shutil.rmtree(os.path.join(out_tables_dir, d))
    clean()
    yield None
    clean()


def out_table_exists(rel_path):
    return os.path.isfile(os.path.join(out_tables_dir, rel_path))


def test_run():
    run(data_dir)
    assert out_table_exists("kml/kml-with-extended-data.kml.csv")
    assert out_table_exists("shapefile/stations.shp.csv")
