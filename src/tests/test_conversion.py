import io
import pytest
from tests.common import data_file
from conversion import convert
from inputs import format_kml
from outputs import feature_output_formats


# just test that the code paths do not fail


@pytest.fixture
def kml_file():
    return data_file("kml/kml-with-extended-data.kml")


def to_csv_with_format(file, format_name):
    with io.StringIO() as f:
        convert(file, f, format_kml, feature_output_formats[format_name], True)
        return f.getvalue()


def test_convert_wkt(kml_file):
    print(to_csv_with_format(kml_file, "wkt"))


def test_convert_geojson_geometry(kml_file):
    print(to_csv_with_format(kml_file, "geojson-geometry"))


def test_convert_geojson_feature(kml_file):
    print(to_csv_with_format(kml_file, "geojson-feature"))
