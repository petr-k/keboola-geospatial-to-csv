import pytest
from tests.common import data_file
from inputs import format_kml


@pytest.fixture
def kml_file():
    return data_file("kml/kml-with-extended-data.kml")


def test_open(kml_file):
    data_source = format_kml.open(kml_file)
    assert data_source


def test_get_nonspatial_field_names(kml_file):
    data_source = format_kml.open(kml_file)
    names = list(data_source.get_non_spatial_field_names())
    assert set([
        'Name',
        'description',
        # 'timestamp',
        # 'begin',
        # 'end',
        'altitudeMode',
        'tessellate',
        'extrude',
        'visibility',
        'drawOrder',
        'icon',
        'edited',
        'blueyardage',
        'whiteyardage',
        'menshandicap',
        'menspar',
        'redyardage',
        'womenshandicap',
        'womenspar']) == set(names)


def test_iterate_features(kml_file):
    data_source = format_kml.open(kml_file)
    assert 3 == len(list(data_source.get_features()))


def test_get_features(kml_file):
    data_source = format_kml.open(kml_file)
    field_names = set(data_source.get_non_spatial_field_names())
    for f in data_source.get_features():
        values = data_source.get_non_spatial_field_values_for_feature(f)
        assert set(values.keys()) == field_names
        assert not f.GetGeometryRef().IsEmpty()
