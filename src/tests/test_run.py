import pytest
import shutil
import os
from processor import run


data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'data')

out_files_dir = os.path.join(data_dir, "out/files")


@pytest.fixture(autouse=True)
def clean_out_files_dir():
    def clean():
        for _, dirs, _ in os.walk(out_files_dir):
            for d in dirs:
                shutil.rmtree(os.path.join(out_files_dir, d))
    clean()
    yield None
    # clean()


def out_file_exists(rel_path):
    return os.path.isfile(os.path.join(out_files_dir, rel_path))


def test_run():
    run(data_dir)
    assert out_file_exists("kml/kml-with-extended-data.csv")
    assert out_file_exists("shapefile/stations.csv")
