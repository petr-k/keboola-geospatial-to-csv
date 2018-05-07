import pytest
from tests.common import data_file
from inputs import format_shapefile


@pytest.fixture
def shp_file():
    return data_file("shapefile/stations.shp")


def test_open(shp_file):
    data_source = format_shapefile.open(shp_file)
    assert data_source


def test_get_nonspatial_field_names(shp_file):
    data_source = format_shapefile.open(shp_file)
    names = list(data_source.get_non_spatial_field_names())
    assert set([
        'name',
        'marker-col',
        'marker-sym',
        'line']) == set(names)


def test_iterate_features(shp_file):
    data_source = format_shapefile.open(shp_file)
    assert 86 == len(list(data_source.get_features()))


def test_get_features(shp_file):
    data_source = format_shapefile.open(shp_file)
    field_names = set(data_source.get_non_spatial_field_names())
    for f in data_source.get_features():
        values = data_source.get_non_spatial_field_values_for_feature(f)
        assert set(values.keys()) == field_names
        assert not f.GetGeometryRef().IsEmpty()
